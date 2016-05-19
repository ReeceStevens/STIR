######################################################
#                                                    #
# comparison.py                                      #
# A script investigating different ischemic boundary #
# detection strategies. Retained in repository as an #
# example file and starting point for further openCV #
# based image analysis.                              #
#                                                    #
######################################################

import nibabel as nib
import cv2
import numpy as np
from matplotlib import pyplot as plt

# Load scan from file
img = nib.load('output.nii.gz')
data = img.get_data()
scan_res = data.shape[0]
num_slices = data.shape[2]
newdata = np.zeros([num_slices,scan_res,scan_res])

# Reshape image data for ease of use
for x in range(0, len(data)):
    for y in range(0,len(data[0])):
        for z in range(0,len(data[0,0])):
            newdata[z,x,y] = data[x,y,z]

# Display all slices in the file
i = 1;
for image in newdata:
    plt.subplot(4,6,i)
    plt.imshow(image, 'gray')
    plt.title('Slice ' + str(i))
    plt.xticks([]), plt.yticks([])
    i += 1;
plt.suptitle("Patient 19001: Original Scan")
plt.show()  

# Adaptive Thresholding
newdata_uint8 = np.divide(newdata, newdata.max())
newdata_uint8 = np.multiply(newdata_uint8, 255)
newdata_uint8 = np.array(newdata_uint8, dtype=np.uint8)

i = 1
max_thresh = newdata.max()
for image in newdata_uint8:
    # Image manipulation on slice 18
    left = np.zeros((len(image)/2, len(image[1])))
    for k in range (0,len(image)/2):
        left[k] = image[k]
    left = cv2.blur(left,(5,5))

    right = np.zeros((len(image)/2, len(image[1])))
    for k in range (0,len(image)/2 - 1):
        right[k] = image[len(image)/2 + k]
    # flip around x axis
    right = cv2.flip(right, 0)
    right = cv2.blur(right,(5,5))

    difference = np.subtract(left, right)

    # Simple binary threshold
    for x in range (0,len(difference)):
        for y in range(0, len(difference[1])):
            if (abs(difference[x,y]) > 60):
                difference[x,y] = 1
            else:
                difference[x,y] = 0

    plt.subplot(4,6,i)
    plt.imshow(difference, 'gray')
    plt.title('Slice ' + str(i))
    plt.xticks([]), plt.yticks([])
    i += 1;
plt.suptitle('Patient 19001: Symmetry Subtraction and Thresholding')
plt.show() 


