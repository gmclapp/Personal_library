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

file_name = "Pre and Post Parametric Review.xlsx" # Don't forget the .xlsx extension.
file_path = r"C:\Users\clappg\Desktop"
# Note the 'r' ahead of the path string. This is a string tag that tells python
# what follows is a "raw string" in layman's terms: 'Backslashes are just
# backslashes. Recall that ordinarily they are escape characters.

file = file_path + '\\' + file_name
# The double backslash in this line is an example of the more standard way of
# using backslashes in strings.

data_dict = tab_dict(file)

PREdf = data_dict['PRE Durability']
POSTdf = data_dict['Post Durability']

PREdf.drop(columns = ['Date',
                      'Time',
                      'TESTER_TEST_ID',
                      'SA_ECU_1',
                      'SA_ECU_26',
                      'WARR_NUM'],inplace=True)

POSTdf.drop(columns = ['Date',
                       'Time',
                       'TESTER_TEST_ID',
                       'SA_ECU_1',
                       'SA_ECU_26',
                       'WARR_NUM'],inplace=True)

PREavg = PREdf.groupby("SAMP_NUM").mean()
POSTavg = POSTdf.groupby("SAMP_NUM").mean()

Specs = {"SA_GS_3":{"USL":8.1,
                    "LSL":6.1},
         "SA_GS_6":{"USL":14.1,
                    "LSL":12.1},
         "SA_GS_9":{"USL":20.1,
                    "LSL":18.1},
         "SA_GS_12":{"USL":6.6,
                    "LSL":4.6},
         "SA_GS_15":{"USL":4.3,
                    "LSL":2.3},
         "SA_GS_17":{"USL":2.9,
                    "LSL":0.9},
         "SA_GS_19":{"USL":4.3,
                    "LSL":2.3},
         "SA_GS_21":{"USL":2.9,
                    "LSL":0.9},
         "SA_GS_23":{"USL":3.9,
                    "LSL":0.9},
         "SA_GS_26":{"USL":17.9,
                    "LSL":15.9},
         "SA_GS_29":{"USL":11.9,
                    "LSL":9.9},
         "SA_GS_32":{"USL":3.6,
                    "LSL":1.6},
         "SA_DET_54":{"USL":22,
                    "LSL":20}}

sn = "SAMP_NUM" # column containing sample numbers

##print(veg_dataframe.head(1)) # prints the first row of the vegetables tab
##print(flower_dataframe.tail(1)) # prints the last row of the flower tab
##dand_column = weed_dataframe["Dandelions"]
##
##for row in enumerate(dand_column):
##    print(row)

