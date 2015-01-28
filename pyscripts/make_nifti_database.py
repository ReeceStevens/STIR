import dicom
import os
import magic
import subprocess

def main:
    root_db_dir = raw_input("Enter root directory of current database: ");
    output_db_dir = raw_input("Enter root directory of new database: ");
    try:
        os.makedirs(output_db_dir);
    except OSError:
        if not os.path.isdir(path):
            print ("Unable to create new root directory of database. Are you sure you have permissions and file space?\n");

    directories = [x[0] for x in os.walk(root_db_dir);
    for path in directories:
        split_path = path.split("/");
    # Duplicate database directory structure and save nifti files in the mirrored db
