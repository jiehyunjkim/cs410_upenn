import os
import mahotas as mh
import nrrd
import numpy as np
import matplotlib
#import sys

#image_file = "C:/Users/alexa/Desktop/CS 410/data/DICOM 6/4 Unnamed Series.nrrd"
#label_file = "C:/Users/alexa/Desktop/CS 410/data/DICOM 6/Segmentation.seg.nrrd"

image_file = "C:/Users/alexa/Desktop/CS 410/data/DICOM 7/11 Unnamed Series.nrrd"
label_file = "C:/Users/alexa/Desktop/CS 410/data/DICOM 7/Segmentation.seg.nrrd"

#image_file = "C:/Users/alexa/Desktop/CS 410/data/DICOM 12-checked/ESUS12c_7 Unnamed Series.nrrd"
#label_file = "C:/Users/alexa/Desktop/CS 410/data/DICOM 12-checked/ESUS12c_Segmentation.seg.nrrd"

#image_file = "C:/Users/alexa/Desktop/CS 410/data/DICOM 13/4 Unnamed Series.nrrd"
#label_file = "C:/Users/alexa/Desktop/CS 410/data/DICOM 13/Segmentation.seg.nrrd"



image_data, image_header = nrrd.read(image_file)
label_data, label_header = nrrd.read(label_file)

voxel_dimensions = label_header['space directions'][label_header['space directions'] != 0]
voxel_volume = voxel_dimensions[0]*voxel_dimensions[1]*voxel_dimensions[2]

relabel, obj = mh.label(label_data) #labeled array, number of objects

plaque_sizes = np.bincount(relabel.flatten())[1:]
plaque_count = len(plaque_sizes)
print("Total number of plaque: {}\n".format(plaque_count))



split_array = np.split(relabel, 2)
right_sizes = np.bincount(split_array[0].flatten())[1:]
left_sizes = np.bincount(split_array[1].flatten())[1:]
print("Number of plaque on right side: {}\nTotal plaque voxels on right side: {}".format(np.count_nonzero(right_sizes), right_sizes.sum()))
print("Number of plaque on left side: {}\nTotal plaque voxels on left side: {}\n".format(np.count_nonzero(left_sizes), left_sizes.sum()))



plaque_index = 0
plaque_side = ""

for i in range(plaque_count):
	plaque_index+=1
	if left_sizes[i] == 0:
		plaque_side = "Right"
	else:
		plaque_side = "Left"
	print("Plaque #{} voxels ({}): {}".format(plaque_index, plaque_side, plaque_sizes[i]))
	print("Plaque #{} volume: {}mm3".format(plaque_index, round(plaque_sizes[i]*voxel_volume, 3)))

unique, counts = np.unique(relabel, return_counts=True)
print("\nComparison with a different method:\n{}".format(dict(zip(unique, counts))))



print("\nTotal number of plaque voxels: {}".format(plaque_sizes.sum()))

image_voxels = (np.bincount(relabel.flatten())).sum()
print("Total number of voxels in image: {}".format(image_voxels))
print("Image dimensions: {}\n".format(label_data.shape))


# remaining issue where a plaque is sometimes undetected by bbox
# ie. plaque 8 from DICOM 7
plaque_bbox = mh.labeled.bbox(label_data)
print("Plaque bbox array:\n{}\n".format(plaque_bbox))

# test1 = plaque_bbox[1]
# print(test1)
# p1voldim = (test1[1]-test1[0]+1)*(test1[3]-test1[2]+1)*(test1[5]-test1[4]+1)
# p1vol = p1voldim*voxel_volume
# print(p1vol)

# by convention, numpy goes y, x, z
y_height = 0
x_width = 0
z_depth = 0
holder = []

for i in range(1, len(plaque_bbox)):
	holder = plaque_bbox[i]
	y_height = round((holder[1]-holder[0]+1)*voxel_dimensions[1], 3)
	x_width = round((holder[3]-holder[2]+1)*voxel_dimensions[0], 3)
	z_depth = round((holder[5]-holder[4]+1)*voxel_dimensions[2], 3)
	print("Plaque #{}:\nHeight (y-axis): {}mm\nWidth (x-axis): {}mm\nDepth (z-axis): {}mm".format(i, y_height, x_width, z_depth))


#___________________________________

## data categories recorded in header of segmentation file

#data = "C:/Users/alexa/Desktop/CS 410/data/DICOM 6/Segmentation.seg.nrrd"
#image = nrrd.read(label_file)

#header = nrrd.read_header(label_file)

#print(header.keys())
#print(header.items())
#___________________________________

## tests printing file contents to txt file

# np.set_printoptions(threshold=sys.maxsize)
# np.set_printoptions(threshold=1000)

#print(image)

#content = str(image)

# with open("upenntest.txt", "w") as txt_file:
# 	for line in content:
# 		txt_file.write(" ".join(line))