
class DinoTree:
    def __init__(self,characteristics, tree_number,tree_level = 0, names = []):
        self.tree_number = tree_number
        self.tree_level = tree_level
        self.names = names
        self.dinos= []
        self.connecting_nodes = {}
        self.characteristics = characteristics
        
    
    def add_dino(self,name):
        self.dinos.append(name)
    
    def add_nodes(self,characteristics, tree_number, tree_level, names = None):
        variable = DinoTree(characteristics, tree_number, tree_level, names)
        if variable.names == None:
            variable.names = []
        
        self.connecting_nodes[variable.tree_number] = variable
    
    #add method that checks the parent of the child so that if it is one, it will add its characteristics only its own list
    #create another method that uses this list above and uses that to filter names
    