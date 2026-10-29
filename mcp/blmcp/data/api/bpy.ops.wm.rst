Wm Operators
============

.. module:: bpy.ops.wm

.. function:: append(*, filepath="", directory="", filename="", files=None, check_existing=False, filter_blender=True, filter_backup=False, filter_image=False, filter_movie=False, filter_python=False, filter_font=False, filter_sound=False, filter_text=False, filter_archive=False, filter_btx=False, filter_alembic=False, filter_usd=False, filter_obj=False, filter_volume=False, filter_folder=True, filter_blenlib=True, filemode=1, display_type='DEFAULT', sort_method='', link=False, do_reuse_local_id=False, clear_asset_data=False, autoselect=True, active_collection=True, instance_collections=False, instance_object_data=True, set_fake=False, use_recursive=True)

   Append from a Library .blend file

   :param filepath: File Path, Path to file (optional, never None)
   :type filepath: str
   :param directory: Directory, Directory of the file (optional, never None)
   :type directory: str
   :param filename: File Name, Name of the file (optional, never None)
   :type filename: str
   :param files: Files, (optional)
   :type files: :class:`bpy_prop_collection`\ [:class:`OperatorFileListElement`] | None
   :param check_existing: Check Existing, Check and warn on overwriting existing files (optional)
   :type check_existing: bool
   :param filter_blender: Filter .blend files, (optional)
   :type filter_blender: bool
   :param filter_backup: Filter backup .blend files, (optional)
   :type filter_backup: bool
   :param filter_image: Filter image files, (optional)
   :type filter_image: bool
   :param filter_movie: Filter movie files, (optional)
   :type filter_movie: bool
   :param filter_python: Filter Python files, (optional)
   :type filter_python: bool
   :param filter_font: Filter font files, (optional)
   :type filter_font: bool
   :param filter_sound: Filter sound files, (optional)
   :type filter_sound: bool
   :param filter_text: Filter text files, (optional)
   :type filter_text: bool
   :param filter_archive: Filter archive files, (optional)
   :type filter_archive: bool
   :param filter_btx: Filter btx files, (optional)
   :type filter_btx: bool
   :param filter_alembic: Filter Alembic files, (optional)
   :type filter_alembic: bool
   :param filter_usd: Filter USD files, (optional)
   :type filter_usd: bool
   :param filter_obj: Filter OBJ files, (optional)
   :type filter_obj: bool
   :param filter_volume: Filter OpenVDB volume files, (optional)
   :type filter_volume: bool
   :param filter_folder: Filter folders, (optional)
   :type filter_folder: bool
   :param filter_blenlib: Filter Blender IDs, (optional)
   :type filter_blenlib: bool
   :param filemode: File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file (in [1, 9], optional)
   :type filemode: int
   :param display_type: Display Type, (optional)

      - ``DEFAULT``
        Default -- Automatically determine display type for files.
      - ``LIST_VERTICAL``
        Short List -- Display files as short list.
      - ``LIST_HORIZONTAL``
        Long List -- Display files as a detailed list.
      - ``THUMBNAIL``
        Thumbnails -- Display files as thumbnails.
   :type display_type: Literal['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL']
   :param sort_method: File sorting mode, (optional)
   :type sort_method: str
   :param link: Link, Link the objects or data-blocks rather than appending (optional)
   :type link: bool
   :param do_reuse_local_id: Re-Use Local Data, Try to re-use previously matching appended data-blocks instead of appending a new copy (optional)
   :type do_reuse_local_id: bool
   :param clear_asset_data: Clear Asset Data, Don't add asset meta-data or tags from the original data-block (optional)
   :type clear_asset_data: bool
   :param autoselect: Select, Select new objects (optional)
   :type autoselect: bool
   :param active_collection: Active Collection, Put new objects on the active collection (optional)
   :type active_collection: bool
   :param instance_collections: Instance Collections, Create instances for collections, rather than adding them directly to the scene (optional)
   :type instance_collections: bool
   :param instance_object_data: Instance Object Data, Create instances for object data which are not referenced by any objects (optional)
   :type instance_object_data: bool
   :param set_fake: Fake User, Set "Fake User" for appended items (except objects and collections) (optional)
   :type set_fake: bool
   :param use_recursive: Localize All, Localize all appended data, including those indirectly linked from other libraries (optional)
   :type use_recursive: bool
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]

.. function:: batch_rename(*, data_type='OBJECT', data_source='SELECT', actions=None)

   Rename multiple items at once

   :param data_type: Type, Type of data to rename (optional)
   :type data_type: Literal['OBJECT', 'COLLECTION', 'MATERIAL', 'MESH', 'CURVE', 'META', 'VOLUME', 'GREASEPENCIL', 'ARMATURE', 'LATTICE', 'LIGHT', 'LIGHT_PROBE', 'CAMERA', 'SPEAKER', 'BONE', 'NODE', 'SEQUENCE_STRIP', 'ACTION_CLIP', 'SCENE', 'BRUSH']
   :param data_source: Source, (optional)
   :type data_source: Literal['SELECT', 'ALL']
   :param actions: actions, (optional)
   :type actions: :class:`bpy_prop_collection`\ [:class:`BatchRenameAction`] | None
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/wm.py\:3315 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L3315>`__


.. function:: blend_strings_utf8_validate()

   Check and fix all strings in current .blend file to be valid UTF-8 Unicode (needed for some old, 2.4x area files)

   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/file.py\:289 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/file.py#L289>`__

.. function:: call_asset_shelf_popover(*, name="")

   Open a predefined asset shelf in a popup

   :param name: Asset Shelf Name, Identifier of the asset shelf to display (optional, never None)
   :type name: str
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]

.. function:: call_menu(*, name="")

   Open a predefined menu

   :param name: Name, Name of the menu (optional, never None)
   :type name: str
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]

.. function:: call_menu_pie(*, name="")

   Open a predefined pie menu

   :param name: Name, Name of the pie menu (optional, never None)
   :type name: str
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]

.. function:: call_panel(*, name="", keep_open=True)

   Open a predefined panel

   :param name: Name, Name of the menu (optional, never None)
   :type name: str
   :param keep_open: Keep Open, (optional)
   :type keep_open: bool
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]

.. function:: clear_recent_files(*, remove='ALL')

   Clear the recent files list

   :param remove: Remove, (optional)
   :type remove: Literal['ALL', 'MISSING']
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]

.. function:: collection_export_all()

   Invoke all configured exporters for all collections

   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
.. function:: context_collection_boolean_set(*, data_path_iter="", data_path_item="", type='TOGGLE')

   Set boolean values for a collection of items

   :param data_path_iter: data_path_iter, The data path relative to the context, must point to an iterable (optional, never None)
   :type data_path_iter: str
   :param data_path_item: data_path_item, The data path from each iterable to the value (int or float) (optional, never None)
   :type data_path_item: str
   :param type: Type, (optional)
   :type type: Literal['TOGGLE', 'ENABLE', 'DISABLE']
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/wm.py\:875 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L875>`__


.. function:: context_cycle_array(*, data_path="", reverse=False)

   Set a context array value (useful for cycling the active mesh edit mode)

   :param data_path: Context Attributes, Context data-path (expanded using visible windows in the current .blend file) (optional, never None)
   :type data_path: str
   :param reverse: Reverse, Cycle backwards (optional)
   :type reverse: bool
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/wm.py\:673 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L673>`__


.. function:: context_cycle_enum(*, data_path="", reverse=False, wrap=False)

   Toggle a context value

   :param data_path: Context Attributes, Context data-path (expanded using visible windows in the current .blend file) (optional, never None)
   :type data_path: str
   :param reverse: Reverse, Cycle backwards (optional)
   :type reverse: bool
   :param wrap: Wrap, Wrap back to the first/last values (optional)
   :type wrap: bool
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/wm.py\:624 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L624>`__


.. function:: context_cycle_int(*, data_path="", reverse=False, wrap=False)

   Set a context value (useful for cycling active material, shape keys, groups, etc.)

   :param data_path: Context Attributes, Context data-path (expanded using visible windows in the current .blend file) (optional, never None)
   :type data_path: str
   :param reverse: Reverse, Cycle backwards (optional)
   :type reverse: bool
   :param wrap: Wrap, Wrap back to the first/last values (optional)
   :type wrap: bool
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/wm.py\:584 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L584>`__


.. function:: context_menu_enum(*, data_path="")

   Undocumented, consider `contributing <https://developer.blender.org/>`__.

   :param data_path: Context Attributes, Context data-path (expanded using visible windows in the current .blend file) (optional, never None)
   :type data_path: str
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/wm.py\:703 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L703>`__


.. function:: context_modal_mouse(*, data_path_iter="", data_path_item="", header_text="", input_scale=0.01, invert=False, initial_x=0)

   Adjust arbitrary values with mouse input

   :param data_path_iter: data_path_iter, The data path relative to the context, must point to an iterable (optional, never None)
   :type data_path_iter: str
   :param data_path_item: data_path_item, The data path from each iterable to the value (int or float) (optional, never None)
   :type data_path_item: str
   :param header_text: Header Text, Text to display in header during scale (optional, never None)
   :type header_text: str
   :param input_scale: input_scale, Scale the mouse movement by this value before applying the delta (in [-inf, inf], optional)
   :type input_scale: float
   :param invert: invert, Invert the mouse input (optional)
   :type invert: bool
   :param initial_x: initial_x, (in [-inf, inf], optional)
   :type initial_x: int
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/wm.py\:1023 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L1023>`__


.. function:: context_pie_enum(*, data_path="")

   Undocumented, consider `contributing <https://developer.blender.org/>`__.

   :param data_path: Context Attributes, Context data-path (expanded using visible windows in the current .blend file) (optional, never None)
   :type data_path: str
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/wm.py\:735 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L735>`__


.. function:: context_scale_float(*, data_path="", value=1.0)

   Scale a float context value

   :param data_path: Context Attributes, Context data-path (expanded using visible windows in the current .blend file) (optional, never None)
   :type data_path: str
   :param value: Value, Assign value (in [-inf, inf], optional)
   :type value: float
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/wm.py\:338 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L338>`__


