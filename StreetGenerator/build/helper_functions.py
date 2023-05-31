import math
import bpy


def define_control_points(start, end, spline):
    # get step-size to distribute control points evenly between start and end
    distance = end - start
    step_size = distance / (len(spline.bezier_points) - 1)

    handle_offset = step_size / 7

    # Set control points for curve
    for i in range(len(spline.bezier_points)):
        if (i == 0):
            spline.bezier_points[i].co = start
            spline.bezier_points[i].handle_left = (
                (start.x-handle_offset.x), (start.y-handle_offset.y), (start.z-handle_offset.z))
            spline.bezier_points[i].handle_right = (
                (start.x+handle_offset.x), (start.y+handle_offset.y), (start.z+handle_offset.z))
        elif (i == (len(spline.bezier_points) - 1)):
            spline.bezier_points[i].co = end
            spline.bezier_points[i].handle_left = (
                (end.x-handle_offset.x), (end.y-handle_offset.y), (end.z-handle_offset.z))
            spline.bezier_points[i].handle_right = (
                (end.x+handle_offset.x), (end.y+handle_offset.y), (end.z+handle_offset.z))
        else:
            current = start + (step_size * i)
            spline.bezier_points[i].co = (current.x, current.y, current.z)
            spline.bezier_points[i].handle_left = (
                (current.x-handle_offset.x), (current.y-handle_offset.y), (current.z-handle_offset.z))
            spline.bezier_points[i].handle_right = (
                (current.x+handle_offset.x), (current.y+handle_offset.y), (current.z+handle_offset.z))
            

def assign_road_material(lanes):
    road_mat = bpy.data.materials.new("Road Material")
    road_mat.use_nodes = True
    nodes = road_mat.node_tree.nodes

    imgpath = "/Users/leonprivat/Documents/GitHub/DVMP_FuwaTwin/StreetGenerator/build/textures/Road_texture.jpg"
    img = bpy.data.images.load(imgpath)

    principled_BSDF = nodes.get('Principled BSDF')
    tex_node: bpy.types.Node = nodes.new('ShaderNodeTexImage')
    tex_node.image = img
    
    road_mat.node_tree.links.new(tex_node.outputs[0], principled_BSDF.inputs[0])
    bpy.context.object.data.materials.append(road_mat)



def get_unit_vec(start, end, factor):
    vec = end - start
    vec_len = math.sqrt(math.pow(vec.x, 2) +
                        math.pow(vec.y, 2)+math.pow(vec.z, 2))
    if (vec_len == 0):
        return (0, 0, 0)
    else:
        unit_vec = vec / vec_len
        return unit_vec*factor