import xml.etree.ElementTree as ET
import bpy
import numpy as np
import bmesh
import math
import pathlib

def get_script_dir(): 
    script_dir = pathlib.Path(__file__).resolve().parent
    return script_dir

class OSMParser():

    def __init__(self, storeyHeight, scalingFactor, highlightHFU):
        self.storeyHeight = storeyHeight
        self.scalingFactor = scalingFactor
        self.highlightHFU = highlightHFU
        self.minLat = 0
        self.minLon = 0
        self.cellSize = 0
        self.terrainMap = []

        self.loadTerrain()

        self.streetCollection = bpy.data.collections.new("StreetCollection")
        bpy.context.scene.collection.children.link(self.streetCollection)

        self.streetObject = bpy.data.objects.new('Street', None)
        self.buildingObject = bmesh.new()
        
        self.forbidden = ["forest", "meadow", "park", "grassland"]
        self.allowed = ["building", "highway"]
        
        filepath = get_script_dir() / "io_import_osm_asc/example_data/smol.osm"
        self.tree = ET.parse(filepath.__str__())


    def loadTerrain(self):
        """
        Loads height data from terrainData.asc.
        """
        filepath = get_script_dir() / "io_import_osm_asc/example_data/terrainData.asc"
        file = open(filepath.__str__())
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

    def loadBuildingMesh(self,lat,lon,height):
        """
        Import the building mesh 
        """
        filepath_building = get_script_dir() / "io_import_osm_asc/example_data/Flasche.obj"
        building_mesh_path = filepath_building.__str__()
        bpy.ops.import_scene.obj(filepath=building_mesh_path)
        building_object = bpy.context.selectable_objects[0]
        building_object.location = (lat,lon,height)
        #building_object.rotation_euler = rotation
        scale = (44.44,19.66,57.85)
        rotation = 1.206, -0.315, math.pi
        building_object.scale = scale
        building_object.rotation_euler = rotation
        bpy.context.view_layer.objects.active = building_object
        bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
        return building_object

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

        latIdx = latDiff / self.cellSize
        lonIdx = lonDiff / self.cellSize

        latFloor = int(math.floor(latIdx))
        latCeil = int(math.ceil(latIdx))
        lonFloor = int(math.floor(lonIdx))
        lonCeil = int(math.ceil(lonIdx))

        if(lonCeil >= self.ncols):
            lonFloor = self.ncols - 2
            lonCeil = self.ncols - 1
        if(latCeil >= self.nrows):
            latFloor = self.nrows - 2
            latCeil = self.nrows - 1

        #print(latFloor, latCeil, lonFloor, lonCeil)
        heightv1 = int(self.terrainMap[latFloor][lonFloor])
        heightv2 = int(self.terrainMap[latCeil][lonFloor])
        heightv3 = int(self.terrainMap[latFloor][lonCeil])
        heightv4 = int(self.terrainMap[latCeil][lonCeil])

        # xFloor =  self.minLat * latFloor * self.cellSize
        # xCeil = self.minLat * latCeil * self.cellSize
        # yFloor = self.minLon * lonFloor * self.cellSize
        # yCeil = self.minLon * lonCeil * self.cellSize

        # v1Coords = (xFloor, yFloor)
        # v2Coords = (xCeil, yFloor)
        # v3Coords = (xFloor, yCeil)
        # v4Coords = (xCeil, yCeil)

        dist1 = latIdx - latFloor
        dist2 = latCeil - latIdx
        dist3 = lonIdx - lonFloor
        dist4 = lonCeil - lonIdx

        area1 = dist2 * dist4
        area2 = dist1 * dist4
        area3 = dist2 * dist3
        area4 = dist1 * dist3

        return (area1 * heightv1 + area2 * heightv2 + area3 * heightv3 + area4 * heightv4) - int(self.terrainMap[30][12])


    def parse(self):
        ghb_found = False
        """
        Parse osm file and generate blender objects.
        """
        node_dict = {}
        root = self.tree.getroot()

        #blockScale = (1, 1, 1)

        buildingIndex = -1
        streetIndex = -1

        firstNodeLocation = ()
        scalingFactor = 100000

        # Iterate over the child elements of the root
        for child in root:
            if (child.tag == "node"):

                # Store first node location, used for centering map
                if (firstNodeLocation == ()):
                    lat = child.attrib.get("lat")
                    lon = child.attrib.get("lon")
                    firstNodeLocation = (float(lat), float(lon))

                # Added GHB Location
                
                    ghb_lat = 48.047495152
                    ghb_lon = 8.209267348
                    fittedgbhLat = (ghb_lat - firstNodeLocation[0]) * scalingFactor
                    fittedgbhLon = (ghb_lon - firstNodeLocation[1]) * scalingFactor
                    ghbHeight = self.calculate_height(ghb_lat, ghb_lon)
                    cube_mappedHgt = ghbHeight
                    #bpy.ops.mesh.primitive_cube_add(size=1, location=(fittedgbhLat, fittedgbhLon, cube_mappedHgt))

                    self.loadBuildingMesh(fittedgbhLat,fittedgbhLon,cube_mappedHgt)
                    obj = bpy.context.active_object
                    obj.name = "Flasche"
                # Store key and value pairs
                keyString = child.attrib.get("id")
                valueString = child.attrib.get(
                    "lat") + " " + child.attrib.get("lon")
                node_dict[keyString] = valueString
            elif (child.tag == "way"):
                tags = child.findall("tag")
                allowedFound = False
                tagString = ""
                levels = 1

                for t in tags:
                    value = t.get("k")
                    if value in self.allowed:
                        allowedFound = True
                        tagString = value
                    elif value == "building:levels":
                        #print(value)
                        levels = int(t.get("v"))
                    elif value == "name" and t.get("v") == "Großhausberg 9":
                        allowedFound = False
                        
                if allowedFound:
                    nodeRefs = child.findall("nd")
                    usedNodes = []
                    roadCoords = []
                    newObject = True
                    
                    firstIndex = 0

                    roof = []
                    wall = []

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
                            mappedHgt = float(mappedHgt)
                            
                            helper = 0

                            if tagString == "building":
                                #if nodeRef not in usedNodes:
                                usedNodes.append(nodeRef)
                                for i in range(2):
                                    self.buildingObject.verts.new((fittedLat, fittedLon, mappedHgt + i * levels * self.storeyHeight))
                                    buildingIndex += 1
                                    self.buildingObject.verts.ensure_lookup_table()
                                    wall.append(self.buildingObject.verts[buildingIndex])
                                    if i > 0:
                                        self.buildingObject.verts.ensure_lookup_table()
                                        if not self.building_edge_exists(self.buildingObject.verts[buildingIndex - 1], self.buildingObject.verts[buildingIndex]):
                                            self.buildingObject.edges.new((self.buildingObject.verts[buildingIndex - 1], self.buildingObject.verts[buildingIndex]))
                                        if not newObject and not self.building_edge_exists(self.buildingObject.verts[buildingIndex - 2], self.buildingObject.verts[buildingIndex]):
                                            self.buildingObject.edges.new((self.buildingObject.verts[buildingIndex - 2], self.buildingObject.verts[buildingIndex]))
                                    if i == 1:
                                        roof.append(self.buildingObject.verts[buildingIndex])
                                    if wall.__len__() == 4 and usedNodes.count(usedNodes) != 2:
                                        self.buildingObject.faces.new([wall[0], wall[1], wall[3], wall[2]])
                                        wall = [wall[2], wall[3]]
                            elif tagString == "highway":
                                #if nodeRef not in usedNodes:
                                usedNodes.append(nodeRef)
                                roadCoords.append(np.array((fittedLat, fittedLon, mappedHgt)))
                                streetIndex += 1
                                if not newObject:
                                    self.add_object(roadCoords[-2], roadCoords[-1], 0)

                            newObject = False

                        else:
                            continue
                    roadCoords = []
                    if tagString == "building":
                            self.buildingObject.faces.new(roof)

        # street = bpy.data.meshes.new("streets")
        # self.streetObject.to_mesh(street)
        # self.streetObject.free()
        # streetob = bpy.data.objects.new("StreetObject", street)
        # bpy.context.scene.collection.objects.link(streetob)
        # bpy.context.view_layer.objects.active = streetob

        building = bpy.data.meshes.new("buildings")
        self.buildingObject.to_mesh(building)
        self.buildingObject.free()
        buildingob = bpy.data.objects.new("BuildingObject", building)
        bpy.context.scene.collection.objects.link(buildingob)

        bpy.ops.object.select_all(action='DESELECT')
        flasche = None
        # Mirror every object along the y,z axis
        for obj in bpy.context.scene.objects:
            obj.select_set(True)
        
        bpy.ops.transform.mirror(orient_type='LOCAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='LOCAL', constraint_axis=(False, True, False))


        #bpy.ops.object.delete()
        #obj.select_set(False)
        # buildingob.select_set(True)
        # bpy.ops.object.mode_set(mode='EDIT')
        # bpy.ops.mesh.select_all(action='SELECT')
        # bpy.ops.mesh.edge_face_add()

        # # Switch back to object mode
        # bpy.ops.object.mode_set(mode='OBJECT')


    def define_control_points(self, start, end, spline):
        # get step-size to distribute control points evenly between start and end
        #print("LAMO\n")

        distance = end - start
        step_size = distance / (len(spline.bezier_points) - 1)

        handle_offset = step_size / 7

        # Set control points for curve
        for i in range(len(spline.bezier_points)):
            spline.bezier_points[i].tilt = 1.5708 # tilt each spline by 90 degrees
            if (i == 0):
                spline.bezier_points[i].co = start
                spline.bezier_points[i].handle_left = (
                    (start[0]-handle_offset[0]), (start[1]-handle_offset[1]), (start[2]-handle_offset[2]))
                spline.bezier_points[i].handle_right = (
                    (start[0]+handle_offset[0]), (start[1]+handle_offset[1]), (start[2]+handle_offset[2]))
            elif (i == (len(spline.bezier_points) - 1)):
                spline.bezier_points[i].co = end
                spline.bezier_points[i].handle_left = (
                    (end[0]-handle_offset[0]), (end[1]-handle_offset[1]), (end[2]-handle_offset[2]))
                spline.bezier_points[i].handle_right = (
                    (end[0]+handle_offset[0]), (end[1]+handle_offset[1]), (end[2]+handle_offset[2]))
            else:
                current = start + (step_size * i)
                spline.bezier_points[i].co = (current[0], current[1], current[2])
                spline.bezier_points[i].handle_left = (
                    (current[0]-handle_offset[0]), (current[1]-handle_offset[1]), (current[2]-handle_offset[2]))
                spline.bezier_points[i].handle_right = (
                    (current[0]+handle_offset[0]), (current[1]+handle_offset[1]), (current[2]+handle_offset[2]))
                
    def add_object(self, start_point, end_point, cuts):

        # Create curve object
        street_curve = bpy.data.curves.new('BezierCurve', 'CURVE')
        street_curve.dimensions = '3D'

        # Create a new spline for the curve
        spline = street_curve.splines.new('BEZIER')
        spline.bezier_points.add(cuts + 1)

        # Define control points for the spline
        self.define_control_points(start_point, end_point, spline)

        # Set fill mode and extrusion
        street_curve.fill_mode = 'HALF'
        street_curve.extrude = 0.5


        # Create an object from the curve
        obj = bpy.data.objects.new('StreetObject', street_curve)
        self.streetCollection.objects.link(obj)
   
    def link_street_curves(self):
        """
        Link street curves to one curve. Not used, as the outcome is unusable.
        """
        for obj in self.streetCollection.objects:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = self.streetCollection.objects[0]
        bpy.ops.object.join()
        
    def merge_objects(self):
        """
        Merge all street objects together. Takes too long to execute, but increases performance once finished.
        """
        ctx = bpy.context.copy()
        ctx["active_object"] = self.streetCollection.objects[0]
        ctx["selected_editable_objects"] = self.streetCollection.objects
        bpy.ops.object.join(ctx)