.. function:: context_scale_int(*, data_path="", value=1.0, always_step=True)

   Scale an int context value

   :param data_path: Context Attributes, Context data-path (expanded using visible windows in the current .blend file) (optional, never None)
   :type data_path: str
   :param value: Value, Assign value (in [-inf, inf], optional)
   :type value: float
   :param always_step: Always Step, Always adjust the value by a minimum of 1 when 'value' is not 1.0 (optional)
   :type always_step: bool
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/wm.py\:376 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L376>`__


.. function:: context_set_boolean(*, data_path="", value=True)

   Set a context value

   :param data_path: Context Attributes, Context data-path (expanded using visible windows in the current .blend file) (optional, never None)
   :type data_path: str
   :param value: Value, Assignment value (optional)
   :type value: bool
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/wm.py\:267 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L267>`__


.. function:: context_set_enum(*, data_path="", value="")

   Set a context value

   :param data_path: Context Attributes, Context data-path (expanded using visible windows in the current .blend file) (optional, never None)
   :type data_path: str
   :param value: Value, Assignment value (as a string) (optional, never None)
   :type value: str
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/wm.py\:267 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L267>`__


.. function:: context_set_float(*, data_path="", value=0.0, relative=False)

   Set a context value

   :param data_path: Context Attributes, Context data-path (expanded using visible windows in the current .blend file) (optional, never None)
   :type data_path: str
   :param value: Value, Assignment value (in [-inf, inf], optional)
   :type value: float
   :param relative: Relative, Apply relative to the current value (delta) (optional)
   :type relative: bool
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/wm.py\:267 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L267>`__


.. function:: context_set_id(*, data_path="", value="")

   Set a context value to an ID data-block

   :param data_path: Context Attributes, Context data-path (expanded using visible windows in the current .blend file) (optional, never None)
   :type data_path: str
   :param value: Value, Assign value (optional, never None)
   :type value: str
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/wm.py\:817 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L817>`__


.. function:: context_set_int(*, data_path="", value=0, relative=False)

   Set a context value

   :param data_path: Context Attributes, Context data-path (expanded using visible windows in the current .blend file) (optional, never None)
   :type data_path: str
   :param value: Value, Assign value (in [-inf, inf], optional)
   :type value: int
   :param relative: Relative, Apply relative to the current value (delta) (optional)
   :type relative: bool
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/wm.py\:267 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L267>`__


.. function:: context_set_string(*, data_path="", value="")

   Set a context value

   :param data_path: Context Attributes, Context data-path (expanded using visible windows in the current .blend file) (optional, never None)
   :type data_path: str
   :param value: Value, Assign value (optional, never None)
   :type value: str
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/wm.py\:267 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L267>`__


.. function:: context_set_value(*, data_path="", value="")

   Set a context value

   :param data_path: Context Attributes, Context data-path (expanded using visible windows in the current .blend file) (optional, never None)
   :type data_path: str
   :param value: Value, Assignment value (as a string) (optional, never None)
   :type value: str
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/wm.py\:480 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L480>`__


.. function:: context_toggle(*, data_path="", module="")

   Toggle a context value

   :param data_path: Context Attributes, Context data-path (expanded using visible windows in the current .blend file) (optional, never None)
   :type data_path: str
   :param module: Module, Optionally override the context with a module (optional, never None)
   :type module: str
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/wm.py\:504 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L504>`__


.. function:: context_toggle_enum(*, data_path="", value_1="", value_2="")

   Toggle a context value

   :param data_path: Context Attributes, Context data-path (expanded using visible windows in the current .blend file) (optional, never None)
   :type data_path: str
   :param value_1: Value, Toggle enum (optional, never None)
   :type value_1: str
   :param value_2: Value, Toggle enum (optional, never None)
   :type value_2: str
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/wm.py\:545 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L545>`__


.. function:: debug_menu(*, debug_value=0)

   Open a popup to set the debug level

   :param debug_value: Debug Value, (in [-32768, 32767], optional)
   :type debug_value: int
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]

.. function:: doc_view(*, doc_id="")

   Open online reference docs in a web browser

   :param doc_id: Doc ID, (optional, never None)
   :type doc_id: str
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/wm.py\:1379 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L1379>`__


.. function:: doc_view_manual(*, doc_id="")

   Load online manual

   :param doc_id: Doc ID, (optional, never None)
   :type doc_id: str
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/wm.py\:1352 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L1352>`__


.. function:: doc_view_manual_ui_context()

   View a context based online manual in a web browser

   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
.. function:: drop_blend_file(*, filepath="")

   Undocumented, consider `contributing <https://developer.blender.org/>`__.

   :param filepath: filepath, (optional, never None)
   :type filepath: str
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/wm.py\:3690 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L3690>`__


.. function:: drop_import_file(*, directory="", files=None)

   Operator that allows file handlers to receive file drops

   :param directory: Directory, Directory of the file (optional, never None)
   :type directory: str
   :param files: Files, (optional)
   :type files: :class:`bpy_prop_collection`\ [:class:`OperatorFileListElement`] | None
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]

.. function:: id_linked_relocate(*, id_session_uid=0, filepath="", directory="", filename="", check_existing=False, filter_blender=True, filter_backup=False, filter_image=False, filter_movie=False, filter_python=False, filter_font=False, filter_sound=False, filter_text=False, filter_archive=False, filter_btx=False, filter_alembic=False, filter_usd=False, filter_obj=False, filter_volume=False, filter_folder=True, filter_blenlib=True, filemode=1, relative_path=True, display_type='DEFAULT', sort_method='', link=True, do_reuse_local_id=False, clear_asset_data=False, autoselect=True, active_collection=False, instance_collections=False, instance_object_data=False)

   Relocate a linked ID, i.e. select another ID to link, and remap its local usages to that newly linked data-block). Currently only designed as an internal operator, not directly exposed to the user

   :param id_session_uid: Linked ID Session UID, Unique runtime identifier for the linked ID to relocate (in [0, inf], optional)
   :type id_session_uid: int
   :param filepath: File Path, Path to file (optional, never None)
   :type filepath: str
   :param directory: Directory, Directory of the file (optional, never None)
   :type directory: str
   :param filename: File Name, Name of the file (optional, never None)
   :type filename: str
   :param check_existing: Check Existing, Check and warn on overwriting existing files (optional)
   :type check_existing: bool
   :param filter_blender: Filter .blend files, (optional)
   :type filter_blender: bool
   :param filter_backup: Filter backup .blend files, (optional)
   :type filter_backup: bool
   :param filter_image: Filter image files, (optional)
   :type filter_image: bool
   :param filter_movie: Filter movie files, (optional)
   :type filter_movie: bool
   :param filter_python: Filter Python files, (optional)
   :type filter_python: bool
   :param filter_font: Filter font files, (optional)
   :type filter_font: bool
   :param filter_sound: Filter sound files, (optional)
   :type filter_sound: bool
   :param filter_text: Filter text files, (optional)
   :type filter_text: bool
   :param filter_archive: Filter archive files, (optional)
   :type filter_archive: bool
   :param filter_btx: Filter btx files, (optional)
   :type filter_btx: bool
   :param filter_alembic: Filter Alembic files, (optional)
   :type filter_alembic: bool
   :param filter_usd: Filter USD files, (optional)
   :type filter_usd: bool
   :param filter_obj: Filter OBJ files, (optional)
   :type filter_obj: bool
   :param filter_volume: Filter OpenVDB volume files, (optional)
   :type filter_volume: bool
   :param filter_folder: Filter folders, (optional)
   :type filter_folder: bool
   :param filter_blenlib: Filter Blender IDs, (optional)
   :type filter_blenlib: bool
   :param filemode: File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file (in [1, 9], optional)
   :type filemode: int
   :param relative_path: Relative Path, Select the file relative to the blend file (optional)
   :type relative_path: bool
   :param display_type: Display Type, (optional)

      - ``DEFAULT``
        Default -- Automatically determine display type for files.
      - ``LIST_VERTICAL``
        Short List -- Display files as short list.
      - ``LIST_HORIZONTAL``
        Long List -- Display files as a detailed list.
      - ``THUMBNAIL``
        Thumbnails -- Display files as thumbnails.
   :type display_type: Literal['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL']
   :param sort_method: File sorting mode, (optional)
   :type sort_method: str
   :param link: Link, Link the objects or data-blocks rather than appending (optional)
   :type link: bool
   :param do_reuse_local_id: Re-Use Local Data, Try to re-use previously matching appended data-blocks instead of appending a new copy (optional)
   :type do_reuse_local_id: bool
   :param clear_asset_data: Clear Asset Data, Don't add asset meta-data or tags from the original data-block (optional)
   :type clear_asset_data: bool
   :param autoselect: Select, Select new objects (optional)
   :type autoselect: bool
   :param active_collection: Active Collection, Put new objects on the active collection (optional)
   :type active_collection: bool
   :param instance_collections: Instance Collections, Create instances for collections, rather than adding them directly to the scene (optional)
   :type instance_collections: bool
   :param instance_object_data: Instance Object Data, Create instances for object data which are not referenced by any objects (optional)
   :type instance_object_data: bool
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]

.. function:: interface_theme_preset_add(*, name="", remove_name=False, remove_active=False)

   Add a custom theme to the preset list

   :param name: Name, Name of the preset, used to make the path name (optional, never None)
   :type name: str
   :param remove_name: remove_name, (optional)
   :type remove_name: bool
   :param remove_active: remove_active, (optional)
   :type remove_active: bool
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/presets.py\:119 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/presets.py#L119>`__


.. function:: interface_theme_preset_remove(*, name="", remove_name=False, remove_active=True)

   Remove a custom theme from the preset list

   :param name: Name, Name of the preset, used to make the path name (optional, never None)
   :type name: str
   :param remove_name: remove_name, (optional)
   :type remove_name: bool
   :param remove_active: remove_active, (optional)
   :type remove_active: bool
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/presets.py\:119 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/presets.py#L119>`__


.. function:: interface_theme_preset_save(*, name="", remove_name=False, remove_active=True)

   Save a custom theme in the preset list

   :param name: Name, Name of the preset, used to make the path name (optional, never None)
   :type name: str
   :param remove_name: remove_name, (optional)
   :type remove_name: bool
   :param remove_active: remove_active, (optional)
   :type remove_active: bool
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/presets.py\:754 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/presets.py#L754>`__


.. function:: keyconfig_preset_add(*, name="", remove_name=False, remove_active=False)

   Add a custom keymap configuration to the preset list

   :param name: Name, Name of the preset, used to make the path name (optional, never None)
   :type name: str
   :param remove_name: remove_name, (optional)
   :type remove_name: bool
   :param remove_active: remove_active, (optional)
   :type remove_active: bool
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/presets.py\:119 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/presets.py#L119>`__


