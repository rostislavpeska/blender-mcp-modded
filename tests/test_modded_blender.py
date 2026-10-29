# SPDX-License-Identifier: GPL-3.0-or-later

"""Optional disposable Blender proof for retained cameras and canonical import.

Issue #1; audit: dev-2026-10-29-codex-01. Set BLENDER_BIN to opt in.
No MCP listener, installed add-on, owner file, network or provider calls.
"""

__all__ = ()

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

_ROOT = Path(__file__).resolve().parents[1]


def _proof():
    import bpy
    # Tool-code runs inside Blender without the host MCP package dependencies.
    sys.path.insert(0, str(_ROOT / "mcp/blmcp/tools"))
    import import_canonical_model_toolcode as importer
    import place_standard_cameras_toolcode as cameras
    import read_standard_views_toolcode as views

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    bpy.ops.mesh.primitive_cube_add(location=(2, 0, 1))
    bpy.ops.mesh.primitive_cube_add(location=(-2, 0, 1))
    bpy.ops.object.select_all(action="SELECT")
    with tempfile.TemporaryDirectory(prefix="mcp_features_") as folder:
        model = Path(folder) / "two_parts.glb"
        bpy.ops.export_scene.gltf(filepath=str(model), export_format="GLB", use_selection=True)
        archive = Path(folder) / "two_parts.zip"
        with zipfile.ZipFile(archive, "w") as zf:
            zf.write(model, "model/two_parts.glb")
        bpy.ops.object.delete(use_global=False)
        sentinel = bpy.data.objects.new("untouched", None)
        bpy.context.scene.collection.objects.link(sentinel)
        sentinel.location = (42, 43, 44)
        for source in (model, archive):
            result = importer.main(importer.Params(str(source), pivot="bottom", target_size=3,
                                                   collection_name="Imported"))
            assert result.status == "ok", result
            obj = bpy.data.objects[result.object]
            assert obj.mode == "OBJECT", obj.mode
            assert len(obj.data.vertices) == 48, len(obj.data.vertices)
            assert abs(max(obj.dimensions) - 3) < 1e-5, obj.dimensions[:]
            assert abs(result.bbox_min[2]) < 1e-5, result
            assert tuple(sentinel.location) == (42, 43, 44)
            bpy.data.objects.remove(obj, do_unlink=True)

    bpy.ops.mesh.primitive_cube_add(location=(1, 2, 3))
    cube = bpy.context.object
    cube.name = "framed"
    target = bpy.data.collections.new("Target")
    bpy.context.scene.collection.children.link(target)
    for coll in list(cube.users_collection):
        coll.objects.unlink(cube)
    target.objects.link(cube)
    bpy.ops.mesh.primitive_cube_add(location=(100, 100, 100), scale=(100, 100, 100))
    for _ in range(2):
        rig = cameras.main(cameras.Params(target_collection="Target"))
        assert rig.status == "ok", rig
        assert rig.center == [1, 2, 3], rig
        assert rig.max_size == 2, rig
        assert rig.cameras == ["_std_front", "_std_right", "_std_back", "_std_left"], rig
        collection = bpy.data.collections[rig.collection]
        assert len(collection.objects) == 5
        assert collection.hide_viewport and not collection.hide_render
        for name in rig.cameras:
            assert bpy.data.objects[name].constraints[0].target.name == "_std_target"
    refusal = views.main(views.Params())
    assert refusal.status == "error" and "background" in refusal.message, refusal
    print("MODDED_PROOF=" + json.dumps({"blender": bpy.app.version_string,
          "imports": ["two-part GLB", "ZIP with GLB"], "pivot": "bottom", "target_size": 3,
          "cameras": rig.cameras, "repeat_without_duplicates": True,
          "background_contact_sheet_refusal": True}))


@unittest.skipUnless(os.environ.get("BLENDER_BIN"), "set BLENDER_BIN for the disposable native proof")
class TestModdedBlender(unittest.TestCase):
    def test_import_and_camera_tools(self):
        with tempfile.TemporaryDirectory(prefix="mcp_user_") as user:
            proc = subprocess.run(
                [os.environ["BLENDER_BIN"], "--background", "--factory-startup", "--disable-autoexec",
                 "--python-exit-code", "2", "--python", str(Path(__file__).resolve()), "--", "--in-blender"],
                env={**os.environ, "BLENDER_USER_RESOURCES": user},
                capture_output=True, text=True, timeout=90,
            )
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertIn("MODDED_PROOF=", proc.stdout)
            print(proc.stdout[proc.stdout.index("MODDED_PROOF="):].splitlines()[0])


if __name__ == "__main__":
    if "--in-blender" in sys.argv:
        _proof()
    else:
        unittest.main()
