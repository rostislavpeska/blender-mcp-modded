# SPDX-License-Identifier: GPL-3.0-or-later

"""
Tool-code for placing four standardized framing cameras around the scene.

Cameras (front/right/back/left) are fitted to the combined bounds of all mesh
objects and aimed at the scene centre via a TRACK_TO constraint. They live in a
hidden collection (excluded from the viewport, kept renderable) so they never
clutter the user's working view. Read any view afterwards with
``render_viewport_to_path`` after setting it as the active scene camera.
"""

__all__ = (
    "Params",
    "Result",
    "main",
)

from typing import NamedTuple


class Params(NamedTuple):
    distance_multiplier: float = 2.5
    collection_name: str = "_mcp_standard_cameras"
    # Frame only the meshes inside this collection (and its children) when set;
    # otherwise frame every mesh in the scene.
    target_collection: str | None = None
    # Object names to exclude from the framing bounds (e.g. a huge ground/water
    # plane that would otherwise dominate the fit).
    ignore_object_names: tuple = ()


class Result(NamedTuple):
    status: str
    cameras: list[str]
    center: list[float] | None = None
    max_size: float | None = None
    distance: float | None = None
    collection: str | None = None
    message: str | None = None


def main(params: Params) -> Result:
    import bpy  # pylint: disable=import-error,no-name-in-module
    from mathutils import Vector  # pylint: disable=import-error,no-name-in-module

    coll_name = params.collection_name
    scene = bpy.context.scene

    # Gather the meshes whose bounds we frame.
    def _collect(coll):
        objs = [o for o in coll.objects if o.type == 'MESH']
        for child in coll.children:
            objs += _collect(child)
        return objs

    if params.target_collection:
        tc = bpy.data.collections.get(params.target_collection)
        if tc is None:
            return Result(status="error", cameras=[], message="No collection named %r" % params.target_collection)
        meshes = _collect(tc)
    else:
        meshes = [o for o in scene.objects if o.type == 'MESH']

    ignore = set(params.ignore_object_names or ())
    meshes = [o for o in meshes if o.name not in ignore]
    if not meshes:
        return Result(status="error", cameras=[], message="No mesh objects to frame")

    # Bounds from all evaluated mesh objects (modifiers applied).
    deps = bpy.context.evaluated_depsgraph_get()

    mn = Vector((float('inf'), float('inf'), float('inf')))
    mx = Vector((float('-inf'), float('-inf'), float('-inf')))
    for o in meshes:
        oe = o.evaluated_get(deps)
        me = oe.to_mesh()
        mw = o.matrix_world
        for v in me.vertices:
            w = mw @ v.co
            for i in range(3):
                mn[i] = min(mn[i], w[i])
                mx[i] = max(mx[i], w[i])
        oe.to_mesh_clear()

    center = (mn + mx) / 2.0
    size = mx - mn
    max_size = max(size.x, size.y, size.z) or 1.0
    distance = max_size * params.distance_multiplier
    height = distance * 0.4

    # Hidden collection (viewport-excluded, renderable). Re-created clean each call.
    coll = bpy.data.collections.get(coll_name)
    if coll is None:
        coll = bpy.data.collections.new(coll_name)
        scene.collection.children.link(coll)
    coll.hide_render = False
    for o in list(coll.objects):
        bpy.data.objects.remove(o, do_unlink=True)

    # Aim target at the scene centre.
    target = bpy.data.objects.new("_std_target", None)
    target.empty_display_size = max_size * 0.05
    target.location = center
    coll.objects.link(target)

    views = (
        ("_std_front", Vector((center.x, center.y - distance, center.z + height))),
        ("_std_right", Vector((center.x + distance, center.y, center.z + height))),
        ("_std_back", Vector((center.x, center.y + distance, center.z + height))),
        ("_std_left", Vector((center.x - distance, center.y, center.z + height))),
    )

    names: list[str] = []
    for nm, loc in views:
        cam_data = bpy.data.cameras.new(nm)
        cam = bpy.data.objects.new(nm, cam_data)
        cam.location = loc
        coll.objects.link(cam)
        con = cam.constraints.new(type='TRACK_TO')
        con.target = target
        con.track_axis = 'TRACK_NEGATIVE_Z'
        con.up_axis = 'UP_Y'
        names.append(nm)

    # Hide the rig from the viewport (still renderable).
    coll.hide_viewport = True
    layer_coll = bpy.context.view_layer.layer_collection.children.get(coll_name)
    if layer_coll is not None:
        layer_coll.hide_viewport = True

    return Result(
        status="ok",
        cameras=names,
        center=[round(center.x, 4), round(center.y, 4), round(center.z, 4)],
        max_size=round(max_size, 4),
        distance=round(distance, 4),
        collection=coll_name,
    )
