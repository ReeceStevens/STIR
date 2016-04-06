# UNDER CONSTRUCTION!

import os

class FileTreeNode:
    parent = None
    children = [] 
    tag = ""
    def __init__(self, tag):
        self.tag = tag;

class FileTree:
    root = None
    # Create a file tree out of a path
    def __init__(self, directory):
        self.root = FileTreeNode(directory, None)
        directories = [x for x in os.walk(self.root)]
        for patient in directories[0][1]:
            self.add(FileTreeNode(patient), self.root)) 
        for path in directories:
            # Skip this path if we're not yet at the bottom-most directory
            if not path[3]:
                continue

    def add(node, parent):
        parent.children.append(node)
        node.parent = parent
                 



    

