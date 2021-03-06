###########################################################################
#                       registration.py                                   #
# Python script for performing registration on each file in the output    #
# of the make_bet_database.py script. Registers every diffusion-based     #
# scan to a high-definition structural scan. Currently only registers     #
# a patient to themselves.                                                #
#                                                                         #
# Author: Reece Stevens                                                   #
# Written: May 2015                                                       #
# Last Updated: 4/6/2016                                                  #
###########################################################################
import sys
import os
import magic
import subprocess
import re

# Path for external command
reg_aladin = "/work/03187/rstevens/lonestar/nifty_reg/build/bin/reg_aladin";

def main(root_db_dir, output_db_dir, num_cores=8):
    # Convert arguments to strings
    root_db_dir = str(root_db_dir);
    output_db_dir = str(output_db_dir);
    # Open /dev/null for tossing stdout
    devnull = open('/dev/null', 'w');
    # Check if the correct permissions exist to write to the output location
    try:
        os.makedirs(output_db_dir);
    except OSError:
        if not os.path.isdir(output_db_dir):
            print ("Unable to create new root directory of database. Are you sure you have permissions and file space?\n");
            return;

    # Generate empty variable for the reference scan
    reference = ["", ""];
    # Walk through each directory and add scans.
    directories = [x[0] for x in os.walk(root_db_dir)];
    root_split_path = root_db_dir.split("/");
    for path in directories:
        split_path = path.split("/");
        # Remove root directory from path
        for x in range (len(root_split_path)):
            split_path.pop(0);
       
        try:
            if (re.match('EPITHET_STROKE_PROTOCOL_T2.*', split_path[-1])):
                reference = split_path;     
        except IndexError:
            # No known reference image found. Skipping path.
            continue;
        scans = [];
        try:
            # EPITHET-formatted scans
            if (re.match('EPITHET_STROKE_PROTOCOL_DI.*', split_path[-1])):
                scans.append(split_path);
        # Ignore index errors, they're just empty paths
        except IndexError:
            pass; 
        # If no scans were found, skip (nothing to register)
        if (len(scans) < 1):
            continue;
        # Otherwise, go through each file and register
        print scans;
        print reference;
        for in_file in scans: 
            # If the reference and input are from the same patient at the same date, we're ready to register
            if (reference[-2] == in_file[-2]) and (reference != ["", ""]) and (in_file != ["", ""]): 
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
                # Prepare file paths for reference and input files
                refpath = "/".join(reference);
                refpath = root_db_dir + "/" + refpath;
                inpath = "/".join(in_file);
                inpath = root_db_dir + "/" + inpath;
                dir_files_ref = [f for f in os.listdir(refpath) if os.path.isfile(os.path.join(refpath, f))];
                for k in dir_files_ref:
                    # Use regex to make sure we're matching the correct file, not a byproduct of BET
                    if ((not(re.match(".*mask.*", k))) and (not(re.match("co.*", k))) and (not(re.match("o.*", k)))):
                        refpath = "/".join([refpath, k]); 
                        break;

                dir_files_in = [f for f in os.listdir(inpath) if os.path.isfile(os.path.join(inpath, f))];
                for k in dir_files_in:
                    # Use regex to make sure we're matching the correct file, not a byproduct of BET
                    if ((not(re.match(".*mask.*", k))) and (not(re.match("co.*", k))) and (not(re.match("o.*", k)))):
                        inpath = "/".join([inpath, k]); 
                        break;

                # Register a diffusion image with the patient's structural
                subprocess.call([reg_aladin, "-flo", inpath, "-ref", refpath, "-res", (output_db_dir + "/" + prefix + in_file[-1] + ".output.nii.gz"), "-omp", str(num_cores)], stdout=devnull); 	
                reference = ["", ""];
                subprocess.call(["mv", (output_db_dir + "/" + prefix + in_file[-1] + ".output.nii.gz"), "inpath"]);
                print(inpath + " has been successfully registered to " + refpath + "\n");	
                reference_output = refpath.split("/");
                subprocess.call(["cp", refpath, output_db_dir + "/" + prefix + reference_output[-1]]);

# Function handle to allow command line passing of arguments
if __name__ == '__main__':
    if (sys.argv[3] is not None):
        main(sys.argv[1], sys.argv[2], sys.argv[3]);
    else:
        try:
            main(sys.argv[1], sys.argv[2]);
        except IndexError:
            print("Not enough arguments.\nUsage: db_reg <source_dir> <output_dir>\n");
