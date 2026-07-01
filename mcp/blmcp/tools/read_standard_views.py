# SPDX-License-Identifier: GPL-3.0-or-later

# pylint: disable=C0114  # See tool doc-string.

__all__ = (
    "register",
)

import base64

from blmcp.tools_helpers import (
    toolcode_format_call,
    toolcode_load_from_filepath,
    toolcode_wrap_with_calling_convention,
)
from blmcp.tools_helpers.connection import send_code
from blmcp.tools.read_standard_views_toolcode import Params
from mcp.server.fastmcp import FastMCP, Image  # pylint: disable=import-error,no-name-in-module
from mcp.types import ToolAnnotations  # pylint: disable=import-error,no-name-in-module

_TOOL_CALL = toolcode_wrap_with_calling_convention(toolcode_load_from_filepath(__file__))


def register(mcp: FastMCP) -> None:
    @mcp.tool(
        annotations=ToolAnnotations(
            title="Read Standard Views",
            readOnlyHint=True,
        )
    )
    def read_standard_views(
        collection_name: str = "_mcp_standard_cameras",
        resolution: int = 640,
        samples: int = 16,
    ) -> Image:
        """
        Render every standardized camera (placed by ``place_standard_cameras``)
        and return a single 2x2 contact-sheet image (front / right / back / left)
        so the scene can be understood from all angles in one step. Render
        settings and the active camera are restored afterwards.

        Call ``place_standard_cameras`` first if the rig does not exist yet.
        """
        p = Params(collection_name=collection_name, resolution=resolution, samples=samples)
        response = send_code(toolcode_format_call(_TOOL_CALL, p), strict_json=True)
        if response.get("status") != "ok":
            raise RuntimeError(str(response.get("message", "Unknown error")))
        result = response["result"]
        assert isinstance(result, dict)
        if result.get("status") != "ok":
            raise RuntimeError(str(result.get("message", "Unknown error")))
        return Image(data=base64.b64decode(str(result["image_base64"])), format="png")
