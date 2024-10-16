import bpy
import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Define supported file extensions for gathering
CLIP_FILES = {'.mp4', '.mov', '.avi', '.mkv', '.flv', '.webm', '.ogg', '.mpeg'}
ABC_FILES = {'.abc'}  # Alembic files for animations and geometry caches
IMAGE_FILES = {'.jpg', '.jpeg', '.png', '.tga', '.exr', '.dpx', '.cin', 
               '.hdr', '.sgi', '.tif', '.tiff'}
3D_FILES = {'.fbx', '.obj', '.dae', '.stl', '.ply', '.x', '.lwo', 
            '.bvh', '.3ds', '.vrml', '.wrl', '.x3d', '.usd'}

# Cache files include both Alembic (.abc) and USD (.usd) formats
CACHE_FILES = ABC_FILES | {'.usd'}

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

def gather_resources():
    # Set destination directory
    destination = Path(bpy.path.abspath("//textures/"))
    destination.mkdir(parents=True, exist_ok=True)

    collected = {"MOVIE": 0, "IMAGE": 0, "SOUND": 0, "ALEMBIC": 0, "3D": 0, "CACHE": 0}
    tasks = []

    # Gather all media tasks using multi-threading
    with ThreadPoolExecutor() as executor:
        for scene in bpy.data.scenes:
            if scene.sequence_editor:
                for strip in scene.sequence_editor.sequences_all:
                    if strip.type in {'MOVIE', 'IMAGE', 'SOUND'}:
                        src = Path(bpy.path.abspath(strip.filepath))
                        dest = destination / src.name
                        tasks.append(executor.submit(copy_file, src, dest))

            # Handle Alembic and other cache files used in modifiers
            for obj in scene.objects:
                if obj.modifiers:
                    for mod in obj.modifiers:
                        if mod.type == 'MESH_SEQUENCE_CACHE' and mod.cache_file:
                            cache_path = Path(bpy.path.abspath(mod.cache_file.filepath))
                            cache_dest = destination / cache_path.name
                            tasks.append(executor.submit(copy_file, cache_path, cache_dest))

    # Process results and update stats
    for future in as_completed(tasks):
        filename, success = future.result()
        if success:
            strip_path = destination / filename

            # Update collection stats based on file type
            if any(filename.endswith(ext) for ext in CLIP_FILES):
                collected['MOVIE'] += 1
            elif filename.endswith(tuple(ABC_FILES)):
                collected['ALEMBIC'] += 1
            elif filename.endswith(tuple(IMAGE_FILES)):
                collected['IMAGE'] += 1
            elif filename.endswith(tuple(3D_FILES)):
                collected['3D'] += 1
            elif filename.endswith(tuple(CACHE_FILES)):
                collected['CACHE'] += 1

    # Display summary of collected files
    print(f"Gathering Complete: {collected['MOVIE']} videos, "
          f"{collected['IMAGE']} images, {collected['SOUND']} audio files, "
          f"{collected['ALEMBIC']} Alembic files, {collected['3D']} 3D models, "
          f"{collected['CACHE']} cache files.")

# Call the function
gather_resources()
