# SPDX-FileCopyrightText: 2026 Blender Authors
#
# SPDX-License-Identifier: GPL-3.0-or-later

# pylint: disable=C0114  # See tool doc-string.
# Audit: 2026-10-17-claude-opus-5.5 port-per-session-01 (register R7/R14).

__all__ = (
    "register",
)

from blmcp.tools_helpers import connection
from mcp.server.fastmcp import FastMCP  # pylint: disable=import-error,no-name-in-module
from mcp.types import ToolAnnotations  # pylint: disable=import-error,no-name-in-module

# Seconds to wait for each instance when reading its live file name and unsaved state.
_PROBE_TIMEOUT = 3.0

_PROBE_CODE = (
    "import bpy\n"
    "result = {'filepath': bpy.data.filepath, 'is_dirty': bool(bpy.data.is_dirty)}\n"
)


def _probe(port: int) -> dict[str, object]:
    """
    Return the live file name and unsaved state of the instance on *port* (read-only).
    """
    try:
        response = connection.send_code_to(
            connection.host(), port, _PROBE_CODE, strict_json=True, timeout=_PROBE_TIMEOUT,
        )
    except ConnectionError as ex:
        return {"probe_error": str(ex)}
    result = response.get("result")
    if response.get("status") != "ok" or not isinstance(result, dict):
        return {"probe_error": str(response.get("message", response))}
    return {"live_filepath": result.get("filepath"), "is_dirty": result.get("is_dirty")}


def register(mcp: FastMCP) -> None:
    @mcp.tool(
        annotations=ToolAnnotations(
            title="List Blender Instances",
            readOnlyHint=True,
        )
    )
    def list_blender_instances(probe: bool = True) -> dict[str, object]:
        """
        List the running Blender instances that registered an MCP server, and which one this session uses.

        Each instance has its own port. When several run, the other tools refuse to guess:
        choose one with ``select_blender_instance``.
        With *probe*, each instance is asked (read-only) for its open file and unsaved state.
        """
        selection = connection.instance_selection()
        instances = []
        for rec in connection.live_instances():
            item = dict(rec)
            item["selected"] = (
                selection["pinned_port"] is None and
                selection["selected_pid"] is not None and
                rec.get("pid") == selection["selected_pid"]
            )
            if probe:
                item.update(_probe(int(str(rec["port"]))))
            instances.append(item)
        return {
            "registry": connection.registry_dir(),
            "selection": selection,
            "instances": instances,
        }

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Select Blender Instance",
            readOnlyHint=False,
            destructiveHint=False,
        )
    )
    def select_blender_instance(pid: int | None = None, port: int | None = None) -> dict[str, object]:
        """
        Choose which running Blender this MCP session talks to, by process id or port.

        The choice holds for this session only, so two sessions can drive two Blender instances.
        Call with neither argument to clear it. A ``BLENDER_MCP_PORT`` pin of the MCP server wins over it.
        """
        try:
            result = connection.instance_select(pid=pid, port=port)
        except ValueError as ex:
            return {"status": "error", "message": str(ex)}
        if connection.instance_selection()["pinned_port"] is not None:
            result["warning"] = "BLENDER_MCP_PORT pins this MCP server; the selection is ignored while it is set."
        return {"status": "ok", **result}
