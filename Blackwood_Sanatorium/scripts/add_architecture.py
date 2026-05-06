from pxr import Usd, UsdGeom, Gf, Sdf

stage = Usd.Stage.Open("data/layers/environment.usda")

# 1. Clean up
if stage.GetPrimAtPath("/Sanatorium/Geom/Walls"):
    stage.RemovePrim("/Sanatorium/Geom/Walls")

walls_path = "/Sanatorium/Geom/Walls"
walls_scope = UsdGeom.Scope.Define(stage, walls_path)

def create_wall_box(name, pos, scale):
    w = UsdGeom.Cube.Define(stage, f"{walls_path}/{name}")
    w.AddTranslateOp().Set(pos)
    w.AddScaleOp().Set(scale)
    return w

# --- 1. BACK & RIGHT WALLS (Solid) ---
create_wall_box("BackWall", Gf.Vec3d(0, 2.5, -5), Gf.Vec3d(5, 2.5, 0.1))
create_wall_box("RightWall", Gf.Vec3d(5, 2.5, 0), Gf.Vec3d(0.1, 2.5, 5))

# --- 2. LEFT WALL (The Window "Frame") ---
create_wall_box("Left_Start", Gf.Vec3d(-5, 2.5, -3.5), Gf.Vec3d(0.1, 2.5, 1.5)) # Wall segment
create_wall_box("Left_End",   Gf.Vec3d(-5, 2.5, 3.5),  Gf.Vec3d(0.1, 2.5, 1.5)) # Wall segment
create_wall_box("Left_Bottom", Gf.Vec3d(-5, 0.75, 0),  Gf.Vec3d(0.1, 0.75, 2.0)) # Under window
create_wall_box("Left_Top",    Gf.Vec3d(-5, 4.25, 0),  Gf.Vec3d(0.1, 0.75, 2.0)) # Over window

# --- WINDOW BARS ---
# 1. The Vertical Bars
for i in range(-3, 4):
    bar = UsdGeom.Cylinder.Define(stage, f"{walls_path}/VerticalBar_{i+3}")
    bar.GetRadiusAttr().Set(0.04)
    bar.GetHeightAttr().Set(2.8) 
    bar.AddTranslateOp().Set(Gf.Vec3d(-5, 2.5, i * 0.5))
    bar.AddRotateXOp().Set(90) # Rotate to be vertical

# 2. THE HORIZONTAL BAR
h_bar = UsdGeom.Cylinder.Define(stage, f"{walls_path}/HorizontalBar")
h_bar.GetRadiusAttr().Set(0.045) # Slightly thicker to look like a support
h_bar.GetHeightAttr().Set(4.0)   # Matches the width of the window gap
h_bar.AddTranslateOp().Set(Gf.Vec3d(-5, 2.5, 0))

# --- 3. FRONT WALL (The Door "Frame") ---
# Wall to the left of door
create_wall_box("Front_Left", Gf.Vec3d(-3, 2.5, 5), Gf.Vec3d(2, 2.5, 0.1))
# Wall to the right of door
create_wall_box("Front_Right", Gf.Vec3d(3, 2.5, 5), Gf.Vec3d(2, 2.5, 0.1))
# The Header above the door
create_wall_box("Front_Header", Gf.Vec3d(0, 4.5, 5), Gf.Vec3d(1, 0.5, 0.1))

# --- 4. THE HINGED DOOR ---
door_hinge = UsdGeom.Xform.Define(stage, f"{walls_path}/DoorHinge")
# Position hinge at the edge of the opening (X=-1, Z=5)
door_hinge.AddTranslateOp().Set(Gf.Vec3d(-1.0, 0, 5)) 
rotate_op = door_hinge.AddRotateYOp()

door_mesh = UsdGeom.Cube.Define(stage, f"{walls_path}/DoorHinge/DoorMesh")
# Door is 2m wide, so offset center by 1m so edge stays at hinge
door_mesh.AddTranslateOp().Set(Gf.Vec3d(1.0, 2.0, 0)) 
door_mesh.AddScaleOp().Set(Gf.Vec3d(1.0, 2.0, 0.05))

for frame in range(1, 101):
    angle = 0 if frame < 30 else min(110, (frame - 30) * 3)
    rotate_op.Set(angle, frame)

stage.GetRootLayer().Save()