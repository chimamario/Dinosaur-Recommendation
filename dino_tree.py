
class DinoTree:
    def __init__(self,characteristics, tree_number,tree_level = 0, names = []):
        self.tree_number = tree_number #refers dict key value that holds a num that represents which option the hypothetical user choose
        self.tree_level = tree_level #tells you which level of the tree this node is on
        self.names = names
        self.dinos= [] #holds the names of the dinos
        self.connecting_nodes = {} #holds dict of number connected to actual node value ex: {1:node}
        self.characteristics = characteristics
        self.character_list = [] #a list containing the characteristics of that node (traverses through parent nodes to get more characteristics)
        self.parent_dino = None
        
    
    def add_dino(self,name): #adds dino to respective node
        self.dinos.append(name)
    
    def get_dinos_names(self): #access dino list
        return self.dinos
    
    def add_nodes(self,characteristics, tree_number, tree_level, names = None):
        variable = DinoTree(characteristics, tree_number, tree_level, names)
        if variable.names == None:
            variable.names = []
        
        self.connecting_nodes[variable.tree_number] = variable
    
    def get_dino_nodes(self):
        dino_list = list(self.connecting_nodes.values())
        return dino_list

    
    
    def add_to_character_list(self): #should add all the characteristics even the ones of parents
        self.character_list.append(self.characteristics)
        parent = self.parent_dino
        while parent.tree_level > 0:
            self.character_list.append(parent.characteristics)
            parent = parent.get_parent_dino()

    def get_parent_dino(self):
        return self.parent_dino
    def assign_dino_parent(self, parent_node):
        if self.parent_dino == None:
            self.parent_dino = parent_node
        
    
    #add method that checks the parent of the child so that if it is one, it will add its characteristics only its own list
    #create another method that uses this list above and uses that to filter names
    #has to be method that checks if there are any dino names in the node. if not, then we have to tell the user and go back to the parent node
    