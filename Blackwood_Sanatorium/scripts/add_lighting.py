from pxr import Usd, UsdLux, Gf, UsdGeom
import random

stage = Usd.Stage.Open("data/layers/lighting.usda")

# 1. Lights setup
ambient = UsdLux.DomeLight.Define(stage, "/Sanatorium/Lights/AmbientGlow")
ambient.GetIntensityAttr().Set(100) 
ambient.GetColorAttr().Set(Gf.Vec3f(0.05, 0.05, 0.08)) 
ambient.CreateVisibilityAttr().Set("inherited")

light_path = "/Sanatorium/Lights/FlickerLight"
light = UsdLux.DiskLight.Define(stage, light_path)
light.ClearXformOpOrder()
light.AddTranslateOp().Set(Gf.Vec3d(0, 3.0, 0)) 
light.AddRotateXOp().Set(-90) 
light.GetRadiusAttr().Set(0.5)

intensity_attr = light.GetIntensityAttr()
color_attr = light.GetColorAttr()

WHITE = Gf.Vec3f(1.0, 1.0, 1.0)
RED   = Gf.Vec3f(1.0, 0.0, 0.0)

# 2. Animation Logic
for frame in range(1, 101):
    # --- PHASE 1: Normal Rhythmic Flicker (Frames 1-45) ---
    if frame <= 45:
        if frame % 3 == 0:
            roll = random.random()
            intensity = 0 if roll < 0.15 else (150000 if roll < 0.20 else 40000)
        else:
            intensity = 40000
        color = WHITE

    # --- PHASE 2: THE "DYING BREATH" (Frames 46-55) ---
    # Rapid-fire unstable flickering right before the break
    elif 46 <= frame <= 55:
        # Every frame is a random state to create a "buzzing" visual effect
        intensity = random.choice([0, 180000, 0, 10000, 200000]) 
        color = WHITE

    # --- PHASE 3: TOTAL BLACKOUT (Frames 56-65) ---
    elif 56 <= frame <= 65:
        intensity = 0
        color = WHITE

    # --- PHASE 4: THE RED SURGE (Frames 66-85) ---
    elif 66 <= frame <= 85:
        intensity = 120000 
        color = RED

    # --- PHASE 5: RECOVERY (Frames 86-100) ---
    else:
        # Subtle white flicker as it tries to come back to life
        intensity = 60000 if (frame % 2 == 0) else 5000
        color = WHITE
    
    intensity_attr.Set(intensity, frame)
    color_attr.Set(color, frame)

# Set defaults for static view
intensity_attr.Set(40000)
color_attr.Set(WHITE)

stage.GetRootLayer().Save()
print("Sequence Updated: Added rapid pre-blackout jitter phase!")