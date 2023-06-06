file = open("../BlenderImportPipeline/terrain/terrainData.asc")
lines = file.readlines()

ncols = (int)(lines[0].split()[-1])
nrows = (int)(lines[1].split()[-1])
minLon = (float)(lines[2].split()[-1])
minLon = (float)(lines[3].split()[-1])
cellSize = (float)(lines[4].split()[-1])

print(ncols, nrows, cellSize)
terrainMap = [[0] * ncols for i in range(nrows)]

x = 0
y = 0

for line in lines[6:]:
    line = line.split()
    x = 0
    for height in line:
        terrainMap[y][x] = height
        x += 1
    y += 1
