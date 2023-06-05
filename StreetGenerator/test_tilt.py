import bpy


test_curve = bpy.data.curves.new('BezierCurve', 'CURVE')
test_curve.dimensions = '3D'

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
# link to scene-collection
collection = bpy.data.collections.get('Collection')
if (collection):
    collection.objects.link(obj)
else:
    bpy.context.scene.collection.objects.link(obj)

bpy.data.objects["TestCurve"].select_set(True)
bpy.ops.curve.select_all(action='SELECT')
bpy.ops.transform.tilt(value=1.5708, mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', 
                        proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False)