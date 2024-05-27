import pandas as pd
import numpy as np
from dino_tree import DinoTree

df = pd.read_csv(r"/Users/mariochima/Desktop/my first folder/coding folder/recommendation project/jurassic_park_data.csv")

#filling in any empty spaces in data
df['lived_in'].fillna('Other', inplace = True)

#check if string has 'insert period' as part of the string

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

# unique_counts = {}
# for column in df.columns:
#     unique_counts[column] = df[column].value_counts()

# for col, counts in unique_counts.items():
#     print(f"Counts for column {col}:\n{counts}\n")


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

# print(dict_of_diet)

#creating idx reference for different values

numbers = list(range(0,len(dict_of_diet)))

diet_reference = dict(zip(dict_of_diet.keys(), numbers))




#creating Dino tree structure

first_dino = DinoTree(None, 1)
for diet, names in dict_of_diet.items():
    first_dino.add_nodes(diet,diet_reference[diet],1)

for node in first_dino.connecting_nodes.values(): #this line is going thorugh every child node
    for name in dict_of_diet[node.characteristics]: #this line uses the characteristic of node to filter out dictionary
        node.add_dino(name)
        

for node in first_dino.connecting_nodes.values():
    print(node.dinos)

print(first_dino.connecting_nodes)
print(diet_reference)









    



