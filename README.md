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
- mri_convert
- dcm2nii

Due to some issues with subprocess not using the correct path, the
absolute path to each command is specified in the python code. Replace
this with the absolute path for your system (output of the command
`which <command>`).