.. function:: keyconfig_preset_remove(*, name="", remove_name=False, remove_active=True)

   Remove a custom keymap configuration from the preset list

   :param name: Name, Name of the preset, used to make the path name (optional, never None)
   :type name: str
   :param remove_name: remove_name, (optional)
   :type remove_name: bool
   :param remove_active: remove_active, (optional)
   :type remove_active: bool
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/presets.py\:119 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/presets.py#L119>`__


.. function:: lib_reload(*, library="", filepath="", directory="", filename="", hide_props_region=True, check_existing=False, filter_blender=True, filter_backup=False, filter_image=False, filter_movie=False, filter_python=False, filter_font=False, filter_sound=False, filter_text=False, filter_archive=False, filter_btx=False, filter_alembic=False, filter_usd=False, filter_obj=False, filter_volume=False, filter_folder=True, filter_blenlib=False, filemode=8, relative_path=True, display_type='DEFAULT', sort_method='')

   Reload the given library

   :param library: Library, Library to reload (optional, never None)
   :type library: str
   :param filepath: File Path, Path to file (optional, never None)
   :type filepath: str
   :param directory: Directory, Directory of the file (optional, never None)
   :type directory: str
   :param filename: File Name, Name of the file (optional, never None)
   :type filename: str
   :param hide_props_region: Hide Operator Properties, Collapse the region displaying the operator settings (optional)
   :type hide_props_region: bool
   :param check_existing: Check Existing, Check and warn on overwriting existing files (optional)
   :type check_existing: bool
   :param filter_blender: Filter .blend files, (optional)
   :type filter_blender: bool
   :param filter_backup: Filter backup .blend files, (optional)
   :type filter_backup: bool
   :param filter_image: Filter image files, (optional)
   :type filter_image: bool
   :param filter_movie: Filter movie files, (optional)
   :type filter_movie: bool
   :param filter_python: Filter Python files, (optional)
   :type filter_python: bool
   :param filter_font: Filter font files, (optional)
   :type filter_font: bool
   :param filter_sound: Filter sound files, (optional)
   :type filter_sound: bool
   :param filter_text: Filter text files, (optional)
   :type filter_text: bool
   :param filter_archive: Filter archive files, (optional)
   :type filter_archive: bool
   :param filter_btx: Filter btx files, (optional)
   :type filter_btx: bool
   :param filter_alembic: Filter Alembic files, (optional)
   :type filter_alembic: bool
   :param filter_usd: Filter USD files, (optional)
   :type filter_usd: bool
   :param filter_obj: Filter OBJ files, (optional)
   :type filter_obj: bool
   :param filter_volume: Filter OpenVDB volume files, (optional)
   :type filter_volume: bool
   :param filter_folder: Filter folders, (optional)
   :type filter_folder: bool
   :param filter_blenlib: Filter Blender IDs, (optional)
   :type filter_blenlib: bool
   :param filemode: File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file (in [1, 9], optional)
   :type filemode: int
   :param relative_path: Relative Path, Select the file relative to the blend file (optional)
   :type relative_path: bool
   :param display_type: Display Type, (optional)

      - ``DEFAULT``
        Default -- Automatically determine display type for files.
      - ``LIST_VERTICAL``
        Short List -- Display files as short list.
      - ``LIST_HORIZONTAL``
        Long List -- Display files as a detailed list.
      - ``THUMBNAIL``
        Thumbnails -- Display files as thumbnails.
   :type display_type: Literal['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL']
   :param sort_method: File sorting mode, (optional)
   :type sort_method: str
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]

.. function:: lib_relocate(*, library="", filepath="", directory="", filename="", files=None, hide_props_region=True, check_existing=False, filter_blender=True, filter_backup=False, filter_image=False, filter_movie=False, filter_python=False, filter_font=False, filter_sound=False, filter_text=False, filter_archive=False, filter_btx=False, filter_alembic=False, filter_usd=False, filter_obj=False, filter_volume=False, filter_folder=True, filter_blenlib=False, filemode=8, relative_path=True, display_type='DEFAULT', sort_method='')

   Relocate the given library to one or several others

   :param library: Library, Library to relocate (optional, never None)
   :type library: str
   :param filepath: File Path, Path to file (optional, never None)
   :type filepath: str
   :param directory: Directory, Directory of the file (optional, never None)
   :type directory: str
   :param filename: File Name, Name of the file (optional, never None)
   :type filename: str
   :param files: Files, (optional)
   :type files: :class:`bpy_prop_collection`\ [:class:`OperatorFileListElement`] | None
   :param hide_props_region: Hide Operator Properties, Collapse the region displaying the operator settings (optional)
   :type hide_props_region: bool
   :param check_existing: Check Existing, Check and warn on overwriting existing files (optional)
   :type check_existing: bool
   :param filter_blender: Filter .blend files, (optional)
   :type filter_blender: bool
   :param filter_backup: Filter backup .blend files, (optional)
   :type filter_backup: bool
   :param filter_image: Filter image files, (optional)
   :type filter_image: bool
   :param filter_movie: Filter movie files, (optional)
   :type filter_movie: bool
   :param filter_python: Filter Python files, (optional)
   :type filter_python: bool
   :param filter_font: Filter font files, (optional)
   :type filter_font: bool
   :param filter_sound: Filter sound files, (optional)
   :type filter_sound: bool
   :param filter_text: Filter text files, (optional)
   :type filter_text: bool
   :param filter_archive: Filter archive files, (optional)
   :type filter_archive: bool
   :param filter_btx: Filter btx files, (optional)
   :type filter_btx: bool
   :param filter_alembic: Filter Alembic files, (optional)
   :type filter_alembic: bool
   :param filter_usd: Filter USD files, (optional)
   :type filter_usd: bool
   :param filter_obj: Filter OBJ files, (optional)
   :type filter_obj: bool
   :param filter_volume: Filter OpenVDB volume files, (optional)
   :type filter_volume: bool
   :param filter_folder: Filter folders, (optional)
   :type filter_folder: bool
   :param filter_blenlib: Filter Blender IDs, (optional)
   :type filter_blenlib: bool
   :param filemode: File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file (in [1, 9], optional)
   :type filemode: int
   :param relative_path: Relative Path, Select the file relative to the blend file (optional)
   :type relative_path: bool
   :param display_type: Display Type, (optional)

      - ``DEFAULT``
        Default -- Automatically determine display type for files.
      - ``LIST_VERTICAL``
        Short List -- Display files as short list.
      - ``LIST_HORIZONTAL``
        Long List -- Display files as a detailed list.
      - ``THUMBNAIL``
        Thumbnails -- Display files as thumbnails.
   :type display_type: Literal['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL']
   :param sort_method: File sorting mode, (optional)
   :type sort_method: str
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]

.. function:: link(*, filepath="", directory="", filename="", files=None, check_existing=False, filter_blender=True, filter_backup=False, filter_image=False, filter_movie=False, filter_python=False, filter_font=False, filter_sound=False, filter_text=False, filter_archive=False, filter_btx=False, filter_alembic=False, filter_usd=False, filter_obj=False, filter_volume=False, filter_folder=True, filter_blenlib=True, filemode=1, relative_path=True, display_type='DEFAULT', sort_method='', link=True, do_reuse_local_id=False, clear_asset_data=False, autoselect=True, active_collection=True, instance_collections=True, instance_object_data=True)

   Link from a Library .blend file

   :param filepath: File Path, Path to file (optional, never None)
   :type filepath: str
   :param directory: Directory, Directory of the file (optional, never None)
   :type directory: str
   :param filename: File Name, Name of the file (optional, never None)
   :type filename: str
   :param files: Files, (optional)
   :type files: :class:`bpy_prop_collection`\ [:class:`OperatorFileListElement`] | None
   :param check_existing: Check Existing, Check and warn on overwriting existing files (optional)
   :type check_existing: bool
   :param filter_blender: Filter .blend files, (optional)
   :type filter_blender: bool
   :param filter_backup: Filter backup .blend files, (optional)
   :type filter_backup: bool
   :param filter_image: Filter image files, (optional)
   :type filter_image: bool
   :param filter_movie: Filter movie files, (optional)
   :type filter_movie: bool
   :param filter_python: Filter Python files, (optional)
   :type filter_python: bool
   :param filter_font: Filter font files, (optional)
   :type filter_font: bool
   :param filter_sound: Filter sound files, (optional)
   :type filter_sound: bool
   :param filter_text: Filter text files, (optional)
   :type filter_text: bool
   :param filter_archive: Filter archive files, (optional)
   :type filter_archive: bool
   :param filter_btx: Filter btx files, (optional)
   :type filter_btx: bool
   :param filter_alembic: Filter Alembic files, (optional)
   :type filter_alembic: bool
   :param filter_usd: Filter USD files, (optional)
   :type filter_usd: bool
   :param filter_obj: Filter OBJ files, (optional)
   :type filter_obj: bool
   :param filter_volume: Filter OpenVDB volume files, (optional)
   :type filter_volume: bool
   :param filter_folder: Filter folders, (optional)
   :type filter_folder: bool
   :param filter_blenlib: Filter Blender IDs, (optional)
   :type filter_blenlib: bool
   :param filemode: File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file (in [1, 9], optional)
   :type filemode: int
   :param relative_path: Relative Path, Select the file relative to the blend file (optional)
   :type relative_path: bool
   :param display_type: Display Type, (optional)

      - ``DEFAULT``
        Default -- Automatically determine display type for files.
      - ``LIST_VERTICAL``
        Short List -- Display files as short list.
      - ``LIST_HORIZONTAL``
        Long List -- Display files as a detailed list.
      - ``THUMBNAIL``
        Thumbnails -- Display files as thumbnails.
   :type display_type: Literal['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL']
   :param sort_method: File sorting mode, (optional)
   :type sort_method: str
   :param link: Link, Link the objects or data-blocks rather than appending (optional)
   :type link: bool
   :param do_reuse_local_id: Re-Use Local Data, Try to re-use previously matching appended data-blocks instead of appending a new copy (optional)
   :type do_reuse_local_id: bool
   :param clear_asset_data: Clear Asset Data, Don't add asset meta-data or tags from the original data-block (optional)
   :type clear_asset_data: bool
   :param autoselect: Select, Select new objects (optional)
   :type autoselect: bool
   :param active_collection: Active Collection, Put new objects on the active collection (optional)
   :type active_collection: bool
   :param instance_collections: Instance Collections, Create instances for collections, rather than adding them directly to the scene (optional)
   :type instance_collections: bool
   :param instance_object_data: Instance Object Data, Create instances for object data which are not referenced by any objects (optional)
   :type instance_object_data: bool
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]

