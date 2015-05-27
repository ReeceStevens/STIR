import nibabel as nib
import cv2
import numpy as np
from matplotlib import pyplot as plt

img = nib.load('/Users/reecestevens/Downloads/output.nii')
data = img.get_data()

for x in range(0, len(data)):
    for y in range(0,len(data[0])):
        for z in range(0,len(data[0,0])):
            newdata[z,x,y] = data[x,y,z]


