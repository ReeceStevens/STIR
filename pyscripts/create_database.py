###########################################################################
#                       create_database.py                                #
# Python script to recursively parse a database of scans, determine their #
# file types, and produce a .csv file mapping the layout of the databse.  #
#                                                                         # 
# Author: Reece Stevens                                                   #
# Written: October 2014                                                   #
# Last Updated: 6/15/2015                                                 #
###########################################################################

import dicom
import os
import magic
import re
from subprocess import check_output
from subprocess import CalledProcessError

# Output .csv file name
data_table = 'database.csv'; 

###########################################################################
# fileCount() - counts the number of relevant files in the database.      #
###########################################################################
def fileCount(path):
        
    dir_contents = os.listdir(path);
    all_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))];

    for k in all_files:
        if (k == ".DS_Store"):
            all_files.remove(k);
        p = re.compile("csf", re.IGNORECASE);
        if (p.match(k) != None):
            all_files.remove(k);
    
    if (len(all_files) == 0):
        print("Passing through the directory: " + path);

    return len(all_files);

####################################################################################
# dirFileRead() - parses files in the given directory for metadata and returns it  #
#                 in a list already formatted for the output csv. Supports metadata# 
#                 from DICOM and MINC files                                        #
####################################################################################
def dirFileRead(path, parameters):
    dir_contents = os.listdir(path);
    dicom_files = [];
    mnc_files = [];
    attributes = [];
    all_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))];
    
    # If there are no files in the directory, return empty attributes list and exit.
    if (len(all_files) == 0):
        print("Passing through the directory: " + path);
        return attributes;

    # Otherwise, check each file
    for k in all_files:
        if (k == ".DS_Store"): # remove this hidden file
            all_files.remove(k);
            continue;
        
        # Detect DICOM files
        if (magic.from_file(path + "/" + k) == 'DICOM medical imaging data'):
           dicom_files.append(path + "/" + k);
           dm = dicom.read_file(dicom_files[0]); # extract file information

           # Extract each desired parameter and insert it into the output list.
           for x in parameters:
              try:
                  param_info = "dm." + x;
                  output = eval(param_info); # extract a single parameter in dm
              except AttributeError, e:
                  continue;
              if str(output) not in attributes: # prevent duplicate entries
                  attributes.append(str(output));

        # Detect MINC files
        elif (magic.from_file(path + "/" + k) == 'NetCDF Data Format data'):
            mnc_files.append(path + "/" + k);
            # extract file information
            try:
                att = check_output(['mincinfo', '-attvalue', 'acquisition:scanning_sequence', (path + '/' + k)]);
                att = att[0:(len(att)-1)];
            # if information isn't available, skip the file and keep going
            except CalledProcessError, e:
                all_files.remove(k);
                print("MINC file lacking modality variable.");
                continue;
            if att not in attributes: # prevent duplicates
                attributes.append(att);
    return attributes; 

        

def main(root_dir):
    # Determine desired parameters and root directory
    parameters = raw_input("For DICOM files, what parameters would you like to put in the database? Options are: SeriesDescription, Rows, Columns, ImageGeometryType ([a] for all) ");
    if (parameters == "a"):
        parameters = ["SeriesDescription", "Rows", "Columns", "ImageGeometryType"];
    else:
        parameters = list(parameters);
    root_dir = str(root_dir);
    working_dir = root_dir;
    root_dir_split = root_dir.split("/");

    # Begin parsing through the database
    directories = [x[0] for x in os.walk(root_dir)];
    with open(data_table, "a") as myfile:
        for d in directories:
            num_files = fileCount(d);
            file_attributes = dirFileRead(d, parameters);
            if (num_files != 0):
                split_path = d.split("/");
                for q in range (len(root_dir_split)):
                    split_path.pop(0);          # Removes the root directory from the table
                for x in split_path:
                    myfile.write("\"" + x + "\" , ");
                spaces = 4 - len(split_path);
                for j in range(spaces):
                    myfile.write(", ");
                myfile.write(", ");             # Add one last space to signify end of path
                myfile.write(str(num_files) + ", ");
                if (len(file_attributes) != 0):
                    for k in file_attributes:
                        myfile.write(k);
                        myfile.write(", ");
                myfile.write("\n");

# Function handle to allow command line passing of arguments
if __name__ == '__main__':
    # If this script is called, run main
    try: 
        data_table = sys.argv[1];
        main(sys.argv[2]);
    except IndexError: 
        print("Not enough arguments.\nUsage: searchdb <id/modality/list> <search term> <path/to/database.csv>");
        

