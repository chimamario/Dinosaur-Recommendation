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

diet_reference = dict(zip(dict_of_diet.keys(), diet_numbers)) #we either have to do this manually or find a way to make this auto
period_reference = dict(zip(dict_of_period.keys(), period_numbers))
continent_reference = dict(zip(dict_of_continent.keys(), continent_numbers))


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
                print(f" list is for {node.characteristics} with {node.parent_dino.characteristics} parent node. these are the dino names {node.get_dinos_names()}")
    
## FOURTH TREE LEVEL








node_2 = diet_node_list[0]
node_2_list = node_2.get_dino_nodes()


# print(first_dino.connecting_nodes)
# print(diet_reference)
print(diet_node_list)
print(node_2_list)









    



