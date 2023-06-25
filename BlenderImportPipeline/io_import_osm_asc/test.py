import os
import pathlib

print(pathlib.Path(__file__).resolve().parent)
file_path = os.path.join(os.path.dirname(__file__), '..', 'example_data', 'terrainData.asc')
# print(file_path)