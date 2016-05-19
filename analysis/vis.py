######################################################
#                                                    #
# vis.py                                             #
# A script for investigating the quality of scan     #
# registration. Calculates three different scoring   #
# metrics for scan quality, both before and after    #
# registration, then displays the registration       #
# results via matplotlib.                            #
#                                                    #
# Last Updated: 5/19/16                              #
######################################################

import sys
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import reg_score as r

sliceno = 10
file1path = ""
file2path = ""
file3path = ""
if (len(sys.argv) != 4):
    raise ValueError("Incorrect Arguments. Syntax is: python vis.py <original> <reference> <output>")
else:
    file1path = sys.argv[1]
    file2path = sys.argv[2]
    file3path = sys.argv[3]

img = r.loadNifti(file1path)
ref_img = r.loadNifti(file2path) 
img2 = r.loadNifti(file3path)

# Correct for size mismatch in original
img = img[:,:,0:19]

print("Original Abs. Val. Score: " + str(r.absValDiff(img, ref_img)))
print("New Abs. Val. Score: " + str(r.absValDiff(img2, ref_img)))
print("Original Squared Difference Score: " + str(r.ssd(img, ref_img)))
print("New Squared Difference Score: " + str(r.ssd(img2, ref_img)))
print("Original Binary Threshold Score: " + str(r.threshScore(img,ref_img)))
print("New Binary Threshold Score: " + str(r.threshScore(img2,ref_img)))

plt.subplot(1,4,1)
plt.imshow(img[:,:,sliceno])
plt.subplot(1,4,2)
plt.imshow(ref_img[:,:,sliceno])
plt.subplot(1,4,3)
plt.imshow(img2[:,:,sliceno])
plt.subplot(1,4,4)
plt.imshow(img2[:,:,sliceno] - img[:,:,sliceno])

plt.show()
