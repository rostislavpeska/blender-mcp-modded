# SPDX-License-Identifier: GPL-3.0-or-later

"""
Tool-code: import a 3D model and canonicalize it.

Downloads (if *source* is a URL) or opens a local .glb/.gltf/.obj/.fbx, joins it
into a single mesh, applies transforms, normalizes so its largest bounding-box
dimension equals *target_size*, sets the origin to the chosen pivot ('center' =
bbox centre, 'bottom' = base centre), and places it at the world origin.
"""

__all__ = (
    "Params",
    "Result",
    "main",
)

from typing import NamedTuple


class Params(NamedTuple):
    source: str                       # http(s) URL or local filesystem path
    pivot: str = "center"             # "center" | "bottom"
    target_size: float = 1.0          # largest bbox dimension after normalize
    collection_name: str = ""         # optional collection to link the object into


class Result(NamedTuple):
    status: str
    object: str | None = None
    pivot: str | None = None
    bbox_min: list | None = None
    bbox_max: list | None = None
    source: str | None = None
    message: str | None = None


def main(params: Params) -> Result:
    import os
    import tempfile
    import bpy  # pylint: disable=import-error,no-name-in-module
    from mathutils import Vector  # pylint: disable=import-error,no-name-in-module

    src = params.source
    if src.startswith(("http://", "https://")):
        import urllib.request
        path = os.path.join(tempfile.gettempdir(), "mcp_canon_import" + os.path.splitext(src.split("?")[0])[1])
        if not path.lower().endswith((".glb", ".gltf", ".obj", ".fbx")):
            path = os.path.join(tempfile.gettempdir(), "mcp_canon_import.glb")
        try:
            urllib.request.urlretrieve(src, path)
        except Exception as ex:  # pylint: disable=broad-except
            return Result(status="error", message="Download failed: %s" % ex, source=src)
    else:
        path = src
    if not os.path.exists(path):
        return Result(status="error", message="File not found: %s" % path, source=src)

    if bpy.context.object and bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    before = set(bpy.data.objects)
    ext = os.path.splitext(path)[1].lower()
    try:
        if ext in ('.glb', '.gltf'):
            bpy.ops.import_scene.gltf(filepath=path)
        elif ext == '.obj':
            bpy.ops.wm.obj_import(filepath=path)
        elif ext == '.fbx':
            bpy.ops.import_scene.fbx(filepath=path)
        else:
            return Result(status="error", message="Unsupported format: %s" % ext, source=src)
    except RuntimeError as ex:
        return Result(status="error", message="Import failed: %s" % ex, source=src)

    new = [o for o in bpy.data.objects if o not in before]
    meshes = [o for o in new if o.type == 'MESH']
    if not meshes:
        return Result(status="error", message="No mesh objects in imported file", source=src)

    # Join all imported meshes into one object.
    bpy.ops.object.select_all(action='DESELECT')
    for m in meshes:
        m.select_set(True)
    bpy.context.view_layer.objects.active = meshes[0]
    if len(meshes) > 1:
        bpy.ops.object.join()
    obj = bpy.context.view_layer.objects.active
    # Drop leftover import artifacts (e.g. the glTF root empty).
    for x in new:
        if x is not obj and x.name in bpy.data.objects and x.type == 'EMPTY' and not x.children:
            bpy.data.objects.remove(x, do_unlink=True)

    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    # Normalize scale: largest bbox dimension -> target_size.
    bpy.context.view_layer.update()
    cs = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    dim = (
        max(c.x for c in cs) - min(c.x for c in cs),
        max(c.y for c in cs) - min(c.y for c in cs),
        max(c.z for c in cs) - min(c.z for c in cs),
    )
    biggest = max(dim) or 1.0
    factor = (params.target_size or 1.0) / biggest
    obj.scale = (factor, factor, factor)
    bpy.ops.object.transform_apply(scale=True)

    # Set the origin (pivot).
    if params.pivot == "bottom":
        bpy.context.view_layer.update()
        cs = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
        cx = sum(c.x for c in cs) / 8.0
        cy = sum(c.y for c in cs) / 8.0
        mnz = min(c.z for c in cs)
        saved_cursor = tuple(bpy.context.scene.cursor.location)
        bpy.context.scene.cursor.location = (cx, cy, mnz)
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.context.scene.cursor.location = saved_cursor
    else:
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

    obj.location = (0.0, 0.0, 0.0)
    obj.rotation_euler = (0.0, 0.0, 0.0)

    # Make normals consistent (outward).
    try:
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.object.mode_set(mode='OBJECT')
    except RuntimeError:
        pass

    if params.collection_name:
        coll = bpy.data.collections.get(params.collection_name)
        if coll is None:
            coll = bpy.data.collections.new(params.collection_name)
            bpy.context.scene.collection.children.link(coll)
        for c in list(obj.users_collection):
            c.objects.unlink(obj)
        coll.objects.link(obj)

    bpy.context.view_layer.update()
    cs = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    bbox_min = [round(min(c[i] for c in cs), 4) for i in range(3)]
    bbox_max = [round(max(c[i] for c in cs), 4) for i in range(3)]
    return Result(
        status="ok", object=obj.name, pivot=params.pivot,
        bbox_min=bbox_min, bbox_max=bbox_max, source=src,
    )
