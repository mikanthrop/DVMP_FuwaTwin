import xml.etree.ElementTree as ET
import bpy
import numpy as np

# Parse the XML file
tree = ET.parse("BlenderImportPipeline/testMaps/map.osm")

node_dict = {}

# Get the root element>
root = tree.getroot()

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
        for c in child:
            nodeRef = c.attrib.get("ref")
            if (nodeRef != None):
                node = node_dict[nodeRef]
                print(node)
                lat, lon = node.split()
                fittedLat = (np.float64(lat) - firstNodeLocation[0]) * scalingFactor
                fittedLon = (np.float64(lon) - firstNodeLocation[1]) * scalingFactor

                #print(fittedLat, " ", fittedLon)
                bpy.ops.mesh.primitive_cube_add(location=(np.float64(lat), np.float64(lon), 0), scale=(1, 1, 1))

