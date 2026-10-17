# SPDX-FileCopyrightText: 2026 Blender Authors
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Per-process registry of running MCP bridge servers.

Each Blender that binds a port writes ``<registry>/<pid>.json``
(``{pid, port, host, filepath, started_utc, session, binary, background}``),
refreshes ``filepath`` when a file is loaded or saved and removes the file on exit.
The MCP server reads the folder to find the Blender it should talk to,
so several Blender instances can run side by side on different ports.

The registry folder is ``%LOCALAPPDATA%\\blender-mcp\\instances`` on Windows,
``$XDG_STATE_HOME/blender-mcp/instances`` (default ``~/.local/state``) elsewhere,
or ``BLENDER_MCP_REGISTRY_DIR`` when set.
A record whose process is gone (a crash skips the removal) is ignored by readers.

The MCP server keeps its own copy of the reader (``blmcp/tools_helpers/connection.py``),
because the add-on and the server are installed separately; a test keeps both in step.

This module does not import ``bpy`` at module level, so it can be tested outside Blender.

Audit: 2026-10-17-claude-opus-5.5 port-per-session-01 (register R7/R14).
"""

__all__ = (
    "pid_alive",
    "read_live",
    "record_path",
    "refresh_filepath",
    "registry_dir",
    "remove",
    "write",
    "write_for_this_blender",
)

import datetime
import json
import os
import sys
from collections.abc import Callable

# Overrides the registry folder (tests, or several isolated setups on one machine).
_ENV_REGISTRY_DIR = "BLENDER_MCP_REGISTRY_DIR"
# A free-form label set by whoever launched this Blender (e.g. the agent session).
_ENV_SESSION = "BLENDER_MCP_SESSION"


def registry_dir() -> str:
    """
    Return the folder that holds one ``<pid>.json`` per running bridge server.
    """
    override = os.environ.get(_ENV_REGISTRY_DIR)
    if override:
        return override
    if sys.platform == "win32":
        base = os.environ.get("LOCALAPPDATA") or os.path.join(os.path.expanduser("~"), "AppData", "Local")
    else:
        base = os.environ.get("XDG_STATE_HOME") or os.path.join(os.path.expanduser("~"), ".local", "state")
    return os.path.join(base, "blender-mcp", "instances")


def record_path(pid: int | None = None, directory: str | None = None) -> str:
    """
    Return the record file of *pid* (default: this process).
    """
    return os.path.join(directory or registry_dir(), "{:d}.json".format(os.getpid() if pid is None else pid))


def _write_json(path: str, data: dict[str, object]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    # Write a temporary file and move it into place, so a reader never sees half a record.
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)
    os.replace(tmp, path)


def write(
        host: str,
        port: int,
        filepath: str,
        binary: str = "",
        background: bool = False,
        pid: int | None = None,
        session: str | None = None,
        directory: str | None = None,
) -> str:
    """
    Write the record of a bridge server that has just bound *port*. Return the record path.
    """
    pid = os.getpid() if pid is None else pid
    data: dict[str, object] = {
        "pid": pid,
        "port": port,
        "host": host,
        "filepath": filepath,
        "started_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "session": os.environ.get(_ENV_SESSION, "") if session is None else session,
        "binary": binary,
        "background": background,
    }
    path = record_path(pid, directory)
    _write_json(path, data)
    return path


def refresh_filepath(filepath: str, pid: int | None = None, directory: str | None = None) -> bool:
    """
    Update the ``filepath`` of an existing record. Return False when there is no record.
    """
    path = record_path(pid, directory)
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError):
        return False
    if data.get("filepath") == filepath:
        return True
    data["filepath"] = filepath
    _write_json(path, data)
    return True


def remove(pid: int | None = None, directory: str | None = None) -> bool:
    """
    Delete the record of *pid* (default: this process). Return whether a file was removed.
    """
    try:
        os.remove(record_path(pid, directory))
    except FileNotFoundError:
        return False
    return True


def _process_image_windows(pid: int) -> str | None:
    """
    Return the executable path of a live process, ``""`` for a dead one, ``None`` when unknown.
    """
    import ctypes
    from ctypes import wintypes

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.OpenProcess.restype = wintypes.HANDLE
    kernel32.OpenProcess.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)
    process_query_limited_information = 0x1000
    still_active = 259
    handle = kernel32.OpenProcess(process_query_limited_information, False, pid)
    if not handle:
        # 87 = ERROR_INVALID_PARAMETER: no such process. Anything else (access denied) means it exists.
        return "" if ctypes.get_last_error() == 87 else None
    try:
        code = wintypes.DWORD()
        if kernel32.GetExitCodeProcess(handle, ctypes.byref(code)) and code.value != still_active:
            return ""
        size = wintypes.DWORD(32768)
        buf = ctypes.create_unicode_buffer(size.value)
        if kernel32.QueryFullProcessImageNameW(handle, 0, buf, ctypes.byref(size)):
            return buf.value
        return None
    finally:
        kernel32.CloseHandle(handle)


def _process_image_posix(pid: int) -> str | None:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return ""
    except PermissionError:
        return None
    try:
        return os.readlink("/proc/{:d}/exe".format(pid))
    except OSError:
        return None


def pid_alive(pid: int, image: str = "") -> bool:
    """
    Return whether process *pid* is running.

    When *image* (the recorded executable) is given and the live process runs a different
    executable, the pid was reused by another program and the record is treated as stale.
    """
    if pid <= 0:
        return False
    if sys.platform == "win32":
        live_image = _process_image_windows(pid)
    else:
        live_image = _process_image_posix(pid)
    if live_image == "":
        return False
    if image and live_image:
        return os.path.basename(live_image).lower() == os.path.basename(image).lower()
    return True


def read_live(
        directory: str | None = None,
        alive_fn: Callable[[int, str], bool] | None = None,
) -> list[dict[str, object]]:
    """
    Return the records of running instances, sorted by port. Unreadable and stale records are skipped.
    """
    alive = pid_alive if alive_fn is None else alive_fn
    folder = directory or registry_dir()
    try:
        names = sorted(os.listdir(folder))
    except OSError:
        return []
    records: list[dict[str, object]] = []
    for name in names:
        if not name.endswith(".json"):
            continue
        try:
            with open(os.path.join(folder, name), encoding="utf-8") as fh:
                data = json.load(fh)
            pid = int(data["pid"])
            int(data["port"])
        except (OSError, ValueError, KeyError, TypeError):
            continue
        if alive(pid, str(data.get("binary") or "")):
            records.append(data)
    records.sort(key=lambda r: int(str(r["port"])))
    return records


def write_for_this_blender(host: str, port: int) -> str:
    """
    Write this Blender's record after its server bound *port*. Return the record path.
    """
    import bpy  # pylint: disable=import-error,import-outside-toplevel

    return write(
        host=host,
        port=port,
        filepath=bpy.data.filepath,
        binary=bpy.app.binary_path,
        background=bool(bpy.app.background),
    )
