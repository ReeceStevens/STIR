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

Contents
--------
`pyscripts` - Contains the Python scripts for database maintenance and
              applying conversions across the entire database.

`bin` - Bash script wrappers for the Python scripts. Add to your PATH 
        environment variable to make execution a lot easier.

`analysis` - Working directory for the image segmentation scripts. 
             Currently in development.

`registration` - A template job submission script for Lonestar. Can be 
                 modified for any job submission.

Dependencies
------------

Python libraries used in these scripts include:

- [PyDicom][pydicom]
- [libmagic][libmagic]
- [OpenCV (cv2)][opencv]

Command line tools called as subprocess commands:
- [Minc Toolkit][minctool]
- [mri_convert (from Freesurfer package)][mriconvert]
- [dcm2nii][dcm2nii]
- [nifti_reg][niftireg_link]

Due to some issues with subprocess not using the correct path, the
absolute path to each command is specified in the python code. Replace
this with the absolute path for your system (output of the command
`which <command>`).


[pydicom]: https://github.com/darcymason/pydicom
[libmagic]: https://pypi.python.org/pypi/python-magic
[opencv]: http://opencv.org/
[minctool]: https://github.com/BIC-MNI/minc-toolkit
[mriconvert]: http://freesurfer.net/
[dcm2nii]: https://www.nitrc.org/projects/dcm2nii/
[niftireg_link]: http://cmictig.cs.ucl.ac.uk/wiki/index.php/NiftyReg
