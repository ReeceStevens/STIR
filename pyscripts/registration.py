import dicom
import sys
import os
import magic
import subprocess
import re

def main(root_db_dir, output_db_dir):
    #root_db_dir = raw_input("Enter root directory of current database: ");
    #output_db_dir = raw_input("Enter root directory of new database: ");
    root_db_dir = str(root_db_dir);
    print root_db_dir
    output_db_dir = str(output_db_dir);
    print output_db_dir
	# Open /dev/null for tossing stdout
    devnull = open('/dev/null', 'w');
    try:
        os.makedirs(output_db_dir);
    except OSError:
        if not os.path.isdir(output_db_dir):
            print ("Unable to create new root directory of database. Are you sure you have permissions and file space?\n");
            return;

    reference = ["", ""];
    in_file = ["", ""]; 
    directories = [x[0] for x in os.walk(root_db_dir)];
    root_split_path = root_db_dir.split("/");
    for path in directories:
        split_path = path.split("/");
        # Remove root directory from path
        for x in range (len(root_split_path)):
            split_path.pop(0);
       
        # Select the directories that we know work right now.
        # This means the directories using the AX_* format.
        try:
            if (re.match('AX_FLAIR_.*', split_path[-1])):
                reference = split_path;     
            if (re.match('AX_DIFF_.*', split_path[-1])):
                in_file = split_path;
        except IndexError:
            continue;
        # If the reference and input are from the same patient at the same date, we're ready to run FLIRT
        if (reference[-2] == in_file[-2]) and (reference != ["", ""]) and (in_file != ["", ""]): 
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
            refpath = "/".join(reference);
            refpath = root_db_dir + "/" + refpath;
            inpath = "/".join(in_file);
            inpath = root_db_dir + "/" + inpath;
            dir_files_ref = [f for f in os.listdir(refpath) if os.path.isfile(os.path.join(refpath, f))];
            for k in dir_files_ref:
                if ((not(re.match(".*mask.*", k))) and (not(re.match("co.*", k))) and (not(re.match("o.*", k)))):
                    refpath = "/".join([refpath, k]); 
                    break;

            dir_files_in = [f for f in os.listdir(inpath) if os.path.isfile(os.path.join(inpath, f))];
            for k in dir_files_in:
                if ((not(re.match(".*mask.*", k))) and (not(re.match("co.*", k))) and (not(re.match("o.*", k)))):
                    inpath = "/".join([inpath, k]); 
                    break;

            ############################################################
            # Register a diffusion image with the patient's structural #
            ############################################################
            # print(inpath + " is about to be registered to " + refpath + "...\n");
            subprocess.call(["/work/03187/rstevens/fsl/fsl/bin/flirt", "-in", inpath, "-ref", refpath, "-out", (output_db_dir + "/" + prefix + "output.nii.gz")], stdout=devnull); 	
            reference = ["", ""];
            in_file = ["", ""]; 
            print(inpath + " has been successfully registered to " + refpath + "\n");

if __name__ == '__main__':
    try:
        main(sys.argv[1], sys.argv[2]);
    except IndexError:
        print(sys.argv[0]);
        print(sys.argv[1]);
        print(sys.argv[2]);
        print("Not enough arguments.\nUsage: db_reg <source_dir> <output_dir>\n");
