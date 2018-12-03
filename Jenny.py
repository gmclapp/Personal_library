import pandas as pd

def tab_dict(rfile):
    '''This function opens an excel file and returns a dictionary where the
    keys of the dictionary are the sheet names and the values are dataframes
    containing the data from that sheet. rfile must include the path
    if the file is not in the current working directory.'''

    try:
        xlsx = pd.ExcelFile(rfile)
        Sheet_frames = {sh:xlsx.parse(sh) for sh in xlsx.sheet_names}
        # This line creates a dictionary where the keys are the tab names,
        # and the values are the data from that tab.
        return(Sheet_frames)
    
    except FileNotFoundError:
        print(rfile,"Does not exist.")
        return(None)

file_name = "Flowers.xlsx" # Don't forget the .xlsx extension.
file_path = r"C:\Users\Glenn Clapp\Desktop\GVSU\Personal_library"
# Note the 'r' ahead of the path string. This is a string tag that tells python
# what follows is a "raw string" in layman's terms: 'Backslashes are just
# backslashes. Recall that ordinarily they are escape characters.

file = file_path + '\\' + file_name
# The double backslash in this line is an example of the more standard way of
# using backslashes in strings.

plant_dictionary = tab_dict(file)

flower_dataframe = plant_dictionary['Flowerbed']
veg_dataframe = plant_dictionary['Vegetables']
weed_dataframe = plant_dictionary['Weeds']

print(veg_dataframe.head(1)) # prints the first row of the vegetables tab
print(flower_dataframe.tail(1)) # prints the last row of the flower tab
dand_column = weed_dataframe["Dandelions"]

for row in enumerate(dand_column):
    print(row)
