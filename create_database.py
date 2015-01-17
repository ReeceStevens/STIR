import dicom
import os
import magic
import re
from subprocess import check_output
from subprocess import CalledProcessError


data_table = 'database.csv'; 
dicom_fields = {'SeriesDescription':[0x0008,0x103E] , 'Rows':[0x0028,0x0010] , 'Columns':[0x0028,0x0011] , 'ImageGeometryType':[

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

def dirFileRead(path, parameters):
    dir_contents = os.listdir(path);
    dicom_files = [];
    mnc_files = [];
    attributes = [];
    all_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))];
   
    # ignore the .DS_store file that appears in every directory
    for k in all_files:
        if (k == ".DS_Store"):
            all_files.remove(k);
       # p = re.compile("csf", re.IGNORECASE);
       # if (p.match(k) != None):
       #     all_files.remove(k);

        if (magic.from_file(path + "/" + k) == 'DICOM medical imaging data'):
           dicom_files.append(path + "/" + k);
           dm = dicom.read_file(dicom_files[0]);

          #############################################

          for x in parameters:
              try:
                  param_info = "dm." + x;
              except AttributeError, e:
                  continue;
              if param_info not in attributes:

          #############################################

           # Extract the Series Description
           try:
                series_info = dm.SeriesDescription;
           except AttributeError, e:
                continue;
           if dm.SeriesDescription not in attributes:
               description = '';
               for x in dm.SeriesDescription:
                    description += x;
               attributes.append(description);


        elif (magic.from_file(path + "/" + k) == 'NetCDF Data Format data'):
            mnc_files.append(path + "/" + k);
            try:
                att = check_output(['mincinfo', '-attvalue', 'acquisition:scanning_sequence', (path + '/' + k)]);
                att = att[0:(len(att)-1)];
            except CalledProcessError, e:
                all_files.remove(k);
                print("MINC file lacking modality variable.");
                continue;
            if att not in attributes:
                attributes.append(att);

    if (len(all_files) == 0):
        print("Passing through the directory: " + path);
        
    return attributes; 

def main():
    # Load all files in current directory
    # Need to extend this for intelligently navigating the database directory
    parameters = input("For DICOM files, what parameters would you like to put in the database?\nOptions are: SeriesDescription, Rows, Columns, ImageGeometryType ([a] for all) ");
    if (parameters == "a"):
        parameters = ["SeriesDescription", "Rows", "Columns", "ImageGeometryType"];
    else:
        parameters = list(parameters);
    root_dir = raw_input("Enter root directory of database: ");
    working_dir = root_dir;
    root_dir_split = root_dir.split("/");

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

main()

