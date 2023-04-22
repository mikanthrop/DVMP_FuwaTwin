import xml.etree.ElementTree as ET
import bpy

# Parse the XML file
tree = ET.parse('test.osm')

# Get the root element
root = tree.getroot()

# Iterate over the child elements of the root
for child in root:
    print(child.tag, child.attrib, "\n")
    for sub_child in child:
        print(sub_child.tag, sub_child.text, "\n")