import xml.etree.ElementTree as ET
import bpy
import numpy as np
import math

# Parse the XML file
tree = ET.parse("BlenderImportPipeline/testMaps/oneRoad.osm")

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

node_dict = {}
# Get the root element>
root = tree.getroot()

blockScale = (1, 1, 1)

mat = bpy.data.materials.new("Blue")

# Activate its nodes
mat.use_nodes = True

# Get the principled BSDF (created by default)
principled = mat.node_tree.nodes['Principled BSDF']

# Assign the color
principled.inputs['Base Color'].default_value = (0,0,1,1)

firstNodeLocation = ()
scalingFactor = 10000
# Iterate over the child elements of the root
for child in root:
    if (child.tag == "node"):
        # Store first node location, used for centering map
        if (firstNodeLocation == ()):
            lat = child.attrib.get("lat")
            lon = child.attrib.get("lon")
            firstNodeLocation = (np.float64(lat), np.float64(lon))
        # Store key and value pairs
        keyString = child.attrib.get("id")
        valueString = child.attrib.get("lat") + " " + child.attrib.get("lon")
        node_dict[keyString] = valueString
    elif (child.tag == "way"):
        previousNode = None
        for c in child:
            nodeRef = c.attrib.get("ref")
            if previousNode == None:
                previousNode = nodeRef
                curNode = None
                continue
            if nodeRef != None and previousNode != None:
                curNode = nodeRef
                prevNode = node_dict[previousNode]
                currentNode = node_dict[nodeRef]

                prevLat, prevLon = prevNode.split()
                curLat, curLon = currentNode.split()

                prevNodePos = ((np.float64(prevLat) - firstNodeLocation[0]) * scalingFactor, (np.float64(prevLon) - firstNodeLocation[1]) * scalingFactor, 0)
                curNodePos = ((np.float64(curLat) - firstNodeLocation[0]) * scalingFactor, (np.float64(curLon) - firstNodeLocation[1]) * scalingFactor, 0)

                blockPos = (prevNodePos[0] + (curNodePos[0] - prevNodePos[0])/2, prevNodePos[1] + (curNodePos[1] - prevNodePos[1])/2, 0)
                rot = angle_between(blockPos, prevNodePos) * scalingFactor + math.pi/2
                scl = math.dist(prevNodePos, blockPos) 
                # fittedLat = (np.float64(lat) -
                #              firstNodeLocation[0]) * scalingFactor
                # fittedLon = (np.float64(lon) -
                #              firstNodeLocation[1]) * scalingFactor
                #print(fittedLat, " ", fittedLon)
                bpy.ops.mesh.primitive_cube_add(location=blockPos, scale=(scl, 1, 1), rotation=(0, 0, rot))
                previousNode = curNode
            elif nodeRef == None:
               previousNode = None
               continue
    # elif (child.tag == "way"):
    #     for c in child:
    #         nodeRef = c.attrib.get("ref")
    #         if (nodeRef != None):
    #             node = node_dict[nodeRef]
    #             lat, lon = node.split()
    #             fittedLat = (np.float64(lat) -
    #                          firstNodeLocation[0]) * scalingFactor
    #             fittedLon = (np.float64(lon) -
    #                          firstNodeLocation[1]) * scalingFactor
    #             #print(fittedLat, " ", fittedLon)
    #             bpy.ops.mesh.primitive_cube_add(
    #                 location=(fittedLat, fittedLon, 0), scale=blockScale)
    #             obj = bpy.context.object
    #             obj.color = (0,0,1,1)
    #             obj.data.materials.append(mat)
    #         else:
    #             continue
