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

    # Use multi-threading for faster processing
    with ThreadPoolExecutor() as executor:
        # Scan all data blocks in the active scene
        for datablock in bpy.data.objects:
            # Check for modifiers with external references (e.g., Alembic caches)
            if datablock.modifiers:
                for mod in datablock.modifiers:
                    if mod.type == 'MESH_SEQUENCE_CACHE' and mod.cache_file:
                        src = Path(bpy.path.abspath(mod.cache_file.filepath))
                        dest = get_destination_folder(src, textures_dir) / src.name
                        tasks.append(executor.submit(copy_file, src, dest))

        # Handle video, audio, and image strips in the VSE
        for scene in bpy.data.scenes:
            if scene.sequence_editor:
                for strip in scene.sequence_editor.sequences_all:
                    if strip.type in {'MOVIE', 'IMAGE', 'SOUND'}:
                        src = Path(bpy.path.abspath(strip.filepath))
                        dest = get_destination_folder(src, textures_dir) / src.name
                        tasks.append(executor.submit(copy_file, src, dest))

    # Process results and report collected files
    collected_files = {"TOTAL": 0}
    for future in as_completed(tasks):
        filename, success = future.result()
        if success:
            collected_files["TOTAL"] += 1

    # Print summary of collected resources
    print(f"Gathering Complete: {collected_files['TOTAL']} files collected.")

# Call the function
gather_resources()