.. function:: memory_statistics()

   Print memory statistics to the console

   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
.. function:: obj_export(*, filepath="", check_existing=True, filter_blender=False, filter_backup=False, filter_image=False, filter_movie=False, filter_python=False, filter_font=False, filter_sound=False, filter_text=False, filter_archive=False, filter_btx=False, filter_alembic=False, filter_usd=False, filter_obj=False, filter_volume=False, filter_folder=True, filter_blenlib=False, filemode=8, display_type='DEFAULT', sort_method='', export_animation=False, start_frame=-2147483648, end_frame=2147483647, forward_axis='NEGATIVE_Z', up_axis='Y', global_scale=1.0, apply_modifiers=True, apply_transform=True, export_eval_mode='DAG_EVAL_VIEWPORT', export_selected_objects=False, export_uv=True, export_normals=True, export_colors=False, export_materials=True, export_pbr_extensions=False, path_mode='AUTO', export_triangulated_mesh=False, export_curves_as_nurbs=False, export_object_groups=False, export_material_groups=False, export_vertex_groups=False, export_smooth_groups=False, smooth_group_bitflags=False, filter_glob="*.obj;*.mtl", collection="")

   Save the scene to a Wavefront OBJ file

   :param filepath: File Path, Path to file (optional, never None)
   :type filepath: str
   :param check_existing: Check Existing, Check and warn on overwriting existing files (optional)
   :type check_existing: bool
   :param filter_blender: Filter .blend files, (optional)
   :type filter_blender: bool
   :param filter_backup: Filter backup .blend files, (optional)
   :type filter_backup: bool
   :param filter_image: Filter image files, (optional)
   :type filter_image: bool
   :param filter_movie: Filter movie files, (optional)
   :type filter_movie: bool
   :param filter_python: Filter Python files, (optional)
   :type filter_python: bool
   :param filter_font: Filter font files, (optional)
   :type filter_font: bool
   :param filter_sound: Filter sound files, (optional)
   :type filter_sound: bool
   :param filter_text: Filter text files, (optional)
   :type filter_text: bool
   :param filter_archive: Filter archive files, (optional)
   :type filter_archive: bool
   :param filter_btx: Filter btx files, (optional)
   :type filter_btx: bool
   :param filter_alembic: Filter Alembic files, (optional)
   :type filter_alembic: bool
   :param filter_usd: Filter USD files, (optional)
   :type filter_usd: bool
   :param filter_obj: Filter OBJ files, (optional)
   :type filter_obj: bool
   :param filter_volume: Filter OpenVDB volume files, (optional)
   :type filter_volume: bool
   :param filter_folder: Filter folders, (optional)
   :type filter_folder: bool
   :param filter_blenlib: Filter Blender IDs, (optional)
   :type filter_blenlib: bool
   :param filemode: File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file (in [1, 9], optional)
   :type filemode: int
   :param display_type: Display Type, (optional)

      - ``DEFAULT``
        Default -- Automatically determine display type for files.
      - ``LIST_VERTICAL``
        Short List -- Display files as short list.
      - ``LIST_HORIZONTAL``
        Long List -- Display files as a detailed list.
      - ``THUMBNAIL``
        Thumbnails -- Display files as thumbnails.
   :type display_type: Literal['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL']
   :param sort_method: File sorting mode, (optional)
   :type sort_method: str
   :param export_animation: Export Animation, Export multiple frames instead of the current frame only (optional)
   :type export_animation: bool
   :param start_frame: Start Frame, The first frame to be exported (in [-inf, inf], optional)
   :type start_frame: int
   :param end_frame: End Frame, The last frame to be exported (in [-inf, inf], optional)
   :type end_frame: int
   :param forward_axis: Forward Axis, (optional)

      - ``X``
        X -- Positive X axis.
      - ``Y``
        Y -- Positive Y axis.
      - ``Z``
        Z -- Positive Z axis.
      - ``NEGATIVE_X``
        -X -- Negative X axis.
      - ``NEGATIVE_Y``
        -Y -- Negative Y axis.
      - ``NEGATIVE_Z``
        -Z -- Negative Z axis.
   :type forward_axis: Literal['X', 'Y', 'Z', 'NEGATIVE_X', 'NEGATIVE_Y', 'NEGATIVE_Z']
   :param up_axis: Up Axis, (optional)

      - ``X``
        X -- Positive X axis.
      - ``Y``
        Y -- Positive Y axis.
      - ``Z``
        Z -- Positive Z axis.
      - ``NEGATIVE_X``
        -X -- Negative X axis.
      - ``NEGATIVE_Y``
        -Y -- Negative Y axis.
      - ``NEGATIVE_Z``
        -Z -- Negative Z axis.
   :type up_axis: Literal['X', 'Y', 'Z', 'NEGATIVE_X', 'NEGATIVE_Y', 'NEGATIVE_Z']
   :param global_scale: Scale, Value by which to enlarge or shrink the objects with respect to the world's origin (in [0.0001, 10000], optional)
   :type global_scale: float
   :param apply_modifiers: Apply Modifiers, Apply modifiers to exported meshes (optional)
   :type apply_modifiers: bool
   :param apply_transform: Apply Transform, Apply object transforms to exported vertices (optional)
   :type apply_transform: bool
   :param export_eval_mode: Object Properties, Determines properties like object visibility, modifiers etc., where they differ for Render and Viewport (optional)

      - ``DAG_EVAL_RENDER``
        Render -- Export objects as they appear in render.
      - ``DAG_EVAL_VIEWPORT``
        Viewport -- Export objects as they appear in the viewport.
   :type export_eval_mode: Literal['DAG_EVAL_RENDER', 'DAG_EVAL_VIEWPORT']
   :param export_selected_objects: Export Selected Objects, Export only selected objects instead of all supported objects (optional)
   :type export_selected_objects: bool
   :param export_uv: Export UVs, (optional)
   :type export_uv: bool
   :param export_normals: Export Normals, Export per-face normals if the face is flat-shaded, per-face-corner normals if smooth-shaded (optional)
   :type export_normals: bool
   :param export_colors: Export Colors, Export per-vertex colors (optional)
   :type export_colors: bool
   :param export_materials: Export Materials, Export MTL library. There must be a Principled-BSDF node for image textures to be exported to the MTL file (optional)
   :type export_materials: bool
   :param export_pbr_extensions: Export Materials with PBR Extensions, Export MTL library using PBR extensions (roughness, metallic, sheen, coat, anisotropy, transmission) (optional)
   :type export_pbr_extensions: bool
   :param path_mode: Path Mode, Method used to reference paths (optional)

      - ``AUTO``
        Auto -- Use relative paths with subdirectories only.
      - ``ABSOLUTE``
        Absolute -- Always write absolute paths.
      - ``RELATIVE``
        Relative -- Write relative paths where possible.
      - ``MATCH``
        Match -- Match absolute/relative setting with input path.
      - ``STRIP``
        Strip -- Write filename only.
      - ``COPY``
        Copy -- Copy the file to the destination path.
   :type path_mode: Literal['AUTO', 'ABSOLUTE', 'RELATIVE', 'MATCH', 'STRIP', 'COPY']
   :param export_triangulated_mesh: Export Triangulated Mesh, All ngons with four or more vertices will be triangulated. Meshes in the scene will not be affected. Behaves like Triangulate Modifier with ngon-method: "Beauty", quad-method: "Shortest Diagonal", min vertices: 4 (optional)
   :type export_triangulated_mesh: bool
   :param export_curves_as_nurbs: Export Curves as NURBS, Export curves in parametric form instead of exporting as mesh (optional)
   :type export_curves_as_nurbs: bool
   :param export_object_groups: Export Object Groups, Append mesh name to object name, separated by a '_' (optional)
   :type export_object_groups: bool
   :param export_material_groups: Export Material Groups, Generate an OBJ group for each part of a geometry using a different material (optional)
   :type export_material_groups: bool
   :param export_vertex_groups: Export Vertex Groups, Export the name of the vertex group of a face. It is approximated by choosing the vertex group with the most members among the vertices of a face (optional)
   :type export_vertex_groups: bool
   :param export_smooth_groups: Export Smooth Groups, Generate smooth groups identifiers for each group of smooth faces, as unique integer values by default (optional)
   :type export_smooth_groups: bool
   :param smooth_group_bitflags: Bitflags Smooth Groups, If exporting smoothgroups, generate 'bitflags' values for the groups, instead of unique integer values. The same bitflag value can be re-used for different groups of smooth faces, as long as they have no common sharp edges or vertices (optional)
   :type smooth_group_bitflags: bool
   :param filter_glob: Extension Filter, (optional, never None)
   :type filter_glob: str
   :param collection: Collection, (optional, never None)
   :type collection: str
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]

