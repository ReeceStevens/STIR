import dicom
import sys
import os
import magic
import subprocess

def main(root_db_dir, output_db_dir):
    #root_db_dir = raw_input("Enter root directory of current database: ");
    #output_db_dir = raw_input("Enter root directory of new database: ");
    #root_db_dir = str(root_db_dir);
    #output_db_dir = str(output_db_dir);
	# Open /dev/null for tossing stdout
    devnull = open('/dev/null', 'w');
    try:
        os.makedirs(output_db_dir);
    except OSError:
        if not os.path.isdir(output_db_dir):
            print ("Unable to create new root directory of database. Are you sure you have permissions and file space?\n");
            return;

    directories = [x[0] for x in os.walk(root_db_dir)];
    root_split_path = root_db_dir.split("/");
    for path in directories:
        split_path = path.split("/");
        # Remove root directory from path
        for x in range (len(root_split_path)):
            split_path.pop(0);
        prefix = "";
        for folder in split_path:
            try:
                os.makedirs(output_db_dir + "/" + prefix + folder);
                print("Creating directory " + output_db_dir + "/" + prefix + folder + "\n");
            except OSError:
                if not os.path.isdir(output_db_dir + "/" + prefix + folder):
                    print("Unable to create subdirectories.\n");
                    return;
            prefix += (folder + "/");
        
        # Convert each file within each directory into a DICOM format
        # given that it is either a MINC or DICOM scan type.
        # This is done via a subprocess shell command.
        dir_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))];
        for k in dir_files:
            if (k == ".DS_Store"):
                dir_files.remove(k);
            if (magic.from_file(path + "/" + k) == 'DICOM medical imaging data'):
                ############################################
                # Copy existing DICOM files to new location#
                ############################################
                subprocess.call(['cp', path, (output_db_dir + "/" + prefix)], stdout=devnull);
                print("Dicom file " + k + " successfully copied.\n");
                break;
            if (magic.from_file(path + "/" + k) == 'NetCDF Data Format data'): 
                ###############################################
                # Convert from minc to dicom using mri_convert#
                ###############################################
                split_name = k.split(".");
                subprocess.call(["/corral-repl/utexas/poldracklab/software_lonestar/freesurfer/bin/mri_convert", "--in_type", "minc", (root_db_dir + "/" + prefix + k), (output_db_dir + "/" + prefix + split_name[0] + ".dcm")], stdout=devnull); 
                print(split_name[0] + "has been converted to DICOM format.\n");
    
if __name__ == '__main__':
    try:
        main(sys.argv[1], sys.argv[2]);
    except IndexError:
        print("Not enough arguments.\nUsage: db2dcm <source_dir> <output_dir>\n");
