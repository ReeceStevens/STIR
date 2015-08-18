import nibabel as nib
import cv2
import numpy as np
from matplotlib import pyplot as plt

# Load scan from file
img = nib.load('/Users/reecestevens/scans/07001/20020211T131648/EPITHET_STROKE_PROTOCOL_DI/output.nii.gz')
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
""" plt.imshow(newdata_uint8[16], 'gray')
plt.show()
plt.imshow(newdata[16], 'gray')
plt.show() """
i = 1
max_thresh = newdata.max()
for image in newdata_uint8:
    #image = cv2.GaussianBlur(image, (5,5),0)
    # image = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 0)
    # ret, image = cv2.threshold(image, 0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    #ret, image = cv2.threshold(image,115,255,cv2.THRESH_BINARY)

    # Calculate average intensity for the image slice
    """ k = 0
    average = 0
    for x in image:
        for y in x:
            # Ignore low intensity areas (background, CSF)
            if (y <= 30):
                continue
            k = k + 1
            average = average + y
    if (k != 0):
        average = average / k
    else:
        average = 0

    # Threshold determined by values that are two standard deviations away from the adjusted mean
    std_image = np.std(image)
    thresh = average + std_image*2
    orig_image = image """

    # contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(orig_image, contours, len(contours)-1, (0,255,0), 2)
    # ret, image = cv2.threshold(image,thresh,255,cv2.THRESH_BINARY)
    # orig_image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2GRAY)
    # combined = cv2.addWeighted(orig_image, 0.5, image, 0.5, 0.0)

    # Image manipulation on slice 18
    left = np.zeros((len(image)/2, len(image[1])))
    for k in range (0,len(image)/2):
        left[k] = image[k]
    left = cv2.blur(left,(5,5))
    # plt.imshow(left)

    right = np.zeros((len(image)/2, len(image[1])))
    for k in range (0,len(image)/2 - 1):
        right[k] = image[len(image)/2 + k]
    # flip around x axis
    right = cv2.flip(right, 0)
    right = cv2.blur(right,(5,5))
    # plt.imshow(right)

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


