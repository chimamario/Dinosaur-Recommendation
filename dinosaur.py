import pandas as pd
import numpy as np
from dino_tree import DinoTree

df = pd.read_csv(r"/Users/mariochima/Desktop/my first folder/coding folder/recommendation project/jurassic_park_data.csv")

#filling in any empty spaces in data
df['lived_in'].fillna('Other', inplace = True)

#shortening period section in dataset
modified_unique_periods = []

for period in df["period"]:
    if "Early Jurassic" in period:
        modified_unique_periods.append("Early Jurassic" )
    elif "Mid Jurassic" in period:
        modified_unique_periods.append("Mid Jurassic")
    elif "Late Jurassic" in period:
        modified_unique_periods.append("Late Jurassic")
    elif "Early Cretaceous" in period:
        modified_unique_periods.append("Early Cretaceous")
    elif "Mid Cretaceous" in period:
        modified_unique_periods.append("Mid Cretaceous")
    elif "Late Cretaceous" in period:
        modified_unique_periods.append("Late Cretaceous")
    elif "Early Triassic" in period:
        modified_unique_periods.append("Early Triassic")
    elif "Mid Triassic" in period:
        modified_unique_periods.append("Mid Triassic")
    elif "Late Triassic" in period:
        modified_unique_periods.append("Late Triassic")
    else:
        modified_unique_periods.append(period)

df["period"] = modified_unique_periods

#adding continents as another section
country_to_continent = { 
    "South Africa": "Africa","Egypt" : "Africa" , "Niger" : "Africa" ,"North Africa" : "Africa" , "Zimbabwe" : "Africa" , 
    "Morroco" : "Africa" , "Tanzania" : "Africa" ,"Madagascar" : "Africa" , "Lesotho" : "Africa" ,  "Malawi" : "Africa" , "Tunisia": "Africa" ,

    "France": "Europe",  "Spain" : "Europe", "Germany" : "Europe", "United Kingdom" : "Europe", "Wales":"Europe",
    "Romania" : "Europe",  "Russia" : "Europe", "Switzerland": "Europe",

    "USA":"North America", "Canada": "North America",

    "Argentina": "South America", "Uruguay":"South America", "Brazil":"South America",

    "Mongolia":"Asia", "China":"Asia","Kazakhstan":"Asia","Uzebekistan":"Asia", "India":"Asia", "Japan":"Asia",

    "Australia":"Other", "Antarctica":"Other" , "Other": "Other"        
         }

df['continent'] = df['lived_in'].map(country_to_continent)

#filled continent column that has missing values
df['continent'].fillna('Other', inplace = True)

#This section gets the unique values of diets, continents, period,
###created lists of unique values for each column listed above
###created dictionary to hold unique value for each column listed above

columns_for_iteration = ['diet', 'period', 'continent', 'type'] 

list_of_diets = df['diet'].unique().tolist()
list_of_period = df['period'].unique().tolist()
list_of_continent = df['continent'].unique().tolist()
list_of_types = df['type'].unique().tolist()

list_of_unique_lists = [list_of_diets,list_of_period, list_of_continent, list_of_types]

dict_of_diet = {}
dict_of_period = {}
dict_of_continent = {}
dict_of_type = {}

list_of_unique_dicts = [dict_of_diet, dict_of_period, dict_of_continent, dict_of_type]

for idx in range(0,len(list_of_unique_lists)):
    for value in list_of_unique_lists[idx]:
        value_value = df[df[columns_for_iteration[idx]] == value]
        list_of_unique_dicts[idx][value] = value_value['name'].to_list()


#creating idx reference for different values

diet_numbers = list(range(0,len(dict_of_diet)))
period_numbers = list(range(0,len(dict_of_period)))
continent_numbers = list(range(0,len(dict_of_continent)))
type_numbers = list(range(0,len(dict_of_type)))

diet_reference = dict(zip(dict_of_diet.keys(), diet_numbers)) #we either have to do this manually or find a way to make this auto
period_reference = dict(zip(dict_of_period.keys(), period_numbers))
continent_reference = dict(zip(dict_of_continent.keys(), continent_numbers))
type_reference = dict(zip(dict_of_type.keys(), type_numbers))


