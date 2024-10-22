# Blender-GatherResources

Collect/Assemble/Gather all resources to the texture child directory. AKA: 'GET YOUR SHIT TOGETHER.'

<img src="GatherResources.png">

Early testing has begun.

I have tested a couple of scenarios, but TEST AT YOUR OWN PERIL.... Be sure to test it on something that you don't mind destroying. 


## Installation:

Download from here: https://github.com/SimonHeggie/Blender-GatherResources/archive/refs/heads/main.zip (DO NOT UNZIP)

In blender: Edit/Preferences/Add-ons... Top right arrow, 'Install from Disk'. Select the Gather Resources zip file, then tick it to activate.

## Usage:

File > External Data > Gather Resources: 

This will take all resources used within your project and relocate them to your child texture directory.

## (Speculative) Road Map:

### Alpha:

- If a duplicate is found somehow; either rename the file, or place in number clone folder. Should be dedectable via comparing file sizes.
- There is currently a bug where sub-folders in the texture folder are moved into the root of textures which may result in unwanted merged data.
- If a duplicate is found and it has the exact same file size, technically that should be re-used instead of causing uneccesary clone data bloat. (This means that asset versioning is up to the users to manage)

### Beta

- Full cross platform support (Linux, Windows, Mac)

### Production ready Stable build:

- All bugs founds and crushed

### Future ideas:

- Menu option to 'Automatically Gather Resources'
- Either combine the task of, or create a seperate option for capturing all PROXY and CACHE data, which should be gathered but probably not into the 'textures' directory, seeing as it's something that it not as essential as the core resources needed to re-bake and re-render.
- 'Distribute Resources' Sort of like unpack; does the opposite of Gather. It requires storing the original locations of files prior to being gathered. Usecase is updating modified library and stock content for example.
- Support for resource data which is linked and needs to be gathered and vise-versa
- (Very unsure of where this is essential or not...) Collapse the entire 'PACK' menu into one sub-menu and do the same for the gathering commands to neaten the entire menu.
- CLEAN resources: FIRST; warns the users to double check that any other blend files are not share data, and if they are to append all into one blend file before hand. (can remove warning) THEN finds every file NOT being read by the active blend file and removes it. This is going to be SO helpful for optimizing for easy deployment and archiving.

### Final plan:

- Polish the Addon: Ensure code quality, follow Blender's coding guidelines, and fully document the addon.
- Submit to Blender Developers: Create a task on Blender Developer Site and submit the addon for review.
- Engage with Developer Community: Discuss the proposal on the Blender Developer forums or IRC to gather feedback.
- Address Feedback: Make necessary improvements based on code reviews and feedback from Blender's core development team.
- Wait for Testing and Integration: The addon will go through further testing, and if accepted, it will be included in a future Blender release.

## Reporting BUGS:

This is going to be full of bugs, so any testing is apreciated.

#### Report bugs to:

https://github.com/SimonHeggie/Blender-GatherResources/issues

And please use the following, or similar bug reporting template (Copy and paste it :)):

-

#### 1. Summary of the Issue

What’s not working? (E.g., "File links are not updating to the new 'textures' folder.")
What did you expect to happen? (E.g., "The script should copy files to the 'textures' folder and update the paths to relative links.")

#### 2. Steps to Reproduce the Issue

Provide a step-by-step guide to reproduce the problem:

Open Blender [Version Number].
Set up a scene with videos, images, sounds, or Alembic caches.
Run the Gather Resources script.
Check if all files were copied to the textures/ folder and paths were correctly updated.

#### 3. Expected vs. Actual Behavior
Expected Behavior: (E.g., "Files should be copied to the 'textures' folder, and their paths updated to relative links.")
Actual Behavior: (E.g., "Files remained in their original location, or the paths were not updated.")

#### 4. System Information


Operating System: (E.g., Windows 11, Ubuntu 22.04, macOS 13)
CPU: (E.g., Intel Core i9-13900HX)
GPU: (E.g., NVIDIA RTX 4070)
RAM: (E.g., 32GB)
Blender Version: (E.g., 4.0.1, 3.6.5)
5. Files and Formats Involved
Were all file types handled correctly?
(E.g., "The script copied image files, but skipped .abc files.")
Relevant Formats in Use: (Check all that apply)
 Video (.mp4, .mkv, etc.)
 Image (.png, .jpg, etc
.)
 Audio (.wav, .mp3, etc.)
 Alembic (.abc)
 3D Models (.fbx, .obj, etc.)

#### 6. Error Messages or Console Output
Were there any errors? (If yes, provide the exact error message or attach a screenshot of the console output.)

#### 7. Workarounds or Attempts to Fix (If Any)
What have you tried so far? (E.g., “Tried running the script on a fresh project, but the issue persists.”)

#### 8. Additional Context or Observations
How often does the issue occur? (E.g., Every time, or intermittently?)
Is this project-specific? (Does the problem happen in only one project or across multiple?)
