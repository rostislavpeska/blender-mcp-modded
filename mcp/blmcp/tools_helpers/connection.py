# SPDX-FileCopyrightText: 2026 Blender Authors
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Socket client for communicating with the Blender add-on.

Used by MCP "tools" that send-code to the Blender add-on.

Which Blender: several instances can run at once, each on its own port, and each one that
bound a port registers itself (see the add-on's ``instance_registry.py``). The port is chosen as:

1. ``BLENDER_MCP_PORT`` in this server's environment: an explicit pin, the registry is not read.
2. The instance chosen with ``select_blender_instance`` in this server process.
3. The only live registered instance, which is then kept for this server process,
   so a later call fails loudly instead of moving to another Blender when it goes away.

With no registered instance or several, the call is refused with the list; it never falls back
to port 9876, because the instance answering there may be another agent's Blender.
"""

__all__ = (
    "get_connection_params",
    "host",
    "instance_select",
    "instance_selection",
    "live_instances",
    "port_answers",
    "registry_dir",
    "send_code",
    "send_code_to",
)

import json
import os
import socket
import sys
from collections.abc import Callable

_DEFAULT_HOST = "localhost"
_TIMEOUT = 300.0
_RECV_BUFFER_SIZE = 65536

_ENV_HOST = "BLENDER_MCP_HOST"
_ENV_PORT = "BLENDER_MCP_PORT"
# Same folder as the add-on's `instance_registry.registry_dir` (a test keeps both in step).
_ENV_REGISTRY_DIR = "BLENDER_MCP_REGISTRY_DIR"


class _Selection:
    """
    The instance this server process talks to, chosen by ``select_blender_instance`` or automatically.

    One MCP server process serves one client session, so the choice is per session.
    """

    pid: int | None = None
    port: int | None = None
    # "selected" (by the tool), "auto" (the only live instance) or "port" (an unregistered port).
    how: str = ""

    @classmethod
    def clear(cls) -> None:
        cls.pid = None
        cls.port = None
        cls.how = ""


def registry_dir() -> str:
    """
    Return the folder where each running add-on server writes ``<pid>.json``.
    """
    override = os.environ.get(_ENV_REGISTRY_DIR)
    if override:
        return override
    if sys.platform == "win32":
        base = os.environ.get("LOCALAPPDATA") or os.path.join(os.path.expanduser("~"), "AppData", "Local")
    else:
        base = os.environ.get("XDG_STATE_HOME") or os.path.join(os.path.expanduser("~"), ".local", "state")
    return os.path.join(base, "blender-mcp", "instances")


def _process_image_windows(pid: int) -> str | None:
    """
    Return the executable path of a live process, ``""`` for a dead one, ``None`` when unknown.
    """
    import ctypes  # pylint: disable=import-outside-toplevel
    from ctypes import wintypes  # pylint: disable=import-outside-toplevel

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
            return str(buf.value)
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


def _pid_alive(pid: int, image: str = "") -> bool:
    """
    Return whether *pid* runs; when *image* is given, also that it still runs that executable (no pid reuse).
    """
    if pid <= 0:
        return False
    live_image = _process_image_windows(pid) if sys.platform == "win32" else _process_image_posix(pid)
    if live_image == "":
        return False
    if image and live_image:
        return os.path.basename(live_image).lower() == os.path.basename(image).lower()
    return True


def live_instances(
        directory: str | None = None,
        alive_fn: Callable[[int, str], bool] | None = None,
) -> list[dict[str, object]]:
    """
    Return the registry records of running instances, sorted by port; stale and unreadable records are skipped.
    """
    alive = _pid_alive if alive_fn is None else alive_fn
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


def _instance_line(rec: dict[str, object]) -> str:
    return "pid {:s} port {:s} file {:s} session {:s} started {:s}".format(
        str(rec.get("pid")),
        str(rec.get("port")),
        str(rec.get("filepath") or "(unsaved)"),
        str(rec.get("session") or "-"),
        str(rec.get("started_utc") or "?"),
    )


def _instances_text(instances: list[dict[str, object]]) -> str:
    return "\n".join("  - " + _instance_line(rec) for rec in instances)


def port_answers(port: int, host_name: str | None = None, timeout: float = 1.0) -> bool:
    """
    Return whether something accepts connections on *port*.
    """
    try:
        socket.create_connection((host_name or host(), port), timeout=timeout).close()
    except OSError:
        return False
    return True


def instance_select(
        pid: int | None = None,
        port: int | None = None,
        directory: str | None = None,
        alive_fn: Callable[[int, str], bool] | None = None,
        answers_fn: Callable[[int], bool] | None = None,
) -> dict[str, object]:
    """
    Choose the instance this server process talks to, by *pid* or *port*; with neither, clear the choice.

    A port without a registry record (an add-on that does not register itself) is accepted only
    when something answers on it. Raise ``ValueError`` when the choice does not match a live instance.
    """
    if pid is None and port is None:
        _Selection.clear()
        return {"selected": None, "message": "Selection cleared; the next call picks the only live instance."}
    instances = live_instances(directory, alive_fn)
    matches = [
        rec for rec in instances
        if (pid is None or int(str(rec["pid"])) == pid) and (port is None or int(str(rec["port"])) == port)
    ]
    if matches:
        rec = matches[0]
        _Selection.pid = int(str(rec["pid"]))
        _Selection.port = int(str(rec["port"]))
        _Selection.how = "selected"
        return {"selected": rec, "message": "This MCP session now talks to " + _instance_line(rec)}
    if pid is None and port is not None:
        answers = port_answers if answers_fn is None else answers_fn
        if answers(port):
            _Selection.pid = None
            _Selection.port = port
            _Selection.how = "port"
            return {
                "selected": {"pid": None, "port": port},
                "message": (
                    "Port {:d} answers but has no registry record (an add-on without instance registration). "
                    "This MCP session now talks to it; check its scene before changing anything."
                ).format(port),
            }
    raise ValueError(
        "No live Blender instance matches pid={!r} port={!r}. Live instances (registry {:s}):\n{:s}".format(
            pid, port, directory or registry_dir(), _instances_text(instances) or "  (none)",
        )
    )


def instance_selection() -> dict[str, object]:
    """
    Return this server process's current choice (for ``list_blender_instances``).
    """
    pinned = os.environ.get(_ENV_PORT, "").strip()
    return {
        "pinned_port": int(pinned) if pinned else None,
        "selected_pid": _Selection.pid,
        "selected_port": _Selection.port,
        "how": _Selection.how,
    }


def host() -> str:
    """
    Return the host the add-on servers listen on (``BLENDER_MCP_HOST``, default localhost).
    """
    return os.environ.get(_ENV_HOST, _DEFAULT_HOST)


def get_connection_params(
        directory: str | None = None,
        alive_fn: Callable[[int, str], bool] | None = None,
) -> tuple[str, int]:
    """
    Return ``(host, port)`` of the Blender this server process talks to; see the module doc-string.

    Raise ``ConnectionError`` with the list of instances when the choice is missing or ambiguous.
    """
    host_name = host()
    pinned = os.environ.get(_ENV_PORT, "").strip()
    if pinned:
        return host_name, int(pinned)

    if _Selection.how == "port" and _Selection.port is not None:
        return host_name, _Selection.port

    instances = live_instances(directory, alive_fn)
    if _Selection.pid is not None:
        for rec in instances:
            if int(str(rec["pid"])) == _Selection.pid:
                return host_name, int(str(rec["port"]))
        raise ConnectionError(
            (
                "The Blender this MCP session was using (pid {:d}, port {:s}) is no longer running. "
                "Not switching to another instance silently. Call `list_blender_instances`, then "
                "`select_blender_instance(pid=...)`. Live instances:\n{:s}"
            ).format(_Selection.pid, str(_Selection.port), _instances_text(instances) or "  (none)")
        )

    if len(instances) == 1:
        rec = instances[0]
        _Selection.pid = int(str(rec["pid"]))
        _Selection.port = int(str(rec["port"]))
        _Selection.how = "auto"
        return host_name, _Selection.port
    if not instances:
        raise ConnectionError(
            (
                "No running Blender has registered an MCP server in {:s}. Start Blender with the MCP add-on "
                "(it registers when it binds its port). An older add-on that does not register can be used "
                "with `select_blender_instance(port=...)` or by pinning {:s} for this MCP server."
            ).format(directory or registry_dir(), _ENV_PORT)
        )
    raise ConnectionError(
        (
            "Several Blender instances are running; not guessing which one this session means. "
            "Call `select_blender_instance(pid=...)` (or `port=...`) first:\n{:s}"
        ).format(_instances_text(instances))
    )


def send_code_to(
        host: str,
        port: int,
        code: str,
        strict_json: bool,
        timeout: float = _TIMEOUT,
) -> dict[str, object]:
    """
    Send Python code to the add-on server at *host*:*port*; see ``send_code``.
    """
    request = json.dumps({
        "type": "execute",
        "code": code,
        "strict_json": strict_json,
    }) + "\0"

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            sock.connect((host, port))
            sock.sendall(request.encode("utf-8"))

            # Read response until the null byte delimiter.
            buf = bytearray()
            while True:
                chunk = sock.recv(_RECV_BUFFER_SIZE)
                if not chunk:
                    break
                buf.extend(chunk)
                if b"\0" in buf:
                    break
    except ConnectionRefusedError as ex:
        raise ConnectionError(
            "Cannot connect to Blender at {:s}:{:d}. "
            "Ensure Blender is running with the MCP addon enabled and the server started.".format(host, port)
        ) from ex
    except socket.timeout as ex:
        raise ConnectionError(
            "Blender connection timed out at {:s}:{:d}".format(host, port)
        ) from ex
    except OSError as ex:
        # NOTE: intentionally not catching `Exception` here.
        # Callers use `ConnectionError` to trigger a fallback path;
        # a broader catch would mask real bugs as connection failures.
        raise ConnectionError(
            "Socket error communicating with Blender at {:s}:{:d}: {:s}".format(host, port, str(ex))
        ) from ex

    if not buf:
        raise ConnectionError("Empty response from Blender")

    # Parse only up to the first null byte delimiter.
    line, _sep, _rest = buf.partition(b"\0")
    try:
        response: dict[str, object] = json.loads(line.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as ex:
        raise ConnectionError(
            "Invalid response from Blender at {:s}:{:d}: {:s}".format(host, port, str(ex))
        ) from ex
    return response


def send_code(code: str, strict_json: bool) -> dict[str, object]:
    """
    Send Python code to the Blender add-on socket server for execution.

    Returns the full response dict from the add-on containing
    ``status`` (``"ok"`` or ``"error"``), ``result`` (on success),
    ``message`` (on error), and optionally ``stdout``/``stderr``
    captured during execution.

    Raises ``ConnectionError`` when Blender is unreachable, when no single
    instance is chosen (see ``get_connection_params``) or when it
    returns an invalid response.
    """
    host, port = get_connection_params()
    return send_code_to(host, port, code, strict_json)
