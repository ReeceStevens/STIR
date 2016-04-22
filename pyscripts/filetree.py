# UNDER CONSTRUCTION!

import os

class FileTreeNode:
    parent = None
    children = [] 
    tag = ""
    level = None
    def __init__(self, tag):
        self.tag = tag;
        self.children = [];

    # Define the structure level that the node is on
    def setLevel(self, level):
        self.level = level

    def getScan(self):
        if (self.level == 3):
            for k in children:
                if ((not(re.match(".*mask.*", k.tag))) and (not(re.match("co.*", k.tag))) and (not(re.match("o.*", k.tag)))):
                return k;
        return None;


    # Return child node if this node or one of its 
    # children contain child.
    def hasChild(self, child_tag):
        if not self.children:
            return None;
        for node in self.children:
            if (node.tag == child_tag):
                return node;
            found = node.hasChild(child_tag)
            return found;
        return None;

class FileTree:
    root = None
    nodes = {};
    # Create a file tree out of a path
    def __init__(self, directory):
        # Set root folder as the root of the tree
        self.root = FileTreeNode(directory)
        self.root.parent = None;
        self.root.level = 0;

        directories = [x for x in os.walk(self.root.tag)]
        rootpath = self.root.tag.split("/");

        #for patient in directories[0][1]:
        #    self.add(FileTreeNode(patient), self.root)) 

        for path in directories:
            full_path = path[0]
            split_path = full_path.split("/")
            # Remove the root path from the file structure
            split_path = split_path[len(rootpath)-1:]
            # If there aren't three directories above, we aren't at the correct folder.
            if (len(split_path) < 3):
                continue
            # Add directory structure or append to existing parent nodes
            parent = self.root;
            for i in range(len(split_path)):
                new_parent = parent.hasChild(split_path[i]);
                if (new_parent != None):
                    parent = new_parent;
                    continue;
                else:
                    # If node is new, add it 
                    new_node = FileTreeNode(split_path[i]);
                    self.add(new_node,parent);
                    # ... then set it as the parent for the next folder
                    parent = new_node;
            for i in range(len(path[2])):
                self.add(FileTreeNode(path[2][i]), parent);
    
    def getPatients(self):
        patients = {};
        for node in nodes:
            if (node.level == 1):
                patients[node.tag] = node;
        return patients;

    def getDates(self, patient_tag):
        dates = {};
        patient = self.get(patient_tag);
        for child in patient.children:
            dates[child.tag] = child;
        return dates;

    def getModalities(self, patient_tag, date_tag):
        modalities = {};
        patient = self.get(patient_tag);
        for date in patient.children:
            if (date.tag == date_tag):
                for child in date.children:
                    modalities[child.tag] = child;
        return modalities;

    def getAllScans(self):
        scans = {};
        for node in nodes:
            if (node.level == 4):
                scans[node.tag] = node;
        return scans;

    def sameSession(self, scan_a_tag, scan_b_tag);
        scanA = self.get(scan_a_tag);
        scanB = self.get(scan_b_tag);
        # If the patient and date are the same, these scans are from the same session
        if (scanA.parent.parent.parent == scanB.parent.parent.parent) and (scanA.parent.parent == scanB.parent.parent):
            return True;
        else:
            return False;

    def printTree(self):
        self.printTreeRecursive(self.root);

    def printTreeRecursive(self, root):
        if (root == None): 
            return;
        print(root.tag);
        for node in root.children:
            print(node.tag);

    def add(self, node, parent):
        parent.children.append(node)
        node.parent = parent
        node.level = parent.level + 1
        self.nodes[node.tag] = node
    
    def get(self, tag):
        return self.nodes[tag];
