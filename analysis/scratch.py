import nibabel as nib
import cv2
import numpy as np
from matplotlib import pyplot as plt

# Load scan from file
img = nib.load('/Users/reecestevens/Downloads/output.nii')
data = img.get_data()
newdata = np.zeros([24,256,256])

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
plt.show()

# Simple Thresholding
thresh_data = np.zeros([24,256,256])
ret,thresh = cv2.threshold(data,200,255,cv2.THRESH_BINARY)
for x in range(0, len(data)):
    for y in range(0,len(data[0])):
        for z in range(0,len(data[0,0])):
            thresh_data[z,x,y] = thresh[x,y,z]
i = 1;
for image in thresh_data:
    plt.subplot(4,6,i)
    plt.imshow(image, 'gray')
    plt.title('Slice ' + str(i))
    plt.xticks([]), plt.yticks([])
    i += 1;
plt.show()
