# Gather Resources - Gathers all resources used in the project and copies them to a local textures folder.
# Copyright (C) 2024  Simon Heggie
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# You can provide feedback, report bugs, or submit suggestions via the issue section:
# https://github.com/SimonHeggie/Blender-GatherResources/issues
#
# If this program operates interactively, it should output the following:
#
# Gather Resources  Copyright (C) 2024  Simon Heggie
# This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
# This is free software, and you are welcome to redistribute it
# under certain conditions; type `show c' for details.
#
# The commands `show w` and `show c` should display relevant parts of the GNU GPL.

bl_info = {
    "name": "Gather Resources",
    "blender": (4, 2, 0),
    "category": "File",
    "version": (0, 3, 1, "alpha"),
    "author": "Simon Heggie",
    "description": "Gathers all resources used in the project to a local textures folder.",
    "location": "File > External Data",
    "warning": "Pre-alpha testing",
    "wiki_url": "https://github.com/SimonHeggie/Blender-GatherResources/blob/main/README.md",
    "tracker_url": "https://github.com/SimonHeggie/Blender-GatherResources/issues",
    "license": "GPL",
}

# (rest of the code follows here)

import bpy
import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

class GatherResourcesOperator(bpy.types.Operator):
    """Gather resources and copy to the 'textures/' folder within the .blend file's directory"""
    bl_idname = "file.gather_resources"
    bl_label = "Gather Resources"
    bl_options = {'REGISTER', 'UNDO'}

    def copy_file(self, src, dest):
        """Helper function to copy files with error handling."""
        try:
            if not dest.exists() or src.stat().st_mtime > dest.stat().st_mtime:
                shutil.copy2(src, dest)
                self.report({'INFO'}, f"Collected: {src} -> {dest}")
            return src.name, True
        except PermissionError as e:
            self.report({'ERROR'}, f"Error copying {src}: {e}")
            return src.name, False

    def get_destination_folder(self, src, textures_dir):
        """Determine destination folder to prevent naming conflicts."""
        if textures_dir in src.parents:
            return textures_dir  # Place in root if already inside textures/

        folder_name = src.parent.name
        folder_path = textures_dir / folder_name
        folder_path.mkdir(parents=True, exist_ok=True)
        return folder_path

    def execute(self, context):
        # Check if the blend file has been saved
        blend_filepath = bpy.data.filepath
        if not blend_filepath:
            self.report({'ERROR'}, "Please save your blend file before gathering resources.")
            return {'CANCELLED'}

        # Set destination directory relative to the saved .blend file
        blend_dir = Path(bpy.path.abspath("//"))
        textures_dir = blend_dir / "textures"
        textures_dir.mkdir(parents=True, exist_ok=True)

        tasks = []

        def add_task_for_path(file_path, strip=None):
            """Add a copy task for a given file path, checking strip type if needed."""
            if not file_path:  # Ensure the path is valid
                return

            # Check if it's a SoundSequence and use strip.sound.filepath if available
            if strip and hasattr(strip, 'sound'):
                file_path = strip.sound.filepath

            src = Path(bpy.path.abspath(file_path))
            if src.exists():  # Ensure the file exists
                dest = self.get_destination_folder(src, textures_dir) / src.name
                tasks.append(executor.submit(self.copy_file, src, dest))
            else:
                self.report({'WARNING'}, f"File not found: {src}")

        with ThreadPoolExecutor() as executor:
            # Process all images used in shaders and textures
            for image in bpy.data.images:
                add_task_for_path(image.filepath)

            # Process all media files in VSE
            for scene in bpy.data.scenes:
                if scene.sequence_editor:
                    for strip in scene.sequence_editor.sequences_all:
                        add_task_for_path(strip.filepath if hasattr(strip, 'filepath') else None, strip=strip)

            # Process all cache files in object modifiers
            for obj in bpy.data.objects:
                for mod in obj.modifiers:
                    if mod.type == 'MESH_SEQUENCE_CACHE' and mod.cache_file:
                        add_task_for_path(mod.cache_file.filepath)

        # Process results and print summary
        collected_files = {"TOTAL": 0}
        for future in as_completed(tasks):
            filename, success = future.result()
            if success:
                collected_files["TOTAL"] += 1

        self.report({'INFO'}, f"Gathering Complete: {collected_files['TOTAL']} files collected.")
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(GatherResourcesOperator.bl_idname, text="Gather Resources")


def register():
    bpy.utils.register_class(GatherResourcesOperator)
    bpy.types.TOPBAR_MT_file_external_data.prepend(menu_func)  # Use prepend to insert at the top

def unregister():
    bpy.utils.unregister_class(GatherResourcesOperator)
    bpy.types.TOPBAR_MT_file_external_data.remove(menu_func)


if __name__ == "__main__":
    register()
