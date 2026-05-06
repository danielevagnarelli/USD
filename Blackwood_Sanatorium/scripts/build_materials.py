from pxr import Usd, UsdShade, UsdGeom, Gf, Sdf

path = "data/layers/materials.usda"
stage = Usd.Stage.CreateNew(path)

# Create a Scope to keep the stage tree clean
UsdGeom.Scope.Define(stage, "/Sanatorium/Materials")

def create_preview_material(name, diffuse, roughness, metallic=0.0):
    mat_path = f"/Sanatorium/Materials/{name}"
    material = UsdShade.Material.Define(stage, mat_path)
    
    # Create the Shader (UsdPreviewSurface is the industry standard)
    shader = UsdShade.Shader.Define(stage, f"{mat_path}/Shader")
    shader.CreateIdAttr("UsdPreviewSurface")
    
    # Set Properties
    shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set(diffuse)
    shader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(roughness)
    shader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(metallic)
    
    # Connect Shader to Material Surface
    material.CreateSurfaceOutput().ConnectToSource(shader.ConnectableAPI(), "surface")
    return material

# --- THE SANATORIUM PALETTE ---

# FLOOR: Let's increase roughness to 0.6 (dusty tile) and slightly brighten color
# This makes reflections "blurry" and soft.
create_preview_material("Linoleum_Floor", (0.2, 0.2, 0.2), 0.6)

# PILLS: Stay bright and shiny
create_preview_material("Pill_Plastic", (0.8, 0.8, 0.8), 0.05)

# BEDS/BARS: Keep metallic but increase roughness to 0.5 (rusty/corroded steel)
# Smooth steel is black, but rough steel scatters light and looks "steelier."
create_preview_material("Surgical_Steel", (0.2, 0.2, 0.2), 0.5, metallic=1.0)

stage.GetRootLayer().Save()