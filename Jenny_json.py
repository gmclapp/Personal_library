import json

Jenny_dict = {"Name":"Hydrangeas",
              "Diseases":[],
              "Pests":[],
              "Water requirement": 3.5,
              "Photos":["hydrangea picture.jpg","yellow variant.png"],
              "Stock": 75}

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

with open("Spring Meadow database.txt", "w") as f:
    pass
