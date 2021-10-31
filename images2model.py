from PIL import Image, ImageFilter, ImageEnhance
import PIL.ImageOps

# these parameters need to be changed based on the images you are using
numOfImages = 476
spaceBetweenLayers = 0.005
threshold = 200
xCoordScale = 0.01
yCoordScale = 0.01
neighbours = 8

outputFileName = input("Enter the name of the output file: ")
subDirName = input("Enter the name of the subdirectory the images are stored in, with a slash behind it (e.g. Dir/) (leave blank if in the same directory as the script): ")

writeFile = open(outputFileName, "w")
z = 0
allPoints = []
facetStrings = []

def getDistBetweenPoints(x1, y1, z1, x2, y2, z2):
    return ((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)**0.5

def getNClosestPoints(inList, x, y, z, n, middleIndex):
    reachBack = 1000
    reachForward = 1000
    
    closestIndices = [-1] * n # closest ones are at lower indexes
    closestDists = [100000000] * n

    for i in range((0 if (middleIndex - reachBack < 0) else middleIndex - reachBack), (len(inList) if (middleIndex + reachForward) > len(inList) else middleIndex + reachForward)):
        currDist = getDistBetweenPoints(x, y, z, inList[i][0], inList[i][1], inList[i][2])
        
        for j in range(0, len(closestDists)):
            if currDist < closestDists[j] and z != inList[i][2]:
                closestDists.insert(j, currDist)
                closestDists.pop()
                closestIndices.insert(j, i)
                closestIndices.pop()
                break

    return closestIndices

print("Loading images")
for n in range(1, numOfImages + 1):
    print(n)
    
    #currImage = PIL.ImageOps.invert(Image.open(subDirName+str(n)+".png").convert("L")) # opens image and converts it to grayscale and inverts it
    currImage = Image.open(subDirName+str(n)+".png").convert("L") # opens image and converts it to grayscale
    currImage = currImage.resize((100, 100), Image.ANTIALIAS) # resize the image
    currImage = ImageEnhance.Contrast(currImage).enhance(5) # increase image contrast
    edgeImage = currImage.filter(ImageFilter.FIND_EDGES) # creates an image with edges

    points = []

    for i in range(0, edgeImage.size[1]):
        for j in range(0, edgeImage.size[0]):
            currPixel = edgeImage.getpixel((j, i))
            if currPixel > threshold:
                points.append((j, i))
    
    for i in range(0,len(points)):
        allPoints.append((points[i][0]*xCoordScale, points[i][1]*yCoordScale, z))
        
    z += spaceBetweenLayers

print("Writing vertexes")
for i in range(0, len(allPoints)):
    print(str(i)+"/"+str(len(allPoints)-1))
    writeFile.write("v "+str(allPoints[i][0])+" "+str(allPoints[i][2])+" "+str(allPoints[i][1])+"\n")

print("Calculating facets")
for i in range(0, len(allPoints)):
    print(str(i)+"/"+str(len(allPoints)-1))
    closestIndices = getNClosestPoints(allPoints, allPoints[i][0], allPoints[i][1],allPoints[i][2], neighbours, i)
    for j in range(0,neighbours-1):
        writeFile.write("f "+str(i + 1)+" "+str(closestIndices[j] + 1)+" "+str(closestIndices[j + 1] + 1)+"\n")

writeFile.write("\n")
writeFile.close()

"""
Useful links:
https://www.geeksforgeeks.org/python-edge-detection-using-pillow/
https://www.geeksforgeeks.org/python-pil-getpixel-method/
https://www.kite.com/python/answers/how-to-iterate-through-a-decreasing-range-with-a-for-loop-in-python
"""
