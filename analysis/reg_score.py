"""
reg_score.py

Scoring functions to determine goodness of registration.
Each score is normalized by the number of voxels in 
the images.

loadNifti(path):
    Load nifti images and return the image
    data in a numpy array.

absValDiff(reg_op_path, ref_path):
    Score based on the absolute value difference voxel
    per voxel. Smaller is better!

ssd(reg_op_path, ref_path):
    Score based on the sum of the squared differences 
    voxel per voxel. Smaller is better!

threshScore(reg_op_path,ref_path):
    Score based on how many voxels are on the same side 
    of a threshold. Returns a percentage. Bigger is better!

"""

import os
import numpy as np
import nibabel as nib

def loadNifti(path):
    img = nib.load(path)
    im_dat = img.get_data()
    return im_dat

def absValDiff(reg_op, ref):
    if (reg_op.shape != ref.shape):
        raise ValueError("Scan shapes must be identical to compare.")
    diff = abs(reg_op - ref)
    score = np.sum(diff) / diff.size
    return score

def ssd(reg_op, ref):
    if (reg_op.shape != ref.shape):
        raise ValueError("Scan shapes must be identical to compare.")
    diff = reg_op - ref 
    diff = diff**2
    score = np.sum(diff) / diff.size
    return score

def threshScore(reg_op, ref):
    if (reg_op.shape != ref.shape):
        raise ValueError("Scan shapes must be identical to compare.")
    threshold = 10
    binary_reg_op = np.greater_equal(reg_op,threshold)
    binary_ref = np.greater_equal(ref,threshold)
    boundary_match = np.equal(binary_reg_op,binary_ref)
    score = float(np.sum(boundary_match)) / boundary_match.size
    return score
