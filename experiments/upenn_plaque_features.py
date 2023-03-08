import os
import mahotas as mh
import nrrd
import numpy as np
import matplotlib
#import sys

plaque_index = 0

#image_file = "C:/Users/alexa/Desktop/CS 410/data/DICOM 6/4 Unnamed Series.nrrd"
#label_file = "C:/Users/alexa/Desktop/CS 410/data/DICOM 6/Segmentation.seg.nrrd"

#image_file = "C:/Users/alexa/Desktop/CS 410/data/DICOM 7/11 Unnamed Series.nrrd"
#label_file = "C:/Users/alexa/Desktop/CS 410/data/DICOM 7/Segmentation.seg.nrrd"

image_file = "C:/Users/alexa/Desktop/CS 410/data/DICOM 12/ESUS 12_7 Unnamed Series.nrrd"
label_file = "C:/Users/alexa/Desktop/CS 410/data/DICOM 12/ESUS12_Segmentation.seg.nrrd"

#bounding box for size - length, width, height 
#for depth, maybe make a 2D array and add 1 at the index where the plaque is,
#and the highest number is the max plaque depth (be careful to separate plaques)

image_data, image_header = nrrd.read(image_file)
label_data, label_header = nrrd.read(label_file)

#print(image_data.shape)

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

for i in range(plaque_count):
	plaque_index+=1
	print("Plaque {} voxels: {}".format(plaque_index, plaque_sizes[i]))
	print("Plaque {} volume (mm3): {}".format(plaque_index, round(plaque_sizes[i]*voxel_volume, 3)))

print("Total number of plaque voxels: {}".format(plaque_sizes.sum()))

image_voxels = (np.bincount(relabel.flatten())).sum()
print("Total number of voxels in image: {}".format(image_voxels))





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