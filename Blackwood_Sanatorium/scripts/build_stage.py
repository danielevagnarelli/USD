import os
from pxr import Usd, UsdGeom, Sdf, Kind

# 1. Define paths for Python to WRITE the files (relative to script execution)
# We assume this script is run from the root folder 'Blackwood_Sanatorium/'
main_disk_path = "data/main.usda"
env_disk_path = "data/layers/environment.usda"
props_disk_path = "data/layers/props.usda"
lights_disk_path = "data/layers/lighting.usda"

# Ensure the directories exist before creating files
os.makedirs("data/layers", exist_ok=True)
os.makedirs("data/assets", exist_ok=True)

# Create the physical stages on disk
stage_main = Usd.Stage.CreateNew(main_disk_path)
stage_env = Usd.Stage.CreateNew(env_disk_path)
stage_props = Usd.Stage.CreateNew(props_disk_path)
stage_lights = Usd.Stage.CreateNew(lights_disk_path)

# 2. Setup main.usda Metadata & Composition
# From the perspective of 'data/main.usda', these are the relative paths:
rel_env_path = "./layers/environment.usda"
rel_props_path = "./layers/props.usda"
rel_lights_path = "./layers/lighting.usda"
rel_mats_path = "./layers/materials.usda"

root_layer = stage_main.GetRootLayer()
root_layer.subLayerPaths.append(rel_env_path)
root_layer.subLayerPaths.append(rel_props_path)
root_layer.subLayerPaths.append(rel_lights_path)
root_layer.subLayerPaths.append(rel_mats_path)

# Set the Stage Metadata
stage_main.SetMetadata('comment', 'Blackwood Sanatorium: Initial Layer Setup')
UsdGeom.SetStageUpAxis(stage_main, UsdGeom.Tokens.y)
UsdGeom.SetStageMetersPerUnit(stage_main, 0.01)

stage_main.SetStartTimeCode(1)
stage_main.SetEndTimeCode(100)

# Set the playback speed
stage_main.SetFramesPerSecond(24)
stage_main.SetTimeCodesPerSecond(24)

# 3. Define the Model Hierarchy
# Create the root Xform and set its Kind to 'assembly'
sanatorium_path = Sdf.Path("/Sanatorium")
sanatorium_prim = UsdGeom.Xform.Define(stage_main, sanatorium_path)
Usd.ModelAPI(sanatorium_prim).SetKind(Kind.Tokens.assembly)

# Instead of 'Define' (which blocks sublayers), we use 'OverridePrim' (over)
# This allows the content in props.usda and environment.usda to "shine through"
stage_main.OverridePrim("/Sanatorium/Geom")
stage_main.OverridePrim("/Sanatorium/Props")
stage_main.OverridePrim("/Sanatorium/Lights")

# 4. Create Content in Environment Layer
# We define a cube in the environment layer to represent the floor
placeholder_cube = UsdGeom.Cube.Define(stage_env, "/FloorPlaceholder")
# Set a property just to make it distinct
placeholder_cube.GetSizeAttr().Set(1.0) # Base size
# Scale: X=10 (Wide), Y=0.01 (Paper thin), Z=10 (Deep)
placeholder_cube.AddScaleOp().Set((10.0, 0.01, 10.0))
stage_env.Save() 

# 5. Reference that cube into the Main Stage (The 'E' in LIVERPS)
# We place it inside our /Sanatorium/Geom scope
geom_floor_path = "/Sanatorium/Geom/Floor"
floor_prim = stage_main.OverridePrim(geom_floor_path)

# We reference the file using its relative path to main.usda
floor_prim.GetReferences().AddReference(rel_env_path, "/FloorPlaceholder")

# Final Save
stage_main.GetRootLayer().Save()
stage_props.GetRootLayer().Save()
stage_lights.GetRootLayer().Save()

print("--- Sanatorium Stage Architecture Created Successfully ---")
print(f"Created: {main_disk_path}")
print(f"Sublayered: {rel_env_path}, {rel_props_path}, {rel_lights_path}")