import bpy

# Define a custom handler function to apply the tilt
def handle_spline_draw(context):
    # Access the active object (the drawn splines)
    active_object = bpy.context.active_object

    # Check if the active object is a curve type
    if active_object is not None and active_object.type == 'CURVE' and bpy.context.tool_settings.mesh_tools.current_tool == "builtin.draw":
        # Iterate over each spline in the object
        for spline in active_object.data.splines:
            # Iterate over each point in the spline
            for point in spline.points:
                # Modify the tilt by 90 degrees
                point.tilt += 1.5708  # 90 degrees in radians

        # unregister the handler function
        bpy.app.handlers.depsgraph_update_post.remove(handle_spline_draw)

# Register the handler function
bpy.app.handlers.depsgraph_update_post.append(handle_spline_draw)

# Start the drawing tool
bpy.ops.wm.tool_set_by_id(name="builtin.draw")