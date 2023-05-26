import bpy
from bpy.props import FloatVectorProperty, IntProperty, FloatProperty
from bpy.types import Operator
import math
from . import Helper_Functions


class Add_Object:

    @staticmethod
    def add_object(self):
        # Create curve object
        street_curve = bpy.data.curves.new('BezierCurve', 'CURVE')
        street_curve.dimensions = '3D'

        # Create a new spline for the curve
        spline = street_curve.splines.new('BEZIER')
        spline.bezier_points.add(self.cuts + 1)

        Helper_Functions.define_control_points(self.start_point, self.end_point, spline)

        # Which parts of the curve to extrude ['HALF', 'FRONT', 'BACK', 'FULL'].
        street_curve.fill_mode = 'HALF'
        # Breadth of extrusion, modified by lanes
        street_curve.extrude = 0.125 * self.lanes
        # create object out of curve
        obj = bpy.data.objects.new('StreetObject', street_curve)
        # Tilt curve by 90 degrees
        obj.rotation_euler[0] = math.radians(90)
        # Set origin right between start and end points (How tf does it work?!)

        # link to scene-collection
        collection = bpy.data.collections.get('Collection')
        if (collection):
            collection.objects.link(obj)
        else:
            bpy.context.scene.collection.objects.link(obj)


    


class OBJECT_OT_add_object(Operator):
    """Create a new Street Object"""
    bl_idname = "mesh.add_object"
    bl_label = "Add Street Object"
    bl_options = {'REGISTER', 'UNDO'}

    def __init__(self) -> None:
        super().__init__()

    start_point: FloatVectorProperty(
        name="Start Point",
        default=(0.0, 0.0, 0.0),
        subtype='XYZ',
        description="Choose a point where the street should begin",
    )
    end_point: FloatVectorProperty(
        name="End Point",
        default=(4.0, 0.0, 0.0),
        subtype='XYZ',
        description="Choose a point where the street should end",
    )
    lanes: IntProperty(
        name="Lanes",
        description="Number of lanes the street should have",
        default=1,
        min=1,
        max=4,
        subtype='UNSIGNED',
    )
    cuts: IntProperty(
        name="Control Points",
        description="Number of control points between start and end point",
        default=2,
        min=1,
        max=100,
        subtype='UNSIGNED',
    )

    def execute(self):
        Add_Object.add_object(self)
        return {'FINISHED'}
