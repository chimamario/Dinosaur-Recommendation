import pandas as pd
import numpy as np

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



unique_counts = {}
for column in df.columns:
    unique_counts[column] = df[column].value_counts()

for col, counts in unique_counts.items():
    print(f"Counts for column {col}:\n{counts}\n")


