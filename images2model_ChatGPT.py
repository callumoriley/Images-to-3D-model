import numpy as np
from skimage import measure
from PIL import Image
import os

# Load all PNG files from a directory and determine the size of the volume
directory = "MRI/"
STANDARD_SIZE = False

if not STANDARD_SIZE:
    with Image.open(directory+"1.png") as img:
        width, height = img.size
    
    volume = np.zeros((width, height, len(os.listdir(directory))), dtype=np.uint8)
else:
    volume = np.zeros((512, 512, 512), dtype=np.uint8)

# Load the PNG files and add them to the volume
for filename in os.listdir(directory):
    if filename.endswith(".png"):
        filepath = os.path.join(directory, filename)
        img = Image.open(filepath).convert("L")
        z = int(filename.split(".")[0]) - 1 # subtract 1 if the files start from 1
        volume[:, :, z] = np.array(img)

# Generate the mesh using the marching cubes algorithm
verts, faces, normals, values = measure.marching_cubes(volume)

# Save the mesh as an OBJ file
with open("output_gpt_4.obj", "w") as f:
    for v in verts:
        f.write("v {} {} {}\n".format(v[0], v[1], v[2])) # add Z multiplier here
    for face in faces:
        f.write("f {} {} {}\n".format(face[0]+1, face[1]+1, face[2]+1))
