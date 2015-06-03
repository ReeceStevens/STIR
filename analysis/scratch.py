import nibabel as nib
import cv2
import numpy as np
from matplotlib import pyplot as plt

# Load scan from file
img = nib.load('/Users/reecestevens/Downloads/output.nii')
data = img.get_data()
# data = cv2.cvtColor(color_data, cv2.COLOR_BGR2GRAY)
scan_res = data.shape[0]
num_slices = data.shape[2]
newdata = np.zeros([num_slices,scan_res,scan_res])

# Reshape image data for ease of use
for x in range(0, len(data)):
    for y in range(0,len(data[0])):
        for z in range(0,len(data[0,0])):
            newdata[z,x,y] = data[x,y,z]

# Display all slices in the file
""" i = 1;
for image in newdata:
    plt.subplot(4,6,i)
    plt.imshow(image, 'gray')
    plt.title('Slice ' + str(i))
    plt.xticks([]), plt.yticks([])
    i += 1;
plt.show() """

# Adaptive Thresholding
newdata_uint8 = np.divide(newdata, newdata.max())
newdata_uint8 = np.multiply(newdata, 255)
newdata_uint8 = np.array(newdata_uint8, dtype=np.uint8)
plt.imshow(newdata_uint8[16], 'gray')
plt.show()
plt.imshow(newdata[16], 'gray')
plt.show()
i = 1
max_thresh = newdata.max()
for image in newdata_uint8:
    # image = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 201, 0)
    ret, image = cv2.threshold(image, 200,255,cv2.THRESH_BINARY)
    orig_image = image;
    contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(orig_image, contours, -1, (0,255,0), 2)
    plt.subplot(4,6,i)
    plt.imshow(orig_image)
    plt.title('Slice ' + str(i))
    plt.xticks([]), plt.yticks([])
    i += 1;
plt.show()