.. function:: obj_import(*, filepath="", directory="", files=None, check_existing=False, filter_blender=False, filter_backup=False, filter_image=False, filter_movie=False, filter_python=False, filter_font=False, filter_sound=False, filter_text=False, filter_archive=False, filter_btx=False, filter_alembic=False, filter_usd=False, filter_obj=False, filter_volume=False, filter_folder=True, filter_blenlib=False, filemode=8, display_type='DEFAULT', sort_method='', global_scale=1.0, clamp_size=0.0, forward_axis='NEGATIVE_Z', up_axis='Y', use_split_objects=True, use_split_groups=False, import_vertex_groups=False, validate_meshes=True, close_spline_loops=True, collection_separator="", mtl_name_collision_mode='MAKE_UNIQUE', filter_glob="*.obj;*.mtl")

   Load a Wavefront OBJ scene

   :param filepath: File Path, Path to file (optional, never None)
   :type filepath: str
   :param directory: Directory, Directory of the file (optional, never None)
   :type directory: str
   :param files: Files, (optional)
   :type files: :class:`bpy_prop_collection`\ [:class:`OperatorFileListElement`] | None
   :param check_existing: Check Existing, Check and warn on overwriting existing files (optional)
   :type check_existing: bool
   :param filter_blender: Filter .blend files, (optional)
   :type filter_blender: bool
   :param filter_backup: Filter backup .blend files, (optional)
   :type filter_backup: bool
   :param filter_image: Filter image files, (optional)
   :type filter_image: bool
   :param filter_movie: Filter movie files, (optional)
   :type filter_movie: bool
   :param filter_python: Filter Python files, (optional)
   :type filter_python: bool
   :param filter_font: Filter font files, (optional)
   :type filter_font: bool
   :param filter_sound: Filter sound files, (optional)
   :type filter_sound: bool
   :param filter_text: Filter text files, (optional)
   :type filter_text: bool
   :param filter_archive: Filter archive files, (optional)
   :type filter_archive: bool
   :param filter_btx: Filter btx files, (optional)
   :type filter_btx: bool
   :param filter_alembic: Filter Alembic files, (optional)
   :type filter_alembic: bool
   :param filter_usd: Filter USD files, (optional)
   :type filter_usd: bool
   :param filter_obj: Filter OBJ files, (optional)
   :type filter_obj: bool
   :param filter_volume: Filter OpenVDB volume files, (optional)
   :type filter_volume: bool
   :param filter_folder: Filter folders, (optional)
   :type filter_folder: bool
   :param filter_blenlib: Filter Blender IDs, (optional)
   :type filter_blenlib: bool
   :param filemode: File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file (in [1, 9], optional)
   :type filemode: int
   :param display_type: Display Type, (optional)

      - ``DEFAULT``
        Default -- Automatically determine display type for files.
      - ``LIST_VERTICAL``
        Short List -- Display files as short list.
      - ``LIST_HORIZONTAL``
        Long List -- Display files as a detailed list.
      - ``THUMBNAIL``
        Thumbnails -- Display files as thumbnails.
   :type display_type: Literal['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL']
   :param sort_method: File sorting mode, (optional)
   :type sort_method: str
   :param global_scale: Scale, Value by which to enlarge or shrink the objects with respect to the world's origin (in [0.0001, 10000], optional)
   :type global_scale: float
   :param clamp_size: Clamp Bounding Box, Resize the objects to keep bounding box under this value. Value 0 disables clamping (in [0, 1000], optional)
   :type clamp_size: float
   :param forward_axis: Forward Axis, (optional)

      - ``X``
        X -- Positive X axis.
      - ``Y``
        Y -- Positive Y axis.
      - ``Z``
        Z -- Positive Z axis.
      - ``NEGATIVE_X``
        -X -- Negative X axis.
      - ``NEGATIVE_Y``
        -Y -- Negative Y axis.
      - ``NEGATIVE_Z``
        -Z -- Negative Z axis.
   :type forward_axis: Literal['X', 'Y', 'Z', 'NEGATIVE_X', 'NEGATIVE_Y', 'NEGATIVE_Z']
   :param up_axis: Up Axis, (optional)

      - ``X``
        X -- Positive X axis.
      - ``Y``
        Y -- Positive Y axis.
      - ``Z``
        Z -- Positive Z axis.
      - ``NEGATIVE_X``
        -X -- Negative X axis.
      - ``NEGATIVE_Y``
        -Y -- Negative Y axis.
      - ``NEGATIVE_Z``
        -Z -- Negative Z axis.
   :type up_axis: Literal['X', 'Y', 'Z', 'NEGATIVE_X', 'NEGATIVE_Y', 'NEGATIVE_Z']
   :param use_split_objects: Split By Object, Import each OBJ 'o' as a separate object (optional)
   :type use_split_objects: bool
   :param use_split_groups: Split By Group, Import each OBJ 'g' as a separate object (optional)
   :type use_split_groups: bool
   :param import_vertex_groups: Vertex Groups, Import OBJ groups as vertex groups (optional)
   :type import_vertex_groups: bool
   :param validate_meshes: Validate Meshes, Ensure the data is valid (when disabled, data may be imported which causes crashes displaying or editing) (optional)
   :type validate_meshes: bool
   :param close_spline_loops: Detect Cyclic Curves, Join curve endpoints if overlapping control points are detected (if disabled, no curves will be cyclic) (optional)
   :type close_spline_loops: bool
   :param collection_separator: Path Separator, Character used to separate objects name into hierarchical structure (optional, never None)
   :type collection_separator: str
   :param mtl_name_collision_mode: Material Name Collision, How to handle naming collisions when importing materials (optional)

      - ``MAKE_UNIQUE``
        Make Unique -- Create new materials with unique names for each OBJ file.
      - ``REFERENCE_EXISTING``
        Reference Existing -- Use existing materials with same name instead of creating new ones.
   :type mtl_name_collision_mode: Literal['MAKE_UNIQUE', 'REFERENCE_EXISTING']
   :param filter_glob: Extension Filter, (optional, never None)
   :type filter_glob: str
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]

.. function:: open_mainfile(*, filepath="", hide_props_region=True, check_existing=False, filter_blender=True, filter_backup=False, filter_image=False, filter_movie=False, filter_python=False, filter_font=False, filter_sound=False, filter_text=False, filter_archive=False, filter_btx=False, filter_alembic=False, filter_usd=False, filter_obj=False, filter_volume=False, filter_folder=True, filter_blenlib=False, filemode=8, display_type='DEFAULT', sort_method='', load_ui=True, use_scripts=False, display_file_selector=True, state=0)

   Open a Blender file

   :param filepath: File Path, Path to file (optional, never None)
   :type filepath: str
   :param hide_props_region: Hide Operator Properties, Collapse the region displaying the operator settings (optional)
   :type hide_props_region: bool
   :param check_existing: Check Existing, Check and warn on overwriting existing files (optional)
   :type check_existing: bool
   :param filter_blender: Filter .blend files, (optional)
   :type filter_blender: bool
   :param filter_backup: Filter backup .blend files, (optional)
   :type filter_backup: bool
   :param filter_image: Filter image files, (optional)
   :type filter_image: bool
   :param filter_movie: Filter movie files, (optional)
   :type filter_movie: bool
   :param filter_python: Filter Python files, (optional)
   :type filter_python: bool
   :param filter_font: Filter font files, (optional)
   :type filter_font: bool
   :param filter_sound: Filter sound files, (optional)
   :type filter_sound: bool
   :param filter_text: Filter text files, (optional)
   :type filter_text: bool
   :param filter_archive: Filter archive files, (optional)
   :type filter_archive: bool
   :param filter_btx: Filter btx files, (optional)
   :type filter_btx: bool
   :param filter_alembic: Filter Alembic files, (optional)
   :type filter_alembic: bool
   :param filter_usd: Filter USD files, (optional)
   :type filter_usd: bool
   :param filter_obj: Filter OBJ files, (optional)
   :type filter_obj: bool
   :param filter_volume: Filter OpenVDB volume files, (optional)
   :type filter_volume: bool
   :param filter_folder: Filter folders, (optional)
   :type filter_folder: bool
   :param filter_blenlib: Filter Blender IDs, (optional)
   :type filter_blenlib: bool
   :param filemode: File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file (in [1, 9], optional)
   :type filemode: int
   :param display_type: Display Type, (optional)

      - ``DEFAULT``
        Default -- Automatically determine display type for files.
      - ``LIST_VERTICAL``
        Short List -- Display files as short list.
      - ``LIST_HORIZONTAL``
        Long List -- Display files as a detailed list.
      - ``THUMBNAIL``
        Thumbnails -- Display files as thumbnails.
   :type display_type: Literal['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL']
   :param sort_method: File sorting mode, (optional)
   :type sort_method: str
   :param load_ui: Load UI, Load user interface setup in the .blend file (optional)
   :type load_ui: bool
   :param use_scripts: Trusted Source, Allow .blend file to execute scripts automatically, default available from system preferences (optional)
   :type use_scripts: bool
   :param display_file_selector: Display File Selector, (optional)
   :type display_file_selector: bool
   :param state: State, (in [-inf, inf], optional)
   :type state: int
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]

.. function:: operator_cheat_sheet()

   List all the operators in a text-block, useful for scripting

   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/wm.py\:2289 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L2289>`__

.. function:: operator_defaults()

   Set the active operator to its default values

   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
.. function:: operator_pie_enum(*, data_path="", prop_string="")

   Undocumented, consider `contributing <https://developer.blender.org/>`__.

   :param data_path: Operator, Operator name (in Python as string) (optional, never None)
   :type data_path: str
   :param prop_string: Property, Property name (as a string) (optional, never None)
   :type prop_string: str
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/wm.py\:777 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L777>`__


.. function:: operator_preset_add(*, name="", remove_name=False, remove_active=False, operator="")

   Add or remove an Operator Preset

   :param name: Name, Name of the preset, used to make the path name (optional, never None)
   :type name: str
   :param remove_name: remove_name, (optional)
   :type remove_name: bool
   :param remove_active: remove_active, (optional)
   :type remove_active: bool
   :param operator: Operator, (optional, never None)
   :type operator: str
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/presets.py\:119 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/presets.py#L119>`__


.. function:: operator_presets_cleanup(*, operator="", properties=None)

   Remove outdated operator properties from presets that may cause problems

   :param operator: operator, (optional, never None)
   :type operator: str
   :param properties: properties, (optional)
   :type properties: :class:`bpy_prop_collection`\ [:class:`OperatorFileListElement`] | None
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/presets.py\:967 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/presets.py#L967>`__


.. function:: owner_disable(*, owner_id="")

   Disable add-on for workspace

   :param owner_id: UI Tag, (optional, never None)
   :type owner_id: str
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/wm.py\:2337 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L2337>`__


.. function:: owner_enable(*, owner_id="")

   Enable add-on for workspace

   :param owner_id: UI Tag, (optional, never None)
   :type owner_id: str
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/wm.py\:2322 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L2322>`__


