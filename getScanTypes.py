import csv

# This dictionary will be how we classify scan types that are the same,
# but are named slightly differently. Use regex to flexibly search, or
# just predefine?
scan_types = [];

def listTypes():
    db_path = 'database.csv';
    matches = [];
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

    for x in types:
        print(x);

listTypes();
