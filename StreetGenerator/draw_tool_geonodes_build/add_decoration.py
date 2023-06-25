# https://blender.stackexchange.com/questions/278948/coons-patch-bezier-curve
# https://www.youtube.com/watch?v=Ve9h7-E8EuM
# https://www.youtube.com/watch?v=aVwxzDHniEw&t=143s
# source (bc. I can't come up with that shit on my own...| me neighter): https://behreajj.medium.com/scripting-curves-in-blender-with-python-c487097efd13
# Missing (for the street to have basic functionality):
# -Allow users to reopen the properties panel
# -Scaling of Street-Curve
# -Name of Object
# -extrude along Y-Axis

from mathutils import geometry, Vector, Matrix
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from bpy.props import FloatVectorProperty, IntProperty
from bpy.types import Operator
import bpy
import pathlib

def get_script_dir(): 
    script_path = __file__
    script_dir = pathlib.Path(script_path).resolve().parent
    return script_dir

def add_decoration(self, curve):

    # bpy.ops.object.mode_set(mode='OBJECT')

    for obj in bpy.data.objects:
        obj.select_set(False)
    
    # Create plane.
    bpy.ops.mesh.primitive_plane_add(calc_uvs=True, size=0.1)
    plane1 = bpy.context.active_object

    script_dir = get_script_dir()
    treepath = (script_dir / "Objects/Tree.obj")
    # img = bpy.data.images.load(treepath.__str__())
    
    bpy.ops.wm.obj_import(filepath="C:/GitHub/DVMP_FuwaTwin/StreetGenerator/Objects/Tree.obj",
                         directory="C:/GitHub/DVMP_FuwaTwin/StreetGenerator/Objects/", files=[{"name": "Tree.obj", "name": "Tree.obj"}])
    # bpy.ops.wm.obj_import(filepath=treepath,
    #                       directory=script_dir + "/Objects/", files=[{"name": "Tree.obj", "name": "Tree.obj"}])
    tree1 = bpy.context.active_object
    tree1.scale = (0.1, 0.1, 0.1)
    tree1.parent = plane1
    tree1.hide_set(True)
    plane1.instance_type = 'FACES'

    bpy.ops.mesh.primitive_plane_add(calc_uvs=True, size=0.1)
    plane2 = bpy.context.active_object
    # bpy.ops.object.mode_set(mode='EDIT')
    # bpy.ops.mesh.merge(type='CENTER')
    # bpy.ops.object.mode_set(mode='OBJECT')
    #bpy.ops.wm.obj_import(filepath=treepath,
    #                      directory=script_dir + "/Objects/", files=[{"name": "Tree.obj", "name": "Tree.obj"}])
    bpy.ops.wm.obj_import(filepath="C:/GitHub/DVMP_FuwaTwin/StreetGenerator/Objects/Tree.obj",
                         directory="C:/GitHub/DVMP_FuwaTwin/StreetGenerator/Objects/", files=[{"name": "Tree.obj", "name": "Tree.obj"}])
    tree2 = bpy.context.active_object

    tree2.scale = (0.1, 0.1, 0.1)
    tree2.parent = plane2
    tree2.hide_set(True)
    plane2.instance_type = 'FACES'

    # Append modifiers.
    array_mod1 = plane1.modifiers.new(name='Array', type='ARRAY')
    curve_mod1 = plane1.modifiers.new(name='Curve', type='CURVE')

    # Array modifier properties.
    array_mod1.fit_type = 'FIT_CURVE'
    array_mod1.curve = curve
    array_mod1.use_relative_offset = True
    # array_mod1.relative_offset_displace = (self.tree_distance, 0.0, 0.0) # Adjust the offset values here (x, y, z).
    # Adjust the offset values here (x, y, z).
    array_mod1.relative_offset_displace = (3, 0.0, 0.0)

    # Curve modifier properties.
    curve_mod1.object = curve
    curve_mod1.deform_axis = 'POS_X'

    plane1.location[1] = 0.5

    array_mod2 = plane2.modifiers.new(name='Array', type='ARRAY')
    curve_mod2 = plane2.modifiers.new(name='Curve', type='CURVE')

    # Array modifier properties.
    array_mod2.fit_type = 'FIT_CURVE'
    array_mod2.curve = curve
    array_mod2.use_relative_offset = True
    array_mod2.relative_offset_displace = (3, 0.0, 0.0)

    # Curve modifier properties.
    curve_mod2.object = curve
    curve_mod2.deform_axis = 'POS_X'

    plane2.location[1] = -0.5

    plane1.select_set(True)
    bpy.ops.object.duplicates_make_real()
    bpy.ops.object.select_all(action='DESELECT')

    plane2.select_set(True)
    bpy.ops.object.duplicates_make_real()
    bpy.ops.object.select_all(action='DESELECT')

    for obj in bpy.data.objects:
        # Check if the object's name contains "tree"
        if "tree" in obj.name.lower():
            print("fount tree")
            # Select the object
            obj.select_set(True)
            obj.rotation_euler[1] = 0
            bpy.ops.object.select_all(action='DESELECT')