.. function:: path_open(*, filepath="")

   Open a path in a file browser

   :param filepath: filepath, (optional, never None)
   :type filepath: str
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/wm.py\:1185 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L1185>`__


.. function:: previews_batch_clear(*, files=None, directory="", filter_blender=True, filter_folder=True, use_scenes=True, use_collections=True, use_objects=True, use_intern_data=True, use_trusted=False, use_backups=True)

   Clear selected .blend file's previews

   :param files: files, (optional)
   :type files: :class:`bpy_prop_collection`\ [:class:`OperatorFileListElement`] | None
   :param directory: directory, (optional, never None)
   :type directory: str
   :param filter_blender: filter_blender, (optional)
   :type filter_blender: bool
   :param filter_folder: filter_folder, (optional)
   :type filter_folder: bool
   :param use_scenes: Scenes, Clear scenes' previews (optional)
   :type use_scenes: bool
   :param use_collections: Collections, Clear collections' previews (optional)
   :type use_collections: bool
   :param use_objects: Objects, Clear objects' previews (optional)
   :type use_objects: bool
   :param use_intern_data: Materials & Textures, Clear 'internal' previews (materials, textures, images, etc.) (optional)
   :type use_intern_data: bool
   :param use_trusted: Trusted Blend Files, Enable Python evaluation for selected files (optional)
   :type use_trusted: bool
   :param use_backups: Save Backups, Keep a backup (.blend1) version of the files when saving with cleared previews (optional)
   :type use_backups: bool
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/file.py\:204 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/file.py#L204>`__


.. function:: previews_batch_generate(*, files=None, directory="", filter_blender=True, filter_folder=True, use_scenes=True, use_collections=True, use_objects=True, use_intern_data=True, use_trusted=False, use_backups=True)

   Generate selected .blend file's previews

   :param files: Collection of file paths with common ``directory`` root (optional)
   :type files: :class:`bpy_prop_collection`\ [:class:`OperatorFileListElement`] | None
   :param directory: Root path of all files listed in ``files`` collection (optional, never None)
   :type directory: str
   :param filter_blender: Show Blender files in the File Browser (optional)
   :type filter_blender: bool
   :param filter_folder: Show folders in the File Browser (optional)
   :type filter_folder: bool
   :param use_scenes: Scenes, Generate scenes' previews (optional)
   :type use_scenes: bool
   :param use_collections: Collections, Generate collections' previews (optional)
   :type use_collections: bool
   :param use_objects: Objects, Generate objects' previews (optional)
   :type use_objects: bool
   :param use_intern_data: Materials & Textures, Generate 'internal' previews (materials, textures, images, etc.) (optional)
   :type use_intern_data: bool
   :param use_trusted: Trusted Blend Files, Enable Python evaluation for selected files (optional)
   :type use_trusted: bool
   :param use_backups: Save Backups, Keep a backup (.blend1) version of the files when saving with generated previews (optional)
   :type use_backups: bool
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/file.py\:95 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/file.py#L95>`__


.. function:: previews_clear(*, id_type=set())

   Clear data-block previews (only for some types like objects, materials, textures, etc.)

   :param id_type: Data-Block Type, Which data-block previews to clear (optional)

      - ``ALL``
        All Types.
      - ``GEOMETRY``
        All Geometry Types -- Clear previews for scenes, collections and objects.
      - ``SHADING``
        All Shading Types -- Clear previews for materials, lights, worlds, textures and images.
      - ``SCENE``
        Scenes.
      - ``COLLECTION``
        Collections.
      - ``OBJECT``
        Objects.
      - ``MATERIAL``
        Materials.
      - ``LIGHT``
        Lights.
      - ``WORLD``
        Worlds.
      - ``TEXTURE``
        Textures.
      - ``IMAGE``
        Images.
   :type id_type: set[Literal['ALL', 'GEOMETRY', 'SHADING', 'SCENE', 'COLLECTION', 'OBJECT', 'MATERIAL', 'LIGHT', 'WORLD', 'TEXTURE', 'IMAGE']]
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]

.. function:: previews_ensure()

   Ensure data-block previews are available and up-to-date (to be saved in .blend file, only for some types like materials, textures, etc.)

   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
.. function:: properties_add(*, data_path="")

   Add your own property to the data-block

   :param data_path: Property Edit, Property data_path edit (optional, never None)
   :type data_path: str
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/wm.py\:2171 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L2171>`__


.. function:: properties_context_change(*, context="")

   Jump to a different tab inside the properties editor

   :param context: Context, (optional, never None)
   :type context: str
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/wm.py\:2214 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L2214>`__


.. function:: properties_edit(*, data_path="", property_name="", property_type='FLOAT', is_overridable_library=False, description="", use_soft_limits=False, array_length=3, default_int=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), min_int=-10000, max_int=10000, soft_min_int=-10000, soft_max_int=10000, step_int=1, default_bool=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False), default_float=(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0), min_float=-10000.0, max_float=-10000.0, soft_min_float=-10000.0, soft_max_float=-10000.0, precision=3, step_float=0.1, subtype='', default_string="", id_type='OBJECT', eval_string="")

   Change a custom property's type, or adjust how it is displayed in the interface

   :param data_path: Property Edit, Property data_path edit (optional, never None)
   :type data_path: str
   :param property_name: Property Name, Property name edit (optional, never None)
   :type property_name: str
   :param property_type: Type, (optional)

      - ``FLOAT``
        Float -- A single floating-point value.
      - ``FLOAT_ARRAY``
        Float Array -- An array of floating-point values.
      - ``INT``
        Integer -- A single integer.
      - ``INT_ARRAY``
        Integer Array -- An array of integers.
      - ``BOOL``
        Boolean -- A true or false value.
      - ``BOOL_ARRAY``
        Boolean Array -- An array of true or false values.
      - ``STRING``
        String -- A string value.
      - ``DATA_BLOCK``
        Data-Block -- A data-block value.
      - ``PYTHON``
        Python -- Edit a Python value directly, for unsupported property types.
   :type property_type: Literal['FLOAT', 'FLOAT_ARRAY', 'INT', 'INT_ARRAY', 'BOOL', 'BOOL_ARRAY', 'STRING', 'DATA_BLOCK', 'PYTHON']
   :param is_overridable_library: Library Overridable, Allow the property to be overridden when the data-block is linked (optional)
   :type is_overridable_library: bool
   :param description: Description, (optional, never None)
   :type description: str
   :param use_soft_limits: Soft Limits, Limits the Property Value slider to a range, values outside the range must be inputted numerically (optional)
   :type use_soft_limits: bool
   :param array_length: Array Length, (in [1, 32], optional)
   :type array_length: int
   :param default_int: Default Value, (array of 32 items, in [-inf, inf], optional)
   :type default_int: Sequence[int]
   :param min_int: Min, (in [-inf, inf], optional)
   :type min_int: int
   :param max_int: Max, (in [-inf, inf], optional)
   :type max_int: int
   :param soft_min_int: Soft Min, (in [-inf, inf], optional)
   :type soft_min_int: int
   :param soft_max_int: Soft Max, (in [-inf, inf], optional)
   :type soft_max_int: int
   :param step_int: Step, (in [1, inf], optional)
   :type step_int: int
   :param default_bool: Default Value, (array of 32 items, optional)
   :type default_bool: Sequence[bool]
   :param default_float: Default Value, (array of 32 items, in [-inf, inf], optional)
   :type default_float: Sequence[float]
   :param min_float: Min, (in [-inf, inf], optional)
   :type min_float: float
   :param max_float: Max, (in [-inf, inf], optional)
   :type max_float: float
   :param soft_min_float: Soft Min, (in [-inf, inf], optional)
   :type soft_min_float: float
   :param soft_max_float: Soft Max, (in [-inf, inf], optional)
   :type soft_max_float: float
   :param precision: Precision, (in [0, 8], optional)
   :type precision: int
   :param step_float: Step, (in [0.001, inf], optional)
   :type step_float: float
   :param subtype: Subtype, (optional)
   :type subtype: str
   :param default_string: Default Value, (optional, never None)
   :type default_string: str
   :param id_type: ID Type, (optional)
   :type id_type: Literal['ACTION', 'ARMATURE', 'BRUSH', 'CACHEFILE', 'CAMERA', 'COLLECTION', 'CURVE', 'CURVES', 'FONT', 'GREASEPENCIL', 'GREASEPENCIL_V3', 'IMAGE', 'KEY', 'LATTICE', 'LIBRARY', 'LIGHT', 'LIGHT_PROBE', 'LINESTYLE', 'MASK', 'MATERIAL', 'MESH', 'META', 'MOVIECLIP', 'NODETREE', 'OBJECT', 'PAINTCURVE', 'PALETTE', 'PARTICLE', 'POINTCLOUD', 'SCENE', 'SCREEN', 'SOUND', 'SPEAKER', 'TEXT', 'TEXTURE', 'VOLUME', 'WINDOWMANAGER', 'WORKSPACE', 'WORLD']
   :param eval_string: Value, Python value for unsupported custom property types (optional, never None)
   :type eval_string: str
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/wm.py\:1904 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L1904>`__


.. function:: properties_edit_value(*, data_path="", property_name="", eval_string="")

   Edit the value of a custom property

   :param data_path: Property Edit, Property data_path edit (optional, never None)
   :type data_path: str
   :param property_name: Property Name, Property name edit (optional, never None)
   :type property_name: str
   :param eval_string: Value, Value for custom property types that can only be edited as a Python expression (optional, never None)
   :type eval_string: str
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/wm.py\:2128 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L2128>`__


