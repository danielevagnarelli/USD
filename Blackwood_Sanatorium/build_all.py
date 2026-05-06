import os
import subprocess

# Get the directory where THIS script is located (The root folder)
root_dir = os.path.dirname(os.path.abspath(__file__))

scripts = [
    "scripts/build_stage.py",
    "scripts/build_materials.py",
    "scripts/add_architecture.py",
    "scripts/build_bed_asset.py",
    "scripts/assemble_sanatorium.py",
    "scripts/add_debris.py",
    "scripts/add_lighting.py",
    "scripts/apply_materials.py"
]

print("--- STARTING BLACKWOOD SANATORIUM BUILD ---")

for script_rel_path in scripts:
    # Combine root dir with the relative script path
    full_script_path = os.path.join(root_dir, script_rel_path)
    
    print(f"Running: {script_rel_path}...")
    
    # Set 'cwd=root_dir' so the scripts know where 'data/' is located
    result = subprocess.run(["python", full_script_path], cwd=root_dir, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"  \033[32m Successfully finished {script_rel_path}\033[0m")
    else:
        print(f" \033[31m ERROR in {script_rel_path}:\033[0m")
        print(result.stderr)

print("--- BUILD COMPLETE ---")