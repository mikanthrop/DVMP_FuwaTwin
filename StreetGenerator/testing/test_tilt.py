import bpy


test_curve = bpy.data.curves.new('BezierCurve', 'CURVE')
test_curve.dimensions = '3D'


 # switch all open 3d views to view scene from top -> drawn street lays on ground
for area in bpy.context.screen.areas:
    if area.type == "VIEW_3D":
        override = bpy.context.copy()
        override["area"] = area
        bpy.ops.view3d.view_axis(override, type='TOP', align_active=False) 
        if  area.spaces.active.region_3d.is_perspective:
            bpy.ops.view3d.view_persportho(override)
        else:
            pass


spline = test_curve.splines.new('BEZIER')
spline.bezier_points.add(4)

for i in range(0, len(spline.bezier_points)):
    spline.bezier_points[i].co = (i, 0, 0)
    spline.bezier_points[i].handle_left = (i-0.1, 0, 0)
    spline.bezier_points[i].handle_right = (i+0.1, 0, 0)

# Which parts of the curve to extrude ['HALF', 'FRONT', 'BACK', 'FULL'].
test_curve.fill_mode = 'HALF'
# Breadth of extrusion, modified by lanes
test_curve.extrude = 0.125
# create object out of curve
obj = bpy.data.objects.new('TestCurve', test_curve)
selected_obj = obj
# link to scene-collection and select obj
collection = bpy.data.collections.get('Collection')
if (collection):
    collection.objects.link(obj)
    selected_obj = collection.objects[0]
    selected_obj.select_set(True)
else:
    bpy.context.scene.collection.objects.link(obj)
    selected_obj = bpy.context.scene.collection.objects[0]
    selected_obj.select_set(True)


 # Set the context for the operator
bpy.context.view_layer.objects.active = selected_obj
# Toggle to Edit Mode
bpy.ops.object.editmode_toggle()
bpy.ops.wm.tool_set_by_id(name="builtin.draw")

# Define a custom handler function to apply the tilt
def handle_spline_draw(context):
    # Access the active object (the drawn splines)
    for curve in bpy.data.curves:

        if curve == test_curve:
            for spline in curve.splines:
                
                if spline.type != 'BEZIER':
                    print('only bezier splines allowed')
                    continue
                
                total_points = len(spline.bezier_points)
                if total_points == 0:
                    continue
                
                # Iterate over each point in the spline
                for point in spline.bezier_points:
                    # Modify the tilt by 90 degrees
                    point.tilt = 1.5708  # 90 degrees in radians
    

# Register the handler function
bpy.app.handlers.depsgraph_update_post.append(handle_spline_draw)


# bpy.ops.curve.select_all(action='SELECT')
# bpy.ops.transform.tilt(value=1.5708, mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', 
#                         proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False)