.. function:: properties_remove(*, data_path="", property_name="")

   Internal use (edit a property data_path)

   :param data_path: Property Edit, Property data_path edit (optional, never None)
   :type data_path: str
   :param property_name: Property Name, Property name edit (optional, never None)
   :type property_name: str
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/wm.py\:2228 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L2228>`__


.. function:: quit_blender()

   Quit Blender

   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
.. function:: radial_control(*, data_path_primary="", data_path_secondary="", use_secondary="", rotation_path="", color_path="", fill_color_path="", fill_color_override_path="", fill_color_override_test_path="", zoom_path="", image_id="", secondary_tex=False, release_confirm=False)

   Set some size property (e.g. brush size) with mouse wheel

   :param data_path_primary: Primary Data Path, Primary path of property to be set by the radial control (optional, never None)
   :type data_path_primary: str
   :param data_path_secondary: Secondary Data Path, Secondary path of property to be set by the radial control (optional, never None)
   :type data_path_secondary: str
   :param use_secondary: Use Secondary, Path of property to select between the primary and secondary data paths (optional, never None)
   :type use_secondary: str
   :param rotation_path: Rotation Path, Path of property used to rotate the texture display (optional, never None)
   :type rotation_path: str
   :param color_path: Color Path, Path of property used to set the color of the control (optional, never None)
   :type color_path: str
   :param fill_color_path: Fill Color Path, Path of property used to set the fill color of the control (optional, never None)
   :type fill_color_path: str
   :param fill_color_override_path: Fill Color Override Path, (optional, never None)
   :type fill_color_override_path: str
   :param fill_color_override_test_path: Fill Color Override Test, (optional, never None)
   :type fill_color_override_test_path: str
   :param zoom_path: Zoom Path, Path of property used to set the zoom level for the control (optional, never None)
   :type zoom_path: str
   :param image_id: Image ID, Path of ID that is used to generate an image for the control (optional, never None)
   :type image_id: str
   :param secondary_tex: Secondary Texture, Tweak brush secondary/mask texture (optional)
   :type secondary_tex: bool
   :param release_confirm: Confirm On Release, Finish operation on key release (optional)
   :type release_confirm: bool
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]

.. function:: read_factory_settings(*, use_factory_startup_app_template_only=False, app_template="Template", use_empty=False)

   Load factory default startup file and preferences. To make changes permanent, use "Save Startup File" and "Save Preferences"

   :param use_factory_startup_app_template_only: Factory Startup App-Template Only, (optional)
   :type use_factory_startup_app_template_only: bool
   :param app_template: (optional, never None)
   :type app_template: str
   :param use_empty: Empty, After loading, remove everything except scenes, windows, and workspaces. This makes it possible to load the startup file with its scene configuration and window layout intact, but no objects, materials, animations, ... (optional)
   :type use_empty: bool
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]

.. function:: read_factory_userpref(*, use_factory_startup_app_template_only=False)

   Load factory default preferences. To make changes to preferences permanent, use "Save Preferences"

   :param use_factory_startup_app_template_only: Factory Startup App-Template Only, (optional)
   :type use_factory_startup_app_template_only: bool
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]

.. function:: read_history()

   Reloads history and bookmarks

   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
.. function:: read_homefile(*, filepath="", load_ui=True, use_splash=False, use_factory_startup=False, use_factory_startup_app_template_only=False, app_template="Template", use_empty=False)

   Open the default file

   :param filepath: File Path, Path to an alternative start-up file (optional, never None)
   :type filepath: str
   :param load_ui: Load UI, Load user interface setup from the .blend file (optional)
   :type load_ui: bool
   :param use_splash: Splash, (optional)
   :type use_splash: bool
   :param use_factory_startup: Factory Startup, Load the default ('factory startup') blend file. This is independent of the normal start-up file that the user can save (optional)
   :type use_factory_startup: bool
   :param use_factory_startup_app_template_only: Factory Startup App-Template Only, (optional)
   :type use_factory_startup_app_template_only: bool
   :param app_template: (optional, never None)
   :type app_template: str
   :param use_empty: Empty, After loading, remove everything except scenes, windows, and workspaces. This makes it possible to load the startup file with its scene configuration and window layout intact, but no objects, materials, animations, ... (optional)
   :type use_empty: bool
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]

.. function:: read_userpref()

   Load last saved preferences

   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
.. function:: recover_auto_save(*, filepath="", hide_props_region=True, check_existing=False, filter_blender=True, filter_backup=False, filter_image=False, filter_movie=False, filter_python=False, filter_font=False, filter_sound=False, filter_text=False, filter_archive=False, filter_btx=False, filter_alembic=False, filter_usd=False, filter_obj=False, filter_volume=False, filter_folder=False, filter_blenlib=False, filemode=8, display_type='LIST_VERTICAL', sort_method='', use_scripts=False)

   Open an automatically saved file to recover it

   :param filepath: File Path, Path to file (optional, never None)
   :type filepath: str
   :param hide_props_region: Hide Operator Properties, Collapse the region displaying the operator settings (optional)
   :type hide_props_region: bool
   :param check_existing: Check Existing, Check and warn on overwriting existing files (optional)
   :type check_existing: bool
   :param filter_blender: Filter .blend files, (optional)
   :type filter_blender: bool
   :param filter_backup: Filter backup .blend files, (optional)
   :type filter_backup: bool
   :param filter_image: Filter image files, (optional)
   :type filter_image: bool
   :param filter_movie: Filter movie files, (optional)
   :type filter_movie: bool
   :param filter_python: Filter Python files, (optional)
   :type filter_python: bool
   :param filter_font: Filter font files, (optional)
   :type filter_font: bool
   :param filter_sound: Filter sound files, (optional)
   :type filter_sound: bool
   :param filter_text: Filter text files, (optional)
   :type filter_text: bool
   :param filter_archive: Filter archive files, (optional)
   :type filter_archive: bool
   :param filter_btx: Filter btx files, (optional)
   :type filter_btx: bool
   :param filter_alembic: Filter Alembic files, (optional)
   :type filter_alembic: bool
   :param filter_usd: Filter USD files, (optional)
   :type filter_usd: bool
   :param filter_obj: Filter OBJ files, (optional)
   :type filter_obj: bool
   :param filter_volume: Filter OpenVDB volume files, (optional)
   :type filter_volume: bool
   :param filter_folder: Filter folders, (optional)
   :type filter_folder: bool
   :param filter_blenlib: Filter Blender IDs, (optional)
   :type filter_blenlib: bool
   :param filemode: File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file (in [1, 9], optional)
   :type filemode: int
   :param display_type: Display Type, (optional)

      - ``DEFAULT``
        Default -- Automatically determine display type for files.
      - ``LIST_VERTICAL``
        Short List -- Display files as short list.
      - ``LIST_HORIZONTAL``
        Long List -- Display files as a detailed list.
      - ``THUMBNAIL``
        Thumbnails -- Display files as thumbnails.
   :type display_type: Literal['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL']
   :param sort_method: File sorting mode, (optional)
   :type sort_method: str
   :param use_scripts: Trusted Source, Allow .blend file to execute scripts automatically, default available from system preferences (optional)
   :type use_scripts: bool
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]

.. function:: recover_last_session(*, use_scripts=False)

   Open the last closed file ("quit.blend")

   :param use_scripts: Trusted Source, Allow .blend file to execute scripts automatically, default available from system preferences (optional)
   :type use_scripts: bool
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]

.. function:: redraw_timer(*, type='DRAW', iterations=10, time_limit=0.0)

   Simple redraw timer to test the speed of updating the interface

   :param type: Type, (optional)

      - ``DRAW``
        Draw Region -- Draw region.
      - ``DRAW_SWAP``
        Draw Region & Swap -- Draw region and swap.
      - ``DRAW_WIN``
        Draw Window -- Draw window.
      - ``DRAW_WIN_SWAP``
        Draw Window & Swap -- Draw window and swap.
      - ``ANIM_STEP``
        Animation Step -- Animation steps.
      - ``ANIM_PLAY``
        Animation Play -- Animation playback.
      - ``UNDO``
        Undo/Redo -- Undo and redo.
   :type type: Literal['DRAW', 'DRAW_SWAP', 'DRAW_WIN', 'DRAW_WIN_SWAP', 'ANIM_STEP', 'ANIM_PLAY', 'UNDO']
   :param iterations: Iterations, Number of times to redraw (in [1, inf], optional)
   :type iterations: int
   :param time_limit: Time Limit, Seconds to run the test for (override iterations) (in [0, inf], optional)
   :type time_limit: float
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]

.. function:: revert_mainfile(*, use_scripts=False)

   Reload the saved file

   :param use_scripts: Trusted Source, Allow .blend file to execute scripts automatically, default available from system preferences (optional)
   :type use_scripts: bool
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]

.. function:: save_as_mainfile(*, filepath="", hide_props_region=True, check_existing=True, filter_blender=True, filter_backup=False, filter_image=False, filter_movie=False, filter_python=False, filter_font=False, filter_sound=False, filter_text=False, filter_archive=False, filter_btx=False, filter_alembic=False, filter_usd=False, filter_obj=False, filter_volume=False, filter_folder=True, filter_blenlib=False, filemode=8, display_type='DEFAULT', sort_method='', compress=False, relative_remap=True, copy=False, show_save_modified_images_dialog=False)

   Save the current file in the desired location

   :param filepath: File Path, Path to file (optional, never None)
   :type filepath: str
   :param hide_props_region: Hide Operator Properties, Collapse the region displaying the operator settings (optional)
   :type hide_props_region: bool
   :param check_existing: Check Existing, Check and warn on overwriting existing files (optional)
   :type check_existing: bool
   :param filter_blender: Filter .blend files, (optional)
   :type filter_blender: bool
   :param filter_backup: Filter backup .blend files, (optional)
   :type filter_backup: bool
   :param filter_image: Filter image files, (optional)
   :type filter_image: bool
   :param filter_movie: Filter movie files, (optional)
   :type filter_movie: bool
   :param filter_python: Filter Python files, (optional)
   :type filter_python: bool
   :param filter_font: Filter font files, (optional)
   :type filter_font: bool
   :param filter_sound: Filter sound files, (optional)
   :type filter_sound: bool
   :param filter_text: Filter text files, (optional)
   :type filter_text: bool
   :param filter_archive: Filter archive files, (optional)
   :type filter_archive: bool
   :param filter_btx: Filter btx files, (optional)
   :type filter_btx: bool
   :param filter_alembic: Filter Alembic files, (optional)
   :type filter_alembic: bool
   :param filter_usd: Filter USD files, (optional)
   :type filter_usd: bool
   :param filter_obj: Filter OBJ files, (optional)
   :type filter_obj: bool
   :param filter_volume: Filter OpenVDB volume files, (optional)
   :type filter_volume: bool
   :param filter_folder: Filter folders, (optional)
   :type filter_folder: bool
   :param filter_blenlib: Filter Blender IDs, (optional)
   :type filter_blenlib: bool
   :param filemode: File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file (in [1, 9], optional)
   :type filemode: int
   :param display_type: Display Type, (optional)

      - ``DEFAULT``
        Default -- Automatically determine display type for files.
      - ``LIST_VERTICAL``
        Short List -- Display files as short list.
      - ``LIST_HORIZONTAL``
        Long List -- Display files as a detailed list.
      - ``THUMBNAIL``
        Thumbnails -- Display files as thumbnails.
   :type display_type: Literal['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL']
   :param sort_method: File sorting mode, (optional)
   :type sort_method: str
   :param compress: Compress, Write compressed .blend file (optional)
   :type compress: bool
   :param relative_remap: Remap Relative, Remap relative paths when saving to a different directory (optional)
   :type relative_remap: bool
   :param copy: Save Copy, Save a copy of the actual working state but does not make saved file active (optional)
   :type copy: bool
   :param show_save_modified_images_dialog: Show Save Modified Images Dialog, Show a popup dialog to save modified images before saving the blend file (optional)
   :type show_save_modified_images_dialog: bool
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]

.. function:: save_auto_save()

   Create an autosave in the temp directory for the current file

   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
.. function:: save_homefile()

   Make the current file the default startup file

   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
.. function:: save_mainfile(*, filepath="", hide_props_region=True, check_existing=True, filter_blender=True, filter_backup=False, filter_image=False, filter_movie=False, filter_python=False, filter_font=False, filter_sound=False, filter_text=False, filter_archive=False, filter_btx=False, filter_alembic=False, filter_usd=False, filter_obj=False, filter_volume=False, filter_folder=True, filter_blenlib=False, filemode=8, display_type='DEFAULT', sort_method='', compress=False, relative_remap=False, exit=False, incremental=False, show_save_modified_images_dialog=False)

   Save the current Blender file

   :param filepath: File Path, Path to file (optional, never None)
   :type filepath: str
   :param hide_props_region: Hide Operator Properties, Collapse the region displaying the operator settings (optional)
   :type hide_props_region: bool
   :param check_existing: Check Existing, Check and warn on overwriting existing files (optional)
   :type check_existing: bool
   :param filter_blender: Filter .blend files, (optional)
   :type filter_blender: bool
   :param filter_backup: Filter backup .blend files, (optional)
   :type filter_backup: bool
   :param filter_image: Filter image files, (optional)
   :type filter_image: bool
   :param filter_movie: Filter movie files, (optional)
   :type filter_movie: bool
   :param filter_python: Filter Python files, (optional)
   :type filter_python: bool
   :param filter_font: Filter font files, (optional)
   :type filter_font: bool
   :param filter_sound: Filter sound files, (optional)
   :type filter_sound: bool
   :param filter_text: Filter text files, (optional)
   :type filter_text: bool
   :param filter_archive: Filter archive files, (optional)
   :type filter_archive: bool
   :param filter_btx: Filter btx files, (optional)
   :type filter_btx: bool
   :param filter_alembic: Filter Alembic files, (optional)
   :type filter_alembic: bool
   :param filter_usd: Filter USD files, (optional)
   :type filter_usd: bool
   :param filter_obj: Filter OBJ files, (optional)
   :type filter_obj: bool
   :param filter_volume: Filter OpenVDB volume files, (optional)
   :type filter_volume: bool
   :param filter_folder: Filter folders, (optional)
   :type filter_folder: bool
   :param filter_blenlib: Filter Blender IDs, (optional)
   :type filter_blenlib: bool
   :param filemode: File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file (in [1, 9], optional)
   :type filemode: int
   :param display_type: Display Type, (optional)

      - ``DEFAULT``
        Default -- Automatically determine display type for files.
      - ``LIST_VERTICAL``
        Short List -- Display files as short list.
      - ``LIST_HORIZONTAL``
        Long List -- Display files as a detailed list.
      - ``THUMBNAIL``
        Thumbnails -- Display files as thumbnails.
   :type display_type: Literal['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL']
   :param sort_method: File sorting mode, (optional)
   :type sort_method: str
   :param compress: Compress, Write compressed .blend file (optional)
   :type compress: bool
   :param relative_remap: Remap Relative, Remap relative paths when saving to a different directory (optional)
   :type relative_remap: bool
   :param exit: Exit, Exit Blender after saving (optional)
   :type exit: bool
   :param incremental: Incremental, Save the current Blender file with a numerically incremented name that does not overwrite any existing files (optional)
   :type incremental: bool
   :param show_save_modified_images_dialog: Show Save Modified Images Dialog, Show a popup dialog to save modified images before saving the blend file (optional)
   :type show_save_modified_images_dialog: bool
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]

.. function:: save_userpref()

   Make the current preferences default

   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
.. function:: search_menu()

   Pop-up a search over all menus in the current context

   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
.. function:: search_operator()

   Pop-up a search over all available operators in current context

   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
.. function:: search_single_menu(*, menu_idname="", initial_query="")

   Pop-up a search for a menu in current context

   :param menu_idname: Menu Name, Menu to search in (optional, never None)
   :type menu_idname: str
   :param initial_query: Initial Query, Query to insert into the search box (optional, never None)
   :type initial_query: str
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]

.. function:: set_stereo_3d(*, display_mode='ANAGLYPH', anaglyph_type='RED_CYAN', interlace_type='ROW_INTERLEAVED', use_interlace_swap=False, use_sidebyside_crosseyed=False)

   Toggle 3D stereo support for current window (or change the display mode)

   :param display_mode: Display Mode, (optional)
   :type display_mode: Literal[:ref:`rna_enum_stereo3d_display_items`]
   :param anaglyph_type: Anaglyph Type, (optional)
   :type anaglyph_type: Literal[:ref:`rna_enum_stereo3d_anaglyph_type_items`]
   :param interlace_type: Interlace Type, (optional)
   :type interlace_type: Literal[:ref:`rna_enum_stereo3d_interlace_type_items`]
   :param use_interlace_swap: Swap Left/Right, Swap left and right stereo channels (optional)
   :type use_interlace_swap: bool
   :param use_sidebyside_crosseyed: Cross-Eyed, Right eye should see left image and vice versa (optional)
   :type use_sidebyside_crosseyed: bool
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]

.. function:: set_working_color_space(*, convert_colors=True, working_space='')

   Change the working color space of all colors in this blend file

   :param convert_colors: Convert Colors in All Data-blocks, Change colors in all data-blocks to the new working space (optional)
   :type convert_colors: bool
   :param working_space: Working Space, Color space to set (optional)
   :type working_space: str
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]

.. function:: splash()

   Open the splash screen with release info

   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
.. function:: splash_about()

   Open a window with information about Blender

   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
.. function:: sysinfo(*, filepath="")

   Generate system information, saved into a text file

   :param filepath: filepath, (optional, never None)
   :type filepath: str
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/wm.py\:2257 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L2257>`__


