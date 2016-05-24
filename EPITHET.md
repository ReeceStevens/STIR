Status of EPITHET Database
==========================

Registration
-
Currently, registration only works for T2 reference images and DI images that comply with
the EPITHET file naming convention. There seem to be file errors or data inconsistencies
that make registration very difficult on 3D, perfusion, and other scan types. In addition, 
files with the AX naming convention did not register properly either, possibly due to 
metadata corruption during NIFTI conversion. This requires more investigation. 

The current workflow for analyzing the EPITHET database is as follows:

1. Create the *.csv database record
2. Register each patient's properly-formatted T2 scan to a master T2 scan
3. Registering each patient's DI scan to their previously-registered T2
4. Search the *.csv database record to find a particular patient, modality, or date.

Analysis and Lesion Detection
-
Although emphasis on this portion of the project is dying down, the image analysis tests
that have been performed are recorded in `analysis/comparison.py`. The Python script
currently uses OpenCV to perform symmetry subtraction and thresholding to determine lesion
boundaries, which, while not particularly adaptive, usually serves as a good first pass. 
More adaptive windowing mechanisms will be required if more sensitive lesion detection is 
required.
