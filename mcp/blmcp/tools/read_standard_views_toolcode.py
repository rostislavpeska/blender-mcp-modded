# SPDX-License-Identifier: GPL-3.0-or-later

"""
Tool-code for rendering every standardized camera into one contact sheet.

Renders each camera in the standard-camera collection (created by
``place_standard_cameras``) with a fast EEVEE pass, composites the views into a
single 2x2 montage (front / right / back / left), and returns it as a base64
PNG. Render settings and the active camera are restored afterwards.

A single image is returned (not a list) because the MCP/pydantic layer cannot
build an output schema for ``list[Image]`` and crashes tool registration.
"""

__all__ = (
    "Params",
    "Result",
    "main",
)

import base64
import os
import tempfile
from typing import NamedTuple

# MCP messages are capped at 1 MB; base64 expands data by 4/3.
_IMAGE_SIZE_LIMIT_IN_BYTES = (1_048_576 * 3) // 4

# Preferred 2x2 layout order (falls back to name sort for anything unexpected).
_VIEW_ORDER = {"_std_front": 0, "_std_right": 1, "_std_back": 2, "_std_left": 3}


class Params(NamedTuple):
    collection_name: str = "_mcp_standard_cameras"
    resolution: int = 640
    samples: int = 16


class Result(NamedTuple):
    status: str
    image_base64: str | None = None
    views: list[str] | None = None
    message: str | None = None


# @include_begin: _template_image_downscale_to_size_limit.py
def _image_downscale_to_size_limit(
        tmpdir: str, filepath: str, size_limit_in_bytes: int, size_tolerance_in_bytes: int = 0,
) -> bytes:
    return b''
# @include_end


def main(params: Params) -> Result:
    import bpy  # pylint: disable=import-error,no-name-in-module
    import numpy as np  # pylint: disable=import-error

    if bpy.app.background:
        return Result(status="error", message="Rendering views is not available in background mode")

    coll = bpy.data.collections.get(params.collection_name)
    cams = [o for o in coll.objects if o.type == 'CAMERA'] if coll is not None else []
    if not cams:
        return Result(
            status="error",
            message="No standard cameras in %r; run place_standard_cameras first" % params.collection_name,
        )
    cams.sort(key=lambda o: (_VIEW_ORDER.get(o.name, 99), o.name))

    scene = bpy.context.scene
    rd = scene.render
    saved = {
        "camera": scene.camera,
        "engine": rd.engine,
        "resolution_x": rd.resolution_x,
        "resolution_y": rd.resolution_y,
        "resolution_percentage": rd.resolution_percentage,
        "filepath": rd.filepath,
        "file_format": rd.image_settings.file_format,
        "hide_viewport": coll.hide_viewport,
    }

    try:
        coll.hide_viewport = False
        for engine in ('BLENDER_EEVEE_NEXT', 'BLENDER_EEVEE'):
            try:
                rd.engine = engine
                break
            except (TypeError, ValueError):
                continue
        try:
            scene.eevee.taa_render_samples = max(1, params.samples)
        except AttributeError:
            pass
        rd.resolution_x = params.resolution
        rd.resolution_y = int(params.resolution * 0.75)
        rd.resolution_percentage = 100
        rd.image_settings.file_format = 'PNG'

        names: list[str] = []
        with tempfile.TemporaryDirectory(prefix="blmcp_stdviews_") as tmpdir:
            tiles = []
            for cam in cams:
                scene.camera = cam
                filepath = os.path.join(tmpdir, cam.name + ".png")
                rd.filepath = filepath
                try:
                    bpy.ops.render.render(write_still=True)
                except RuntimeError as ex:
                    return Result(status="error", message=str(ex))
                img = bpy.data.images.load(filepath)
                w, h = img.size
                buf = np.empty(w * h * 4, dtype=np.float32)
                img.pixels.foreach_get(buf)
                tiles.append(buf.reshape(h, w, 4))
                names.append(cam.name)
                bpy.data.images.remove(img)

            # Composite into a 2-column grid (pixel rows are bottom-up).
            th, tw, _ = tiles[0].shape
            cols = 2
            rows = (len(tiles) + cols - 1) // cols
            canvas = np.zeros((rows * th, cols * tw, 4), dtype=np.float32)
            canvas[..., 3] = 1.0
            for i, tile in enumerate(tiles):
                r = i // cols
                c = i % cols
                y0 = (rows - 1 - r) * th
                canvas[y0:y0 + th, c * tw:(c + 1) * tw, :] = tile

            montage = bpy.data.images.new("_std_montage", width=cols * tw, height=rows * th, alpha=True)
            montage.pixels.foreach_set(canvas.reshape(-1))
            montage_path = os.path.join(tmpdir, "montage.png")
            montage.filepath_raw = montage_path
            montage.file_format = 'PNG'
            montage.save()
            bpy.data.images.remove(montage)

            data = _image_downscale_to_size_limit(
                tmpdir, montage_path,
                size_limit_in_bytes=_IMAGE_SIZE_LIMIT_IN_BYTES,
                size_tolerance_in_bytes=_IMAGE_SIZE_LIMIT_IN_BYTES // 16,
            )
            image_base64 = base64.b64encode(data).decode("ascii")
    finally:
        scene.camera = saved["camera"]
        rd.engine = saved["engine"]
        rd.resolution_x = saved["resolution_x"]
        rd.resolution_y = saved["resolution_y"]
        rd.resolution_percentage = saved["resolution_percentage"]
        rd.filepath = saved["filepath"]
        rd.image_settings.file_format = saved["file_format"]
        coll.hide_viewport = saved["hide_viewport"]

    return Result(status="ok", image_base64=image_base64, views=names)
