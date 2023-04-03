import os
import mahotas as mh
import nrrd
import numpy as np
import matplotlib


class PlaqueFeatures:

	def __init__(self, inputdata):

		self._roundto = 3
		self._inputdata = inputdata

		# os.path.exists(self._inputdata) when implementing for directories as well as files
		try:
			if os.path.isfile(self._inputdata) == False or not self._inputdata.lower().endswith('.nrrd'):
				raise Exception
			self._setup(self._inputdata)
		except Exception:
			print("File does not exist or is not a NRRD file.")
	
	
	def _setup(self, inputdata):
		
		self._label_data, self._label_header = nrrd.read(inputdata)
		self._relabel, self._obj = mh.label(self._label_data)

		self._split_array = np.split(self._relabel, 2)
		self._right_pvoxels = np.bincount(self._split_array[0].flatten())[1:]
		self._left_pvoxels = np.bincount(self._split_array[1].flatten())[1:]
		self._right_count = len(self._right_pvoxels)
		self._left_count = np.count_nonzero(self._left_pvoxels)

		self._data_voxels = np.bincount(self._relabel.flatten())
		self._plaque_voxels = self._data_voxels[1:]
		self._plaque_count = len(self._plaque_voxels)

		self._voxel_dimensions = self._label_header['space directions'][self._label_header['space directions'] != 0]
		self._voxel_volume = self._voxel_dimensions[0]*self._voxel_dimensions[1]*self._voxel_dimensions[2]

		self._plaque_side = []
		for i in range(self._plaque_count):
			if self._left_pvoxels[i] == 0:
				self._plaque_side.append("Right")
			else:
				self._plaque_side.append("Left")

		self._plaque_bbox = mh.labeled.bbox(self._relabel)
		self._y_width = 0
		self._x_depth = 0
		self._z_height = 0
		self._hold = []


	def newData(self, newdataset):

		self._new_dataset = newdataset
		try:
			if os.path.isfile(self._new_dataset) == False or not self._new_dataset.lower().endswith('.nrrd'):
				raise Exception
			self._setup(self._new_dataset)
		except Exception:
			print("File does not exist or is not a NRRD file.")
	

	def help(self):
		print("List of all available methods and their functions:\n")
		print("newData(datapath) : Replaces input data with the new dataset and re-runs setup.")
		print("setRound(integer) : Set the number of decimal places to round output to. Default is 3.\n")
		print("pInfo(plaquenumber) : Prints all data for a specified plaque.")
		print("pInfoAll() : Prints all data for each plaque.")
		print("pInfoL() : Prints all data for plaque on the left side.")
		print("pInfoR() : Prints all data for plaque on the right side.\n")
		print("pCount() : Returns the total number of plaque.")
		print("pCountL() : Returns the number of plaque on the left side.")
		print("pCountR() : Returns the number of plaque on the right side.\n")
		print("pVox(plaquenumber) : Returns the number of voxels for a specified plaque.")
		print("pVoxAll() : Prints the number of voxels of each plaque.")
		print("pVoxL() : Prints the number of voxels for plaque on the left side.")
		print("pVoxR() : Prints the number of voxels for plaque on the right side.")
		print("pVoxLTot() : Returns the total number of plaque voxels on the left side.")
		print("pVoxRTot() : Returns the total number of plaque voxels on the right side.")
		print("pVoxTot() : Returns the total number of plaque voxels.\n")
		print("dataVoxTot() : Returns the total number of voxels in the dataset.")
		print("dataDim() : Returns the dimensions of the dataset (the shape).\n")
		print("Note on volume calculations: Outputs are in mm3. To convert to cm3, divide by 1000.")
		print("pVol(plaquenumber) : Returns the volume of a specified plaque.")
		print("pVolAll() : Prints the volume of each plaque.")
		print("pVolL() : Prints the volume of each plaque on the left side.")
		print("pVolR() : Prints the volume of each plaque on the right side.")
		print("pVolLTot() : Returns the total plaque volume of the left side.")
		print("pVolRTot() : Returns the total plaque volume of the right side.")
		print("pVolTot() : Returns the total plaque volume.\n")
		print("Note on size measurements: Outputs are in mm, measured from the lowest to the highest point of the plaque on a 3D Cartesian plane.")
		print("They are in Axial (left to right, y-axis), Sagittal (front to back, x-axis), and Coronal (top down, z-axis) plane order.")
		print("pSize(plaquenumber) : Returns a list of the measurements of the specified plaque in y, x, z order.")
		print("pSizeAll() : Prints the measurements for each plaque.")
		print("pSizeL() : Prints the measurements for each plaque on the left side.")
		print("pSizeR() : Prints the measurements for each plaque on the right side.")


	def pInfo(self, plaquenumber):
		try:
			self._plaque_number = int(plaquenumber)
			if self._plaque_number > self._plaque_count or self._plaque_number < 1:
				raise Exception
			print("Plaque #{} ({}):".format(self._plaque_number, self._plaque_side[self._plaque_number-1]))
			print("Voxels: {}".format(self.pVox(self._plaque_number)))
			print("Volume: {}mm3".format(self.pVol(self._plaque_number)))
			self._sizes = self.pSize(self._plaque_number)
			print("Width (axial plane, y-axis): {}mm".format(self._sizes[0]))
			print("Depth (sagittal plane, x-axis): {}mm".format(self._sizes[1]))
			print("Height (coronal plane, z-axis): {}mm".format(self._sizes[2]))
		except ValueError:
			print("pInfo() has failed. Please enter a valid plaque number from 1 to {}.".format(self._plaque_count))
		except Exception:
			print("pInfo() has failed. Please enter a valid plaque number from 1 to {}.".format(self._plaque_count))


	def pInfoAll(self):
		print("Total number of plaque: {}\n".format(self.pCount()))
		self.pVoxAll()
		print("Total number of plaque voxels: {}".format(self.pVoxTot()))
		print("Total number of voxels in dataset: {}\n".format(self.dataVoxTot()))
		self.pVolAll()
		print("Total plaque volume: {}mm3\n".format(self.pVolTot()))
		self.pSizeAll()
		print("\nDimensions of input dataset: {}".format(self.dataDim()))


	def pInfoL(self):
		print("Number of plaque on the left side: {}\n".format(self.pCountL()))
		self.pVoxL()
		print("Total number of plaque voxels on the left side: {}\n".format(self.pVoxLTot()))
		self.pVolL()
		print("Total plaque volume of the left side: {}mm3\n".format(self.pVolLTot()))
		self.pSizeL()


	def pInfoR(self):
		print("Number of plaque on the right side: {}\n".format(self.pCountR()))
		self.pVoxR()
		print("Total number of plaque voxels on the right side: {}\n".format(self.pVoxRTot()))
		self.pVolR()
		print("Total plaque volume of the right side: {}mm3\n".format(self.pVolRTot()))
		self.pSizeR()


	def pCount(self):
		return self._plaque_count


	def pCountL(self):
		return self._left_count


	def pCountR(self):
		return self._right_count


	def pVox(self, plaquenumber):
		try:
			self._plaque_number = int(plaquenumber)
			if self._plaque_number > self._plaque_count or self._plaque_number < 1:
				raise Exception
			return self._plaque_voxels[self._plaque_number-1]
		except ValueError:
			print("pVox() has failed. Please enter a valid plaque number from 1 to {}.".format(self._plaque_count))
		except Exception:
			print("pVox() has failed. Please enter a valid plaque number from 1 to {}.".format(self._plaque_count))


	def pVoxAll(self):
		for i in range(self._plaque_count):
			print("Plaque #{} ({}) voxels: {}".format(i+1, self._plaque_side[i], self._plaque_voxels[i]))


	def pVoxL(self):
		for i in range(self._left_count):
			print("Plaque #{} ({}) voxels: {}".format(i+1+self._right_count, self._plaque_side[i+self._right_count], self._plaque_voxels[i+self._right_count]))


	def pVoxR(self):
		for i in range(self._right_count):
			print("Plaque #{} ({}) voxels: {}".format(i+1, self._plaque_side[i], self._plaque_voxels[i]))


	def pVoxLTot(self):
		return self._left_pvoxels.sum()


	def pVoxRTot(self):
		return self._right_pvoxels.sum()


	def pVoxTot(self):
		return self._plaque_voxels.sum()


	def dataVoxTot(self):
		return self._data_voxels.sum()


	# May need to change volume functions later if label data doesn't
	# contain 'space directions' for the voxel dimensions.
	# Note: To convert mm3 to cm3, divide mm3 by 1000.

	def pVol(self, plaquenumber):
		try:
			self._plaque_number = int(plaquenumber)
			if self._plaque_number > self._plaque_count or self._plaque_number < 1:
				raise Exception
			return round(self._plaque_voxels[self._plaque_number-1]*self._voxel_volume, self._roundto)
		except ValueError:
			print("pVol() has failed. Please enter a valid plaque number from 1 to {}.".format(self._plaque_count))
		except Exception:
			print("pVol() has failed. Please enter a valid plaque number from 1 to {}.".format(self._plaque_count))


	def pVolAll(self):
		for i in range(self._plaque_count):
			print("Plaque #{} ({}) volume: {}mm3".format(i+1, self._plaque_side[i], round(self._plaque_voxels[i]*self._voxel_volume, self._roundto)))


	def pVolL(self):
		for i in range(self._left_count):
			print("Plaque #{} ({}) volume: {}mm3".format(i+1+self._right_count, self._plaque_side[i+self._right_count], round(self._plaque_voxels[i+self._right_count]*self._voxel_volume, self._roundto)))


	def pVolR(self):
		for i in range(self._right_count):
			print("Plaque #{} ({}) volume: {}mm3".format(i+1, self._plaque_side[i], round(self._plaque_voxels[i]*self._voxel_volume, self._roundto)))


	def pVolLTot(self):
		return round(self._left_pvoxels.sum()*self._voxel_volume, self._roundto)


	def pVolRTot(self):
		return round(self._right_pvoxels.sum()*self._voxel_volume, self._roundto)


	def pVolTot(self):
		return round(self._plaque_voxels.sum()*self._voxel_volume, self._roundto)


	def pSize(self, plaquenumber):
		try:
			self._plaque_number = int(plaquenumber)
			if self._plaque_number > self._plaque_count or self._plaque_number < 1:
				raise Exception
			self._hold = self._plaque_bbox[self._plaque_number]
			self._y_width = round((self._hold[1]-self._hold[0])*self._voxel_dimensions[0], self._roundto)
			self._x_depth = round((self._hold[3]-self._hold[2])*self._voxel_dimensions[1], self._roundto)
			self._z_height = round((self._hold[5]-self._hold[4])*self._voxel_dimensions[2], self._roundto)
			return [self._y_width, self._x_depth, self._z_height]
		except ValueError:
			print("pSize() has failed. Please enter a valid plaque number from 1 to {}.".format(self._plaque_count))
		except Exception:
			print("pSize() has failed. Please enter a valid plaque number from 1 to {}.".format(self._plaque_count))


	def pSizeAll(self):
		for i in range(1, len(self._plaque_bbox)):
			self._hold = self._plaque_bbox[i]
			self._y_width = round((self._hold[1]-self._hold[0])*self._voxel_dimensions[0], self._roundto)
			self._x_depth = round((self._hold[3]-self._hold[2])*self._voxel_dimensions[1], self._roundto)
			self._z_height = round((self._hold[5]-self._hold[4])*self._voxel_dimensions[2], self._roundto)
			print("Plaque #{} ({}):\nWidth (axial plane, y-axis): {}mm\nDepth (sagittal plane, x-axis): {}mm\nHeight (coronal plane, z-axis): {}mm".format(i, self._plaque_side[i-1], self._y_width, self._x_depth, self._z_height))


	def pSizeL(self):
		for i in range(self._right_count+1, len(self._plaque_bbox)):
			self._hold = self._plaque_bbox[i]
			self._y_width = round((self._hold[1]-self._hold[0])*self._voxel_dimensions[0], self._roundto)
			self._x_depth = round((self._hold[3]-self._hold[2])*self._voxel_dimensions[1], self._roundto)
			self._z_height = round((self._hold[5]-self._hold[4])*self._voxel_dimensions[2], self._roundto)
			print("Plaque #{} ({}):\nWidth (axial plane, y-axis): {}mm\nDepth (sagittal plane, x-axis): {}mm\nHeight (coronal plane, z-axis): {}mm".format(i, self._plaque_side[i-1], self._y_width, self._x_depth, self._z_height))


	def pSizeR(self):
		for i in range(1, self._right_count+1):
			self._hold = self._plaque_bbox[i]
			self._y_width = round((self._hold[1]-self._hold[0])*self._voxel_dimensions[0], self._roundto)
			self._x_depth = round((self._hold[3]-self._hold[2])*self._voxel_dimensions[1], self._roundto)
			self._z_height = round((self._hold[5]-self._hold[4])*self._voxel_dimensions[2], self._roundto)
			print("Plaque #{} ({}):\nWidth (axial plane, y-axis): {}mm\nDepth (sagittal plane, x-axis): {}mm\nHeight (coronal plane, z-axis): {}mm".format(i, self._plaque_side[i-1], self._y_width, self._x_depth, self._z_height))


	def dataDim(self):
		return self._relabel.shape


	def setRound(self, val):
		try:
			self._roundto = int(val)
			print("Values will now be rounded to {} decimal places.".format(self._roundto))
		except ValueError:
			print("setRound() has failed. Please enter a valid integer.")