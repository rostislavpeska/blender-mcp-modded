# SPDX-License-Identifier: GPL-3.0-or-later

# pylint: disable=C0114  # See tool doc-string.

__all__ = (
    "register",
)

from blmcp.tools_helpers import (
    toolcode_format_call,
    toolcode_load_from_filepath,
    toolcode_wrap_with_calling_convention,
)
from blmcp.tools_helpers.connection import send_code
from blmcp.tools.place_standard_cameras_toolcode import Params
from mcp.server.fastmcp import FastMCP  # pylint: disable=import-error,no-name-in-module
from mcp.types import ToolAnnotations  # pylint: disable=import-error,no-name-in-module

_TOOL_CALL = toolcode_wrap_with_calling_convention(toolcode_load_from_filepath(__file__))


def register(mcp: FastMCP) -> None:
    @mcp.tool(
        annotations=ToolAnnotations(
            title="Place Standard Cameras",
        )
    )
    def place_standard_cameras(
        distance_multiplier: float = 2.5,
        collection_name: str = "_mcp_standard_cameras",
        target_collection: str | None = None,
        ignore_object_names: list[str] | None = None,
    ) -> dict[str, object]:
        """
        Place four standardized framing cameras (front, right, back, left) around
        the scene, fitted to the bounds of the framed meshes and aimed at their
        centre. The cameras live in a hidden collection (excluded from the
        viewport, still renderable).

        By default every mesh in the scene is framed. Pass *target_collection* to
        frame only the meshes inside one collection, and/or *ignore_object_names*
        to drop objects (e.g. a large ground or water plane) that would otherwise
        dominate the fit.

        To read the views afterwards, call ``read_standard_views`` (or set one
        camera active and use ``render_viewport_to_path``).
        """
        p = Params(
            distance_multiplier=distance_multiplier,
            collection_name=collection_name,
            target_collection=target_collection,
            ignore_object_names=tuple(ignore_object_names or ()),
        )
        return send_code(toolcode_format_call(_TOOL_CALL, p), strict_json=True)
