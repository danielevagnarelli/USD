from pxr import Usd, UsdShade

# Open the main stage where all layers are composed
stage = Usd.Stage.Open("data/main.usda")

def bind_mat(prim_path, mat_path):
    """Helper to bind a material to a specific prim path"""
    prim = stage.GetPrimAtPath(prim_path)
    mat_prim = stage.GetPrimAtPath(mat_path)
    if prim and mat_prim:
        UsdShade.MaterialBindingAPI(prim).Bind(UsdShade.Material(mat_prim))

# 1. DEFINE MATERIAL OBJECTS
# Fetch these once to reuse them in loops
mat_steel = UsdShade.Material(stage.GetPrimAtPath("/Sanatorium/Materials/Surgical_Steel"))
mat_floor = UsdShade.Material(stage.GetPrimAtPath("/Sanatorium/Materials/Linoleum_Floor"))
mat_pill  = UsdShade.Material(stage.GetPrimAtPath("/Sanatorium/Materials/Pill_Plastic"))

# 2. STATIC BINDINGS
# Floor
bind_mat("/Sanatorium/Geom/Floor", "/Sanatorium/Materials/Linoleum_Floor")

# Pill Prototype (Affects all instances)
bind_mat("/Sanatorium/Props/Prototypes/Pill", "/Sanatorium/Materials/Pill_Plastic")

# Beds
bind_mat("/Sanatorium/Props/Bed_01", "/Sanatorium/Materials/Surgical_Steel")
bind_mat("/Sanatorium/Props/Bed_02", "/Sanatorium/Materials/Surgical_Steel")

# 3. DYNAMIC ARCHITECTURE BINDINGS
# Bind the main Walls group to the Floor/Concrete material first
walls_group = stage.GetPrimAtPath("/Sanatorium/Geom/Walls")
if walls_group:
    UsdShade.MaterialBindingAPI(walls_group).Bind(mat_floor)
    
    # Loop through the children of Walls to find Bars and the Door
    for child in walls_group.GetChildren():
        child_name = child.GetName()
        
        # If the object name contains 'Bar', make it Steel
        if "Bar" in child_name:
            UsdShade.MaterialBindingAPI(child).Bind(mat_steel)
            
        # If it's the DoorHinge or DoorMesh, make it Steel too (or whichever you prefer)
        if "Door" in child_name:
            UsdShade.MaterialBindingAPI(child).Bind(mat_steel)

# Save the changes to the root layer
stage.GetRootLayer().Save()
print("--- LookDev: All Materials and Architecture Bindings Applied ---")