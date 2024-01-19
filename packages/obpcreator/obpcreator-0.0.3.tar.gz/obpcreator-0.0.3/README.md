# Installation
Install it by cloning the git reprository or from PyPi using:
```bash
pip install obpcreator
```


# Example from pyvista cube
```bash
import pyvista as pv
import obpcreator.support_functions.pv_mesh_manipulation as pv_mesh_manipulation
from obpcreator import data_model, point_infill_creation, generate_build

path = r"C:\Users\antwi87\Downloads\OneDrive_1_1-17-2024 (1)\STL"
mesh1 = pv.Cube(center=(0,0,5), x_length=10, y_length=10, z_length=10)

meshes = [mesh1]

infill_setting = data_model.ScanParameters(
    spot_size = 10, #[-] 1-100
    beam_power = 660, #[W]
    scan_speed = 2031000, #[micrometers/second]
    dwell_time = 515000, #[ns]
    )
infill = data_model.Infill(
    beam_settings = infill_setting,
    scan_strategy = "point_random",
    strategy_settings = {}
    )
parts = []
for i in range(len(meshes)):
    print("slicing part ", i+1, " out of ", len(meshes))
    point_geometry = point_infill_creation.create_from_pyvista_mesh(meshes[i], 0.3, 0.07, start_angle=0, rotation_angle=0, uniform_point_dist=True, offset_margin=1)
    print("sliced part ", i+1, " out of ", len(meshes))
    part1 = data_model.Part(
        point_geometry = point_geometry,
        infill_setting = infill
    )
    parts.append(part1)

build = data_model.Build(
    parts = parts,
    layer_height = 0.07 #mm
)
out_path = r"C:\Users\antwi87\Downloads\slicer_test\output2"
generate_build.generate_build(build, out_path)
```




# To package
- Delete old builds in the \dist folder 
- Update the version in the setup.cfg file
- run "python -m build"
- upload to pip with "twine upload dist/*"
