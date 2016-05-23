STIR Project Files
==================

Python scripts for creating, parsing, and viewing
MRI databases consisting of both MINC and Dicom imaging
formats.

This combination of scripts is designed to create an organized
database of scans that can be analyzed, registered, and segmented
in an automated fashion.

Contents
--------
`pyscripts` - Python scripts for database maintenance and
              applying conversions across the entire database.

`bin` - Bash script wrappers for the registration Python scripts. Add to your PATH 
        environment variable to make execution a lot easier.

`analysis` - Python scripts for image segmentation/analysis as well as 
			 registration quality scoring. Example files included.

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

Programs
--------

- `createdb <name_of_output.csv> </path/to/database>`
	- Creates a CSV file with all scans in the database
	- Assumes a file structure of `patient/date/scan_modality/scanfile.dcm`

- `searchdb <id/modality/list> <search term> </path/to/database.csv>`
	- Searches for a scan in the generated CSV file by id or modality.
	- Returns path of all scans that match the search parameters.
	- Alternate parameter `list` lists all imaging modalities in the database.

- `db2nii <source_dir> <output_dir>`
	- Given a source database of DICOM and MINC files, creates a new database with scans 
	converted to NIFTI format.
	- Most registration software requires that scans be in the NIFTI format.
	- Assumes a file structure of `patient/date/scan_modality/scanfile.(dcm/mnc)`

- `db_reg <source_dir> <output_dir> <optional: # of cores (default 8)>`
	- Given a source database of NIFTI files, register a patient's diffusion scan to their
	structural T2 scan.
	- Registration is performed intra-patient only.
	- Assumes a file structure of `patient/date/scan_modality/scanfile.nii.gz`
	- ***Warning: this code, by default, overwrites the original input scan with the registered scan. Make a copy of your database before running this program.***

- `db_cross_reg <source_dir> <output_dir> <reference_T2_path> <optional: # of cores (default 8)>`
	- Given a source database of NIFTI files, register a patient's structural T2 scan to a 
	reference T2 scan.
	- Registration is performed inter-patient only.
	- Assumes a file structure of `patient/date/scan_modality/scanfile.nii.gz`
	- ***Warning: this code, by default, overwrites the original input scan with the registered scan. Make a copy of your database before running this program.***

Lonestar 5 Notes
----------------
When running on Lonestar 5, some dependencies are pre-installed. Add these programs to your path:

- `mri_convert`: `/corral-repl/utexas/poldracklab/software_lonestar/freesurfer/bin/mri_convert`
- `dcm2nii`: `/corral-repl/utexas/poldracklab/software_lonestar/local/bin/dcm2nii`
- `reg_aladin` (from the nifti_reg package): `/corral-repl/tacc/bio/STIR-data/rstevens/nifti_reg/bin`
[pydicom]: https://github.com/darcymason/pydicom
[libmagic]: https://pypi.python.org/pypi/python-magic
[opencv]: http://opencv.org/
[minctool]: https://github.com/BIC-MNI/minc-toolkit
[mriconvert]: http://freesurfer.net/
[dcm2nii]: https://www.nitrc.org/projects/dcm2nii/
[niftireg_link]: http://cmictig.cs.ucl.ac.uk/wiki/index.php/NiftyReg
