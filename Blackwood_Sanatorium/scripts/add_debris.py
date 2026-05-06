from pxr import Usd, UsdGeom, Gf
import random

# 1. SETUP STAGE
stage = Usd.Stage.Open("data/layers/props.usda")

# 2. DEFINE DIMENSIONS 
PILL_RADIUS = 0.03
FLOOR_TOP_Y = 0.005  # This matches the floor math (0.01 scale / 2)

# 3. DEFINE PROTOTYPE
proto_path = "/Sanatorium/Props/Prototypes/Pill"
pill = UsdGeom.Sphere.Define(stage, proto_path)
pill.GetRadiusAttr().Set(PILL_RADIUS)
pill.ClearXformOpOrder()
pill.AddScaleOp().Set((2.0, 1.0, 1.0)) # Still a capsule

# 4. CALCULATE PLACEMENT Y
# The pill's center must be its radius + the floor's height 
# to sit perfectly on top without compenetrating.
calc_y = FLOOR_TOP_Y + PILL_RADIUS

# 5. CONSTRUCT INSTANCER
instancer_path = "/Sanatorium/Props/DebrisField"
instancer = UsdGeom.PointInstancer.Define(stage, instancer_path)
instancer.GetPrototypesRel().SetTargets([proto_path])

# 6. ASSIGN POSITIONS USING THE CALCULATED Y
random_positions = []
for _ in range(20):
    x = random.uniform(-4.5, 4.5)
    z = random.uniform(-4.5, 4.5)
    random_positions.append(Gf.Vec3f(x, calc_y, z))

instancer.GetPositionsAttr().Set(random_positions)
instancer.GetProtoIndicesAttr().Set([0] * 20) # Automatically matches count

stage.GetRootLayer().Save()
print(f"Debris updated! Pills are {PILL_RADIUS} size and sitting at Y={calc_y}")