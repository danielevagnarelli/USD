from pxr import Usd, UsdGeom, Sdf, Kind

# 1. DISK PATH: Where Python saves the file
bed_disk_path = "data/assets/patient_bed.usda"
stage = Usd.Stage.CreateNew(bed_disk_path)

# 2. SCENEGRAPH PATH: The "Prim" name inside the file
# We use /PatientBed, NOT the folder name
root_path = "/PatientBed"
root_prim = UsdGeom.Xform.Define(stage, root_path)

# Use the proper Kind.Tokens for component
Usd.ModelAPI(root_prim).SetKind(Kind.Tokens.component)

# Set Default Prim (essential for referencing later!)
stage.SetDefaultPrim(root_prim.GetPrim())

# 3. SETUP VARIANT SET
vset = root_prim.GetPrim().GetVariantSets().AddVariantSet("state")
vset.AddVariant("clean")
vset.AddVariant("abandoned")

# 4. AUTHORING VARIANTS
# Logic: We use the EXACT SAME internal path for both. 
# This is the "magic" of USD.
mattress_path = "/PatientBed/Mattress"

# --- CLEAN VARIANT ---
vset.SetVariantSelection("clean")
with vset.GetVariantEditContext():
    # Inside this variant, Mattress is a Cube
    mattress = UsdGeom.Cube.Define(stage, mattress_path)
    mattress.GetSizeAttr().Set(1.0)
    # Scale it to look like a flat mattress
    mattress.AddScaleOp().Set((2.0, 0.2, 1.0)) 

# --- ABANDONED VARIANT ---
vset.SetVariantSelection("abandoned")
with vset.GetVariantEditContext():
    # Inside THIS variant, the SAME Mattress path is now a Sphere!
    mattress = UsdGeom.Sphere.Define(stage, mattress_path)
    mattress.GetRadiusAttr().Set(0.5)
    # Scale it to look slumped and lumpy
    mattress.AddScaleOp().Set((2.2, 0.1, 1.1))

# 5. Reset to default state and save
vset.SetVariantSelection("clean")
stage.GetRootLayer().Save()

print(f"Successfully created: {bed_disk_path}")