#creating Dino tree structure 

##ZERO TREE LEVEL
first_dino = DinoTree(None, 1)

##FIRST TREE LEVEL
for diet, names in dict_of_diet.items():
    first_dino.add_nodes(diet,diet_reference[diet],1)

for node in first_dino.connecting_nodes.values(): #this line is going thorugh every child node
    for name in dict_of_diet[node.characteristics]: #this line uses the characteristic of node to filter out dictionary to add respective dinos
        node.add_dino(name)
##ENDING FIRST TREE/ SECOND TREE LEVEL
for node in first_dino.connecting_nodes.values():
    node.assign_dino_parent(first_dino)
    node.add_to_character_list()
    #add assign dino parent and character list transverse
    for period, names in dict_of_period.items(): #created period children nodes
        node.add_nodes(period,period_reference[period],2)

for diet_node in first_dino.connecting_nodes.values(): #iterating through period nodes to add respective dinosaurs
    period_nodes = diet_node.get_dino_nodes()

    for node in period_nodes: #assigning dino parents and adding to charcter_list first
        node.assign_dino_parent(diet_node)
        node.add_to_character_list()
    
    for node in period_nodes: #now add dino names based off character list
        for name in dict_of_period[node.characteristics]:
            if name in dict_of_diet[node.character_list[1]]: #note that the parent node character idx is AFTER THE CHILD
                node.add_dino(name)
        # print(f" list is for {node}. these are the dino names {node.get_dinos_names()}")

##THIRD TREE LEVEL

diet_node_list = first_dino.get_dino_nodes()

for diet_node in diet_node_list:  #access period nodes
    period_nodes = diet_node.get_dino_nodes() 

    for period_node in period_nodes:
        if period_node.dinos != []: #we only want to add children nodes to parent nodes that have dino values
            for continent, names in dict_of_continent.items():
                period_node.add_nodes(continent, continent_reference[continent], 3)
    for period_node in period_nodes:
        if period_node.dinos != []:
            continent_nodes = period_node.get_dino_nodes() #access continent nodes
            for node in continent_nodes: #assign parent node and add characterisitic to charcterisitic list
                node.assign_dino_parent(period_node)
                node.add_to_character_list()
    
            for node in continent_nodes: # we will only add dino to node if name can be found in the diet and period dictionaries also
                for name in dict_of_continent[node.characteristics]:
                    if name in dict_of_diet[node.character_list[2]] and name in dict_of_period[node.character_list[1]]:
                        node.add_dino(name)
                # print(f"this is the period (parent) node characteristic: {period_node.characteristics}")
                # print(f" list is for {node.characteristics} with {node.parent_dino.characteristics} parent node. these are the dino names {node.get_dinos_names()}")
    
## FOURTH TREE LEVEL
diet_node_list = first_dino.get_dino_nodes()

for diet_node in diet_node_list:  #access period nodes
    period_nodes = diet_node.get_dino_nodes() 
    for period_node in period_nodes:
        continent_nodes = period_node.get_dino_nodes()
        for continent_node in continent_nodes:
            if continent_node.dinos != []:
                for type, names in dict_of_type.items():
                    continent_node.add_nodes(type, type_reference[type], 4)
        for continent_node in continent_nodes:
            if continent_node.dinos != []:
                type_nodes = continent_node.get_dino_nodes()
                for node in type_nodes:
                    node.assign_dino_parent(continent_node)
                    node.add_to_character_list()
                
                for node in type_nodes:
                    for name in dict_of_type[node.characteristics]:
                        if name in dict_of_diet[node.character_list[3]] and name in dict_of_period[node.character_list[2]] and name in dict_of_continent[node.character_list[1]]:
                            node.add_dino(name)
                    # if node.dinos != []:
                        # print(f" list is for {node.characteristics} with {node.parent_dino.characteristics} parent node. these are the dino names {node.get_dinos_names()}")


##TRAVERSE THROUGH TREE WITH USER

def welcome (): #initial set-up of user interface
    print("\nHello! Welcome to the Dinosaur Recommender!\nWe're going to pick out a dinosaur based on a few factors\nWould you like to pick a dino?")
    t_or_f = False
    while t_or_f == False:
        ans = input("Y for yes, N for no: ")
        ans = ans.upper()
        if ans == 'Y':
            dino_tree_setup()
            t_or_f == True
        if ans == "N":
            print("\nI'm sorry you don't want to pick YOUR OWN DINO :(\nHave a nice day!")
            break
        else:
            print("invalid input. Try again!")
    return
            
    
def dino_tree_setup(): #has set of questions and dictionary references that will be used to traverse tree. It also explains to user how this will work
    print("""\nWe'll ask you four questions based on Diet, Time Period, Continent, and the Type of Dinosaur.\nIt should be noted that there many not be a dinosaur based off the answers given.\nIf that is the case, we'll let you know and give you the chance to answer again.
          """)

    diet_question = "\nWhat type of diet does your dinosaur have?\nPick from the following options:"
    period_question = "\nWhich time period did your dinosaur live in?\nPick from the following options:"
    continent_quetion = "\nWhich continent does your dinoasur reside in?\nPick from the following options:"
    type_question = "\nWhat type of dinoasur is your dinosaur?\nPick from the following options:"

    questions_list = [diet_question, period_question , continent_quetion , type_question]
    dict_reference_list = [diet_reference, period_reference, continent_reference, type_reference]

    dino_node = first_dino
    begin = None
    begin = input("Type anything to begin:")
    if begin != None:
        dino_tree_traverse(dino_node, questions_list, dict_reference_list)





def dino_tree_traverse(node, questions_list, dict_reference_list): #where the main work is held
    while len(questions_list) != 0:

        print(questions_list[0])
        for option, num in dict_reference_list[0].items():
            print(f"{num}: {option}")
        ans = input("")
        ans = int(ans)

        if ans in list(dict_reference_list[0].values()):
            new_node = node.get_child_based_on_option(ans)
            if len(new_node.dinos) == 0:
                print("\nSorry, there are no dinosaurs with this set of characteristics. Answer again")
                dino_tree_traverse(node, questions_list, dict_reference_list)
            elif len(new_node.dinos) == 1:
                print(f"This set of characteristics only have one dinosaur. It is the {new_node.dinos[0]}")
                odd_false = False
                while odd_false == False:
                    odd_ans = input("Is this the dinosaur you want? Y or N")
                    odd_ans = odd_ans.upper()
                    if odd_ans == "Y":
                        print(f"Congratulations on picking {new_node.dinos[0]}!! We hope your happy with your dinosaur!")
                        return
                    if odd_ans == "N":
                        print("Fair enough. Pick another answer")
                        dino_tree_traverse(node, questions_list, dict_reference_list)
                        odd_false = True
                    else:
                        print("invalid answer. Try again real quick.")


            else:
                questions_list.pop(0)
                dict_reference_list.pop(0)
                dino_tree_traverse(new_node, questions_list, dict_reference_list)
            
        else:
            print("Incorrect answer. Please try again")
            dino_tree_traverse(node, questions_list, dict_reference_list)
    
    print(f"\nTheses are the characterisitics that your dinosaur has: Type:{node.character_list[0]}, Continent:{node.character_list[1]}, Time Period:{node.character_list[2]}, Diet:{node.character_list[3]}")
    print("These are the dinosaurs you can pick from:")
    num_list = list(range(0,len(node.dinos)))
    dino_ref = dict(zip(num_list, node.dinos))
    for num, dino in dino_ref.items():
        print(f"{num}:{dino}")
    ans = input("\nWhich dino do you want? Select corresponding number:")
    ans = int(ans)

    print(f"Congratulations on picking {dino_ref[ans]}!! We hope your happy with your dinosaur!")

    return
    

##todo - fix up bug at the end
## - fix bug when there's only one dino in the dino section


# welcome()   



