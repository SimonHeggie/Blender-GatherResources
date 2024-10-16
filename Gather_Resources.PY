import bpy
import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

def copy_file(src, dest):
    """Helper function to copy files with error handling."""
    try:
        if not dest.exists() or src.stat().st_mtime > dest.stat().st_mtime:
            shutil.copy2(src, dest)
            print(f"Collected: {src} -> {dest}")
        return src.name, True
    except PermissionError as e:
        print(f"Error copying {src}: {e}")
        return src.name, False

def get_destination_folder(src, textures_dir):
    """Determine destination folder to prevent naming conflicts."""
    if textures_dir in src.parents:
        return textures_dir  # Place in root if already inside textures/
    
    folder_name = src.parent.name
    folder_path = textures_dir / folder_name
    folder_path.mkdir(parents=True, exist_ok=True)
    return folder_path

def gather_resources():
    # Set destination directory
    textures_dir = Path(bpy.path.abspath("//textures/"))
    textures_dir.mkdir(parents=True, exist_ok=True)

    tasks = []

    def add_task_for_path(file_path):
        """Add a copy task for a given file path."""
        if not file_path:  # Ensure the path is valid
            return
        src = Path(bpy.path.abspath(file_path))
        if src.exists():  # Ensure the file exists
            dest = get_destination_folder(src, textures_dir) / src.name
            tasks.append(executor.submit(copy_file, src, dest))
        else:
            print(f"File not found: {src}")

    with ThreadPoolExecutor() as executor:
        # Process all images used in shaders and textures
        for image in bpy.data.images:
            add_task_for_path(image.filepath)

        # Process all media files in VSE
        for scene in bpy.data.scenes:
            if scene.sequence_editor:
                for strip in scene.sequence_editor.sequences_all:
                    add_task_for_path(strip.filepath)

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

    print(f"Gathering Complete: {collected_files['TOTAL']} files collected.")

# Call the function
gather_resources()
