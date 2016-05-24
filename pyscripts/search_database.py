##################################################################################
#                           search_database.py                                   #
# This program is the user interface to the database created                     #
# by create_database.py. The goal is to programmatically access                  #
# specific scans by parameters like imaging modality, date,                      #
# etc.                                                                           #
#                                                                                #
# In order to have flexibility to fit into other programs, this                  #
# program will simply run a script that will accept parameters                   #
# passed as arguments. If no arguments are detected, the user                    #
# will be prompted to enter search paramters                                     #
#                                                                                #
# Usage will be: search_database.py <options> [filename/patientID/imaging_type]] #
#                                                                                #
# Author: Reece Stevens                                                          #
# Written: December 2014                                                         #
# Last Updated: 6/15/2015                                                        #
##################################################################################
import sys
import csv


###############################################################################
# search() - parses the database pointed to by path_to_database  with respect #
#            to variable argtype for search_term.                             #
###############################################################################
def search(argtype, search_term, path_to_database):
    if not verifyDB(path_to_database):
        raise ValueError("Invalid database. Please create database with createdb program.")
    i = 0;
    if (argtype == 'id'):
        results = searchByID(search_term, path_to_database);
        for each in results:
            print each;
            i += 1;
        print("\nTotal number of results found: " + str(i));
        return results;
    elif (argtype == 'modality'):
        results = searchByModality(search_term, path_to_database);
        for each in results:
            print (each);
            i += 1;
        print("\nTotal number of results found: " + str(i));
        return results;
    elif ((argtype == 'list') & (search_term == 'modality')):
        results = listTypes(path_to_database);
        for each in results:
            print each;
            i += 1;
        print("\nTotal number of results found: " + str(i-1)); # Remove header from count
        return results;
    else:
        print("These are not valid options.\n Usage: searchdb <id/modality/list> <search term> <path/to/database.csv>");
        return -1;

###############################################################################
# searchByID() - Recurse through database and find any IDs that match         #
#                argument. Return the paths of all matching entries.          #
###############################################################################
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


###############################################################################
# searchByModality() - Recurse through database and find any modalities that  #
#                      match argument. Return the paths of all matching       #
#                      entries.                                               #
###############################################################################
def searchByModality(argument, db_path):
    matches = [];
    paths = [];
    with open(db_path, 'rb') as csvfile:
        parser = csv.reader(csvfile, delimiter=',', quotechar='\"');
        for row in parser:
            if (row[2].strip() == str(argument)):
                matches.append(row);
        paths = getPath(matches);
        if (paths == -1):
            print("No matches for the query were found.");
            return;
    return paths;

###########################################################################
# listTypes() - displays a complete list of all scanning modalities in    #
#               the database.                                             #
###########################################################################
def listTypes(db_path):
    types = [];
    with open(db_path, 'rb') as csvfile:
        parser = csv.reader(csvfile, delimiter=',', quotechar='\"');
        for row in parser:
            if row[2].strip() not in types: 
                 types.append(row[2].strip());
    return types;

###########################################################
# getPath() - return the paths of all entries in matches. #
###########################################################
def getPath(matches):
    paths = [];
    if (len(matches) == 0):
        print("No matches for the query were found.");
    else:
        for results in matches:
            temp_path = '';
            for x in results:
                if ((x != " ") and (x != "")):
                    x = x.strip();
                    x = x.strip('"');
                    temp_path += x
                    temp_path += "/";
                else:
                    break;
            paths.append(temp_path);
    return paths;

##########################################################################
# verifyDB() - ensure that this db was generated by createdb by checking #
#              the database header                                       #
##########################################################################
def verifyDB(db_path):
    with open(db_path, 'rb') as csvfile:
        parser = csv.reader(csvfile, delimiter=',', quotechar='\"');
        for row in parser:
            try:
                if (row[0].strip() == "Patient"):
                    return True
                else:
                    return False
            except IndexError:
                return False
            

# Function handle to allow command line passing of arguments
if __name__ == '__main__':
    # If this script is called, run main
    try: 
        search(sys.argv[1], sys.argv[2], sys.argv[3]);
    except IndexError: 
        print("Not enough arguments.\nUsage: searchdb <id/modality/list> <search term> <path/to/database.csv>");
        
