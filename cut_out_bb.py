# Opens file centers.txt (created from soil) and file slope.tif and then creates
# Creates a size 2r square (bounding box) around each center in centers.txt containing
# the pixels from slope.tif. All these hundreds of files are stored right in this directory.


import pickle
import numpy as np
from numpy import load
from numpy import asarray
from numpy import save
from osgeo import gdal

# storing list to file - not used for now
#with open("input.txt", 'wb') as f:
#    pickle.dump((soil_centers), f)
 
# loading list from file
with open("centers.txt", 'rb') as f:
   xcenters, ycenters = pickle.load(f)

r = 5 # meters on either side of the center
 
ds = gdal.Open('slope.tif')

#ds = gdal.Open('T33UUB_20190825T102031_B02_10m.jp2')
for x_coord, y_coord in zip(xcenters, ycenters):
	bb =  [x_coord-r, y_coord+r, x_coord+r, y_coord-r] # This is a rectangle around the coordinate center
	#print("bb",bb)
	new_ds = gdal.Translate('new.tif', ds, projWin = bb)
	myarray = np.array(new_ds.GetRasterBand(1).ReadAsArray())
	# create a numpy array from bbox
	#myarray = np.array(ds.GetRasterBand(1).ReadAsArray())
	
	
	# create unique name for this npy array
	filename = str(x_coord)+'_'+str(y_coord)
	
	# save array under its unique name (i.e. x, y coordinates)
	save(filename+'.npy', myarray)

print("The last npy array was:")
print(myarray.shape)

#Test loading the last dataset as a test # single npy data from file
data = load(filename+'.npy')
# print the array
print(data)

print(data==myarray)
	
#bb = [389196, 6170020,389216 ,6170000] # This is only a 2x2 # [-75.3, 5.5, -73.5, 3.7]


#ds = None


#from osgeo import gdal
#ds = gdal.Open("slope.tif")

#print(myarray.shape)
#print(myarray)

#Upper Left  (  387496.820, 6175003.450) ( 13d12'34.26"E, 55d42'27.81"N)
#Lower Left  (  387496.820, 6159995.450) ( 13d12'56.36"E, 55d34'22.57"N)
#Upper Right (  395004.820, 6175003.450) ( 13d19'44.21"E, 55d42'33.87"N)
#Lower Right (  395004.820, 6159995.450) ( 13d20' 4.84"E, 55d34'28.60"N)
#Center      (  391250.820, 6167499.450) ( 13d16'19.93"E, 55d38'28.27"N)



#dataset = gdal.Open(r'new.tif')
#print(dataset.RasterCount)

# since there are 3 bands
# we store in 3 different variables
#band1 = dataset.GetRasterBand(1) # Red channel
#band2 = dataset.GetRasterBand(2) # Green channel
#band3 = dataset.GetRasterBand(3) # Blue channel

#b1 = band1.ReadAsArray()
#b2 = band2.ReadAsArray()
#b3 = band3.ReadAsArray()

#img = np.dstack((b1, b2, b3))
#f = plt.figure()
#plt.imshow(img)
#plt.savefig('new.png')
#plt.show()

