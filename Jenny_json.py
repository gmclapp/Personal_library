import json

Jenny_db = [{"Name":"Hydrangeas",
              "Diseases":[],
              "Pests":[],
              "Water requirement": 3.5,
              "Photos":["hydrangea picture.jpg","yellow variant.png"],
              "Stock": 75},
              {"Name":"Daisies",
              "Diseases":[],
              "Pests":[],
              "Water requirement": 7.5,
              "Photos":["pushing up daisies.jpg"],
              "Stock": 10}]

''' Dictionaries are specified with curly braces {} and with key:value pairs.
keys can be floats or strings, typically strings as in the example above.
values can be any data type (including dictionaries!). The "Name" key refers to
the string "Hydrangeas", "Diseases" and "Pests" are both lists, which can
contain dictionaries that are a data structures for pests and diseases if you
like which might make it possible to easily search by pest or by disease for
example. "Water requirement" is a float, maybe liters per day or something...
"Photos" is the intersting one here, a list of strings which are file names.
This is how I would approach references to photos stored in the same directory
as the script. Finally, "Stock" is an integer.'''

#----- The following is how you will store/retrieve your database --- #

# The following two lines will save a dictionary to a text file
with open("Spring Meadow database.txt", "w") as f:
    json.dump(Jenny_db,f,sort_keys=False,indent=4)


# The following two lines will load a dictionary from a text file
with open("Spring Meadow database.txt", "r") as f:
    Jenny_db = json.load(f)

#--------------------------------------------------------------------#

print("The following plants are in the database:")
for plant in Jenny_db:
    print(plant["Name"])
print("\n",end="") # Add a line break in output

for plant in Jenny_db:
    if plant["Name"] == "Daisies":
        print("{} require {} liters/day of water.".format(plant["Name"],
                                                          plant["Water requirement"]))
    else:
        pass


    
