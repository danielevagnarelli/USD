from pxr import Usd, UsdGeom, Gf

# 1. Open the layer
stage = Usd.Stage.Open("data/layers/props.usda")
bed_asset_path = "../assets/patient_bed.usda"

# --- BED 01: CLEAN ---
bed1 = UsdGeom.Xform.Define(stage, "/Sanatorium/Props/Bed_01")
bed1.GetPrim().GetReferences().AddReference(bed_asset_path)
# Move it Left and UP (so it's not inside the floor cube)
# Floor is size 2, so Y=1.0 is the "ground"
bed1.AddTranslateOp().Set(Gf.Vec3d(-3.0, 0.11, 0.0))

# --- BED 02: ABANDONED ---
bed2 = UsdGeom.Xform.Define(stage, "/Sanatorium/Props/Bed_02")
bed2.GetPrim().GetReferences().AddReference(bed_asset_path)
vset = bed2.GetPrim().GetVariantSets().GetVariantSet("state")
vset.SetVariantSelection("abandoned")
# Move it Right and UP
bed2.AddTranslateOp().Set(Gf.Vec3d(3.0, 0.06, 0.0))

stage.GetRootLayer().Save()