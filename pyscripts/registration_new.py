import dicom
import sys
import os
import magic
import subprocess
import re

# Path for external command
flirt = "/work/03187/rstevens/lonestar/fsl/fsl/bin/flirt";

def main(root_db_dir, output_db_dir):
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
    directories = [x[0] for x in os.walk(root_db_dir)];
    root_split_path = root_db_dir.split("/");
    for path in directories:
        split_path = path.split("/");
        split_path = split_path[len(root_split_path)-1:];
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
    # Now that all file structures are in place, make trees
    db_in = FileTree(root_db_dir);
    db_out = FileTree(output_db_dir);
   
    reference = None; 
    in_scan = None;
    patients = db_in.getPatients();
    for patient in patients:
        dates = db_in.getDates(patient.tag);
        for session in dates:
            modalities = db_in.getModalities(patient, session); 
            for scan in modalities:
            if (re.match('EPITHET_STROKE_PROTOCOL_T2.*', scan.tag)):
                reference = scan;
            if (re.match('EPITHET_STROKE_PROTOCOL_DI.*', scan.tag)):
                in_scan = scan;
            if (reference and in_scan):
                refscan = reference.getScan();    
                input_scan = in_scan.getScan();
                if (refscan and input_scan):
                    # Perform rigid intra-patient registration
                    inpath = "/".join(root_db_dir,patient.tag,session.tag,in_scan.tag, input_scan.tag);
                    refpath = "/".join(root_db_dir,patient.tag,session.tag,reference.tag,refscan.tag);
                    outpath = "/".join(output_db_dir,patient.tag,session.tag,in_scan.tag,input_scan.tag);
                    subprocess.call([flirt, "-dof", "6", "-in", inpath, "-ref", refpath, "-out", (outpath+ ".output.nii.gz")], stdout=devnull); 	
        
            
# Function handle to allow command line passing of arguments
if __name__ == '__main__':
    try:
        main(sys.argv[1], sys.argv[2]);
    except IndexError:
        print("Not enough arguments.\nUsage: db_reg <source_dir> <output_dir>\n");