.. function:: tool_set_by_brush_type(*, brush_type="", space_type='EMPTY')

   Look up the most appropriate tool for the given brush type and activate that

   :param brush_type: Brush Type, Brush type identifier for which the most appropriate tool will be looked up (optional, never None)
   :type brush_type: str
   :param space_type: Type, (optional)
   :type space_type: Literal['EMPTY', 'VIEW_3D', 'IMAGE_EDITOR', 'NODE_EDITOR', 'SEQUENCE_EDITOR', 'CLIP_EDITOR', 'DOPESHEET_EDITOR', 'GRAPH_EDITOR', 'NLA_EDITOR', 'TEXT_EDITOR', 'CONSOLE', 'INFO', 'TOPBAR', 'STATUSBAR', 'OUTLINER', 'PROPERTIES', 'FILE_BROWSER', 'SPREADSHEET', 'PREFERENCES']
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/wm.py\:2471 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L2471>`__


.. function:: tool_set_by_id(*, name="", cycle=False, as_fallback=False, space_type='EMPTY')

   Set the tool by name (for key-maps)

   :param name: Identifier, Identifier of the tool (optional, never None)
   :type name: str
   :param cycle: Cycle, Cycle through tools in this group (optional)
   :type cycle: bool
   :param as_fallback: Set Fallback, Set the fallback tool instead of the primary tool (optional)
   :type as_fallback: bool
   :param space_type: Type, (optional)
   :type space_type: Literal['EMPTY', 'VIEW_3D', 'IMAGE_EDITOR', 'NODE_EDITOR', 'SEQUENCE_EDITOR', 'CLIP_EDITOR', 'DOPESHEET_EDITOR', 'GRAPH_EDITOR', 'NLA_EDITOR', 'TEXT_EDITOR', 'CONSOLE', 'INFO', 'TOPBAR', 'STATUSBAR', 'OUTLINER', 'PROPERTIES', 'FILE_BROWSER', 'SPREADSHEET', 'PREFERENCES']
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/wm.py\:2380 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L2380>`__


.. function:: tool_set_by_index(*, index=0, cycle=False, expand=True, as_fallback=False, space_type='EMPTY')

   Set the tool by index (for key-maps)

   :param index: Index in Toolbar, (in [-inf, inf], optional)
   :type index: int
   :param cycle: Cycle, Cycle through tools in this group (optional)
   :type cycle: bool
   :param expand: expand, Include tool subgroups (optional)
   :type expand: bool
   :param as_fallback: Set Fallback, Set the fallback tool instead of the primary (optional)
   :type as_fallback: bool
   :param space_type: Type, (optional)
   :type space_type: Literal['EMPTY', 'VIEW_3D', 'IMAGE_EDITOR', 'NODE_EDITOR', 'SEQUENCE_EDITOR', 'CLIP_EDITOR', 'DOPESHEET_EDITOR', 'GRAPH_EDITOR', 'NLA_EDITOR', 'TEXT_EDITOR', 'CONSOLE', 'INFO', 'TOPBAR', 'STATUSBAR', 'OUTLINER', 'PROPERTIES', 'FILE_BROWSER', 'SPREADSHEET', 'PREFERENCES']
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/wm.py\:2430 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L2430>`__


.. function:: toolbar()

   Undocumented, consider `contributing <https://developer.blender.org/>`__.

   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/wm.py\:2538 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L2538>`__

.. function:: toolbar_fallback_pie()

   Undocumented, consider `contributing <https://developer.blender.org/>`__.

   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/wm.py\:2562 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L2562>`__

.. function:: toolbar_prompt()

   Leader key like functionality for accessing tools

   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/wm.py\:2662 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L2662>`__

.. function:: url_open(*, url="")

   Open a website in the web browser

   :param url: URL, URL to open (optional, never None)
   :type url: str
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/wm.py\:1085 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L1085>`__


.. function:: url_open_preset(*, type='')

   Open a preset website in the web browser

   :param type: Site, (optional)
   :type type: str
   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
   :File: `startup/bl_operators/wm.py\:1168 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_operators/wm.py#L1168>`__


.. function:: window_close()

   Close the current window

   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
.. function:: window_fullscreen_toggle()

   Toggle the current window full-screen

   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
.. function:: window_new()

   Create a new window

   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
.. function:: window_new_main()

   Create a new main window with its own workspace and scene selection

   :return: Result of the operator call.
   :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
