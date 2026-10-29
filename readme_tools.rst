#####
Tools
#####

The tools exposed by the MCP server.

..
   Generated from the tool doc-strings by ``make readme_update``.
   Do not edit the listing between the sentinels below by hand.

.. BEGIN TOOL LISTING

``list_blender_instances``
   List the running Blender instances that registered an MCP server, and
   which one this session uses.

``select_blender_instance``
   Choose which running Blender this MCP session talks to, by process id or
   port.

``execute_blender_code``
   Execute Python code in the connected Blender instance.

``execute_blender_code_for_cli``
   Execute Python code in a background Blender process.

``get_blendfile_summary_datablocks``
   Return a summary of the blend file: data-block counts, active workspace,
   and render engine.

``get_blendfile_summary_datablocks_for_cli``
   Return a data-block summary by opening *blend_file* in background
   Blender.

``get_blendfile_summary_missing_files``
   Report external file references that are missing from disk (images,
   libraries, fonts, sounds, movie clips, caches, sequences).

``get_blendfile_summary_missing_files_for_cli``
   Report missing file references by opening *blend_file* in background
   Blender.

``get_blendfile_summary_of_linked_libraries``
   Return a tree of directly and indirectly linked library files.

``get_blendfile_summary_of_linked_libraries_for_cli``
   Return linked-library info by opening *blend_file* in background
   Blender.

``get_blendfile_summary_path_info``
   Simple/fast access to the blend file's path, save status, age, and
   backups.

``get_blendfile_summary_path_info_for_cli``
   Return path info by opening *blend_file* in background Blender.

``get_blendfile_summary_usage_guess``
   Guess the primary use-cases of the current blend file (scored 0-100 with
   certainty).

``get_blendfile_summary_usage_guess_for_cli``
   Guess use-cases by opening *blend_file* in background Blender.

``get_object_detail_summary``
   Return a structured summary of the object identified by *name*.

``get_objects_summary``
   Return the scene's collection hierarchy and their objects.

``get_python_api_docs``
   Return the Blender Python API docs for *identifier*, or list modules
   matching a trailing-``*`` discovery pattern.

``get_screenshot_of_area_as_image``
   Take a screenshot of a single Blender area and return it as a PNG image.

``get_screenshot_of_window_as_image``
   Take a screenshot of the entire Blender window and return it as a PNG
   image.

``get_screenshot_of_window_as_json``
   Return a JSON description of the Blender window layout, areas, active
   object, and selection.

``import_canonical_model``
   Import a 3D model and canonicalize it in one step.

``jump_to_tab_by_name``
   Switch the active workspace tab to *name*.

``jump_to_tab_by_space_type``
   Switch to a workspace whose main area matches *space_type*.

``jump_to_view3d_object_by_name``
   Move the 3D viewport to focus on an object by *name*.

``jump_to_view3d_object_data_by_name``
   Move the 3D viewport to the object whose data block matches *name*.

``place_standard_cameras``
   Place four standardized framing cameras (front, right, back, left)
   around the scene, fitted to the bounds of the framed meshes and aimed at
   their centre. The cameras live in a hidden collection (excluded from the
   viewport, still renderable).

``read_standard_views``
   Render every standardized camera (placed by ``place_standard_cameras``)
   and return a single 2x2 contact-sheet image (front / right / back /
   left) so the scene can be understood from all angles in one step. Render
   settings and the active camera are restored afterwards.

``render_thumbnail_to_path``
   Render a small, low-quality thumbnail to *output_path* (temporarily
   overrides settings).

``render_viewport_to_path``
   Render the current scene to *output_path* using current render settings.

``search_api_docs``
   Full-text search over the bundled Blender Python API reference.

``search_manual_docs``
   Full-text search over the bundled Blender user manual.

``sketchfab_search``
   Search Sketchfab for 3D models (public API). Returns candidates, each
   with uid, name, a preview thumbnail_url, license, faces, downloadable
   and viewer_url. Then sketchfab_preview(thumbnail_url) to see one, and
   sketchfab_download(uid) + import_canonical_model(glb_url) to bring it
   in.

``sketchfab_preview``
   Fetch a Sketchfab model's preview thumbnail (the thumbnail_url from
   sketchfab_search) and return it as an image, so you can judge a model
   before importing it.

``sketchfab_download``
   Resolve a downloadable Sketchfab model (by uid from sketchfab_search) to
   a short-lived model URL via the gated n8n webhook (which holds the
   Sketchfab token). Returns {glb_url, is_zip}. Feed glb_url to
   import_canonical_model (it unpacks the glTF ZIP automatically).

``generate_3d``
   Start 3D generation (TRELLIS) via the n8n pipeline (async). Two modes:

``wait_for_3d_job``
   Poll a 3D generation job (from ``generate_3d``) until the model is
   ready.

.. END TOOL LISTING
