import xml.etree.ElementTree as ET
import bpy
import bmesh
import numpy as np

class OSMParser():

    def __init__(self):
        self.minLat = 0
        self.minLon = 0
        self.cellSize = 0
        self.terrainMap = []

        self.loadTerrain()

        self.streetObject = bmesh.new()
        self.buildingObject = bmesh.new()
        
        self.forbidden = ["forest", "meadow", "park", "grassland"]
        self.allowed = ["building", "highway"]
        
        self.tree = ET.parse("../BlenderImportPipeline/testMaps/map.osm")


    def loadTerrain(self):
        """
        Loads height data from terrainData.asc.
        """
        file = open("../BlenderImportPipeline/terrain/terrainData.asc")
        lines = file.readlines()

        self.ncols = int(lines[0].split()[-1])
        self.nrows = int(lines[1].split()[-1])
        self.minLon = float(lines[2].split()[-1])
        self.minLat = float(lines[3].split()[-1])
        self.cellSize = float(lines[4].split()[-1])

        self.terrainMap = [[0] * self.ncols for i in range(self.nrows)]

        x = 0
        y = 0

        for line in lines[6:]:
            line = line.split()
            x = 0
            for height in line:
                self.terrainMap[y][x] = height
                x += 1
            y += 1

    def building_edge_exists(self, v1, v2):
        """
        Checks if a building edge already exists. Bruteforce bug fix, thus relatively computationally expensive.
        """
        for edge in self.buildingObject.edges:
            if (edge.verts[0] == v1 and edge.verts[1] == v2) or (edge.verts[0] == v2 and edge.verts[1] == v1):
                return True
        return False

    def street_edge_exists(self, v1, v2):
        """
        Checks if a street edge already exists. Bruteforce bug fix, thus relatively computationally expensive.
        """
        for edge in self.streetObject.edges:
            if (edge.verts[0] == v1 and edge.verts[1] == v2) or (edge.verts[0] == v2 and edge.verts[1] == v1):
                return True
        return False

    def calculate_height(self, lat, lon):
        """
        Returns the height at given lat, lon.
        """
        latDiff = lat - self.minLat
        lonDiff = lon - self.minLon
        latIdx = latDiff // self.cellSize
        lonIdx = lonDiff // self.cellSize
        if (latIdx >= self.nrows):
            latIdx = self.nrows - 1
        if(lonIdx >= self.ncols):
            lonIdx = self.ncols - 1
        return self.terrainMap[int(latIdx)][int(lonIdx)]

    def parse(self):
        """
        Parse osm file and generate blender objects.
        """
        node_dict = {}
        root = self.tree.getroot()

        #blockScale = (1, 1, 1)

        buildingIndex = -1
        streetIndex = -1

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
                valueString = child.attrib.get(
                    "lat") + " " + child.attrib.get("lon")
                node_dict[keyString] = valueString
            elif (child.tag == "way"):
                tags = child.findall("tag")
                allowedFound = False
                tagString = ""
                for t in tags:
                    value = t.get("k")
                    if value in self.allowed:
                        allowedFound = True
                        tagString = value
                        break
                if allowedFound:
                    nodeRefs = child.findall("nd")
                    usedNodes = []

                    newObject = True

                    for nd in nodeRefs:
                        nodeRef = nd.get("ref")
                        if (nodeRef != None):
                            node = node_dict[nodeRef]
                            lat, lon = node.split()
                            lat = float(lat)
                            lon = float(lon)
                            fittedLat = (lat -
                                        firstNodeLocation[0]) * scalingFactor
                            fittedLon = (lon -
                                        firstNodeLocation[1]) * scalingFactor
                            
                            mappedHgt = self.calculate_height(lat, lon)
                            mappedHgt = -float(mappedHgt) / 10
                            
                            if tagString == "building":
                                if nodeRef not in usedNodes:
                                    usedNodes.append(nodeRef)
                                    self.buildingObject.verts.new((fittedLat, fittedLon, mappedHgt))
                                    buildingIndex += 1
                                if not newObject:
                                    self.buildingObject.verts.ensure_lookup_table()
                                    if not self.building_edge_exists(self.buildingObject.verts[buildingIndex - 1], self.buildingObject.verts[buildingIndex]):
                                        self.buildingObject.edges.new((self.buildingObject.verts[buildingIndex - 1], self.buildingObject.verts[buildingIndex]))

                            elif tagString == "highway":
                                if nodeRef not in usedNodes:
                                    usedNodes.append(nodeRef)
                                    self.streetObject.verts.new((fittedLat, fittedLon, mappedHgt))
                                    streetIndex += 1
                                if not newObject:
                                    self.streetObject.verts.ensure_lookup_table()
                                    if not self.street_edge_exists(self.streetObject.verts[streetIndex - 1], self.streetObject.verts[streetIndex]):
                                        self.streetObject.edges.new((self.streetObject.verts[streetIndex - 1], self.streetObject.verts[streetIndex]))
                            newObject = False
                        else:
                            continue
                else:
                    continue

        street = bpy.data.meshes.new("streets")
        self.streetObject.to_mesh(street)
        self.streetObject.free()
        streetob = bpy.data.objects.new("StreetObject", street)
        bpy.context.scene.collection.objects.link(streetob)
        bpy.context.view_layer.objects.active = streetob

        building = bpy.data.meshes.new("buildings")
        self.buildingObject.to_mesh(building)
        self.buildingObject.free()
        buildingob = bpy.data.objects.new("BuildingObject", building)
        bpy.context.scene.collection.objects.link(buildingob)
        bpy.context.view_layer.objects.active = buildingob


parser = OSMParser()
parser.parse()