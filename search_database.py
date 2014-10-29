# search_database.py
# 
# This program is the user interface to the database created
# by create_database.py. The goal is to programmatically access
# specific scans by parameters like imaging modality, date, 
# etc. 
#
# In order to have flexibility to fit into other programs, this
# program will simply run a script that will accept parameters
# passed as arguments. If no arguments are detected, the user
# will be prompted to enter search paramters
#
# Usage will be: search_database.py <options> [filename/patientID/imaging_type]]
import sys
import csv

def search(argtype, search_term, path_to_database):
    if (argtype == 'id'):
        results = searchByID(search_term, path_to_database);
        return results;
    elif (argtype == 'modality'):
        results = searchByModality(search_term, path_to_database);
        return results;
    elif ((argtype == 'list') & (search_term == 'modality')):
        results = listTypes(path_to_database);
        return results;
    else:
        print("These are not valid search options. Calling format is 'search_database.search(<options> <argument> <path_to_database>)', where options can be 'id', 'modality', or 'list'.");
        #raise InvalidSearchArgs('Improper parameters were passed to the search function.');
        return -1;

def searchByID(argument, db_path):
    matches = [];
    paths = [];
    with open(db_path, 'rb') as csvfile:
        parser = csv.reader(csvfile, delimiter=',', quotechar='\"');
        for row in parser:
            if (row[0].strip() == argument):
                matches.append(row);
        paths = getPath(matches);
        if (paths == -1):
            print("No matches for the query were found.");
    return paths;


def searchByModality(argument, db_path):
    print("Hooray, we're searching by modality!");
    matches = [];
    paths = [];
    with open(db_path, 'rb') as csvfile:
        parser = csv.reader(csvfile, delimiter=',', quotechar='\"');
        for row in parser:
            try:
                if ((row[6].strip() == argument) | (row[7].strip() == argument)):
                     matches.append(row);
            except IndexError:
                if (row[6] == argument):
                     matches.append(row);
        paths = getPath(matches);
        if (paths == -1):
            print("No matches for the query were found.");
    return paths;

def listTypes(db_path):
    types = [];
    with open(db_path, 'rb') as csvfile:
        parser = csv.reader(csvfile, delimiter=',', quotechar='\"');
        for row in parser:
            try:
                if row[6].strip() not in types: 
                     types.append(row[6].strip());
                elif row[7].strip() not in types:
                     types.append(row[7].strip());
            except IndexError:
                if row[6].strip() not in types:
                     types.append(row[6].strip());
    return types;


def getPath(matches):
    paths = [];
    if (len(matches) == 0):
        print("No matches found. Sorry!");
    else:
        for results in matches:
            temp_path = '';
            for x in results:
                if ((x != " ") & (x != "")):
                    x = x.strip();
                    x = x.strip('"');
                    temp_path += x
                    temp_path += "/";
                else:
                    break;
            paths.append(temp_path);
    return paths;

if __name__ == '__main__':
    # If this script is called, run main
    search(sys.argv[1], sys.argv[2], sys.argv[3]);
