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
from blmcp.tools.import_canonical_model_toolcode import Params
from mcp.server.fastmcp import FastMCP  # pylint: disable=import-error,no-name-in-module
from mcp.types import ToolAnnotations  # pylint: disable=import-error,no-name-in-module

_TOOL_CALL = toolcode_wrap_with_calling_convention(toolcode_load_from_filepath(__file__))


def register(mcp: FastMCP) -> None:
    @mcp.tool(
        annotations=ToolAnnotations(
            title="Import Canonical Model",
        )
    )
    def import_canonical_model(
        source: str,
        pivot: str = "center",
        target_size: float = 1.0,
        collection_name: str = "",
    ) -> dict[str, object]:
        """
        Import a 3D model and canonicalize it in one step.

        *source* is an http(s) URL (e.g. a generated .glb) or a local file path
        (.glb/.gltf/.obj/.fbx). The model is joined into a single mesh, its
        transforms are applied, it is uniformly scaled so its largest bounding-box
        dimension equals *target_size*, its origin is set to *pivot* ("center" =
        bounding-box centre, "bottom" = base centre), and it is placed at the
        world origin. Pass *collection_name* to link it into a specific collection.

        Returns the object name and its final bounding box.
        """
        p = Params(
            source=source,
            pivot=pivot,
            target_size=target_size,
            collection_name=collection_name,
        )
        return send_code(toolcode_format_call(_TOOL_CALL, p), strict_json=True)
