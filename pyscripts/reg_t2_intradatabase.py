###########################################################################
#                       reg_t2_intradatabase.py                           #
# Register the T2 structural scans of each patient to a reference scan    #
# (in this case, the T2 scan of patient 07001). Quality of registration   #
# can be checked by the python packages in the analysis directory.        #
#                                                                         #
# Author: Reece Stevens                                                   #
# Written: November 2015                                                  #
# Last Updated: 05/19/2016                                                #
###########################################################################
import sys
import os
import magic
import subprocess
import re

# Path for external command
reg_aladin = "/work/03187/rstevens/lonestar/nifty_reg/build/bin/reg_aladin" 

def main(root_db_dir, output_db_dir, ref_path="/corral-repl/tacc/bio/STIR-data/rstevens/nifti/07001/20020211T131648/EPITHET_STROKE_PROTOCOL_T2/19020211_131648s010a1001.nii.gz", num_cores=8):
    # Convert arguments to strings
    root_db_dir = str(root_db_dir) 
    output_db_dir = str(output_db_dir) 
    # Open /dev/null for tossing stdout
    devnull = open('/dev/null', 'w') 

    # Check if the correct permissions exist to write to the output location
    try:
        os.makedirs(output_db_dir) 
    except OSError:
        if not os.path.isdir(output_db_dir):
            print ("Unable to create new root directory of database. Are you sure you have permissions and file space?\n") 
            return 
    # Walk through each directory and add scans.
    directories = [x[0] for x in os.walk(root_db_dir)] 
    root_split_path = root_db_dir.split("/") 
    for path in directories:
        split_path = path.split("/") 
        # Remove root directory from path
        for x in range (len(root_split_path)):
            split_path.pop(0) 
       
        # Select the directories that we know work right now.
        # This means the directories using the AX_* or EPITHET_* formats.
        scans = [] 
        try:
            # EPITHET-formatted scans
            if (re.match('EPITHET_STROKE_PROTOCOL_T2.*', split_path[-1])):
                scans.append(split_path) 
        # Ignore index errors, they're just empty paths
        except IndexError:
            pass  
        # If no scans were found, skip (nothing to register)
        if (len(scans) < 1):
            continue 
        # Otherwise, go through each file and register
        for in_file in scans: 
            prefix = "" 
            # Build an identical file structure in the output directory
            for folder in split_path:
                try:
                    os.makedirs(output_db_dir + "/" + prefix + folder) 
                    print("Creating directory " + output_db_dir + "/" + prefix + folder + "\n") 
                except OSError:
                    if not os.path.isdir(output_db_dir + "/" + prefix + folder):
                        print("Unable to create subdirectories.\n") 
                        return 
                prefix += (folder + "/") 
            # Prepare file paths for reference and input files
            inpath = "/".join(in_file) 
            inpath = root_db_dir + "/" + inpath 
            dir_files_in = [f for f in os.listdir(inpath) if os.path.isfile(os.path.join(inpath, f))] 
            for k in dir_files_in:
                # Use regex to make sure we're matching the correct file, not a mask or byproduct of other scan conversions
                if ((not(re.match(".*mask.*", k))) and (not(re.match("co.*", k))) and (not(re.match("o.*", k)))):
                    inpath = "/".join([inpath, k])  
                    break 
            # Register the patient's T2 scan to the reference T2
            subprocess.call([reg_aladin, "-flo", inpath, "-ref", ref_path, "-res", (output_db_dir + "/" + prefix + in_file[-1] + ".output.nii.gz"),"-omp", str(num_cores)], stdout=devnull)  	
            subprocess.call(["mv", (output_db_dir + "/" + prefix + in_file[-1] + ".output.nii.gz"), inpath]) 
            print(inpath + " has been successfully registered to " + ref_path + "\n") 

# Function handle to allow command line passing of arguments
if __name__ == '__main__':
    try:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]) 
    except IndexError:
        try:
            main(sys.argv[1], sys.argv[2], sys.argv[3]) 
        except IndexError:
            try:
                main(sys.argv[1], sys.argv[2]) 
            except IndexError:
                print("Not enough arguments.\nUsage: db_reg <source_dir> <output_dir> <reference path> <optional: number of cores>\n") 
