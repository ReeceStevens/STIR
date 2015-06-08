STIR Project Files
==================

Python scripts for creating, parsing, and viewing
MRI databases consisting of both MINC and Dicom imaging
formats.

This combination of scripts is designed to create an organized
database of scans that can be analyzed, registered, and segmented
in an automated fashion.

Currently in development: automatic image segmentation using
OpenCV. 

Dependencies
------------

Python libraries used in these scripts include:

- PyDicom
- Magic
- OpenCV (cv2)

Command line tools called as subprocess commands:
- Minc Toolkit
- mri_convert
- dcm2nii

Due to some issues with subprocess not using the correct path, the
absolute path to each command is specified in the python code. Replace
this with the absolute path for your system (output of the command
`which <command>`).
