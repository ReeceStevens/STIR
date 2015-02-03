STIR Project Files
==================

Python scripts for creating, parsing, and viewing
MRI databases consisting of both MINC and Dicom imaging
formats.

Now has the capability to convert databases of mixed MINC and 
DICOM files into a single database of NIFTI formatted files.

Dependencies
------------

Python libraries used in these scripts include:

- PyDicom
- Magic
- Pillow (fork of Python Imaging Library)

Command line tools called as subprocess commands:
- Minc Toolkit
- mnc2nii
- dcm2nii

Ensure that the command line tools are located in your PATH variable.
