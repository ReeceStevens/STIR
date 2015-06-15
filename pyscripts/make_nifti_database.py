###########################################################################
#                       make_nifti_database.py                            #
# Python script for converting a database of MINC and DICOM scans into    #
# NIFTI format. Uses external programs mri_convert and dcm2nii for        #
# conversion process.                                                     # 
#                                                                         #
# Author: Reece Stevens                                                   #
# Written: February 2015                                                  #
# Last Updated: 6/15/2015                                                 #
###########################################################################
import dicom
import sys
import os
import magic
import subprocess

# Path to external commands
mri_convert = "/corral-repl/utexas/poldracklab/software_lonestar/freesurfer/bin/mri_convert";
dcm2nii = "dcm2nii";


def main(root_db_dir, output_db_dir):
    # Open /dev/null for tossing stdout
    devnull = open('/dev/null', 'w');
    # Check if the correct permissions exist to write to the output location
    try:
        os.makedirs(output_db_dir);
    except OSError:
        if not os.path.isdir(output_db_dir):
            print ("Unable to create new root directory of database. Are you sure you have permissions and file space?\n");
            return;

    # Recursively walk through the database 
    directories = [x[0] for x in os.walk(root_db_dir)];
    root_split_path = root_db_dir.split("/");
    for path in directories:
        split_path = path.split("/");
        # Remove root directory from path
        for x in range (len(root_split_path)):
            split_path.pop(0);
        prefix = "";
        # Build an identical file structure in the output directory
        for folder in split_path:
            try:
                os.makedirs(output_db_dir + "/" + prefix + folder);
                print("Creating directory " + output_db_dir + "/" + prefix + folder + "\n");
            except OSError:
                if not os.path.isdir(output_db_dir + "/" + prefix + folder):
                    print("Unable to create subdirectories.\n");
                    return;
            prefix += (folder + "/");
        
        # Convert each file within each directory into a NIFTI format
        # given that it is either a MINC or DICOM scan type.
        dir_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))];
        for k in dir_files:
            if (k == ".DS_Store"):
                dir_files.remove(k);
            if (magic.from_file(path + "/" + k) == 'DICOM medical imaging data'):
                # Convert from dicom to nifti using dcm2nii
                subprocess.call([dcm2nii, '-o', (output_db_dir + "/" + prefix), path], stdout=devnull);
                print("Dicom file " + k + " successfully converted\n");
                break;
            if (magic.from_file(path + "/" + k) == 'NetCDF Data Format data'): 
                # Convert from minc to nifti using mri_convert
                split_name = k.split(".");
                subprocess.call([mri_convert, "--in_type", "minc", (root_db_dir + "/" + prefix + k), (output_db_dir + "/" + prefix + split_name[0] + ".nii.gz")], stdout=devnull); 
                print(split_name[0] + "has been converted to NIFTI format.\n");
    
# Function handle to allow command line passing of arguments
if __name__ == '__main__':
    try:
        main(sys.argv[1], sys.argv[2]);
    except IndexError:
        print("Not enough arguments.\nUsage: db2nii <source_dir> <output_dir>\n");
