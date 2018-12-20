import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
# Note that taking the mean by sample number drops columns with text data
# We still need test condition data before stacking the data
PREavg["Test Condition"] = "PRE"
POSTavg["Test Condition"] = "POST"

stacked_data = pd.concat([PREavg,POSTavg])
stacked_data.to_csv("stacked_data.csv")

# For the actual tests we'll do the following
diffDF = pd.DataFrame()
for col in PREavg:
    try:
        diffDF[col] = PREavg[col].sub(POSTavg[col])
    except:
        continue

# For paired data, if a sample was not measured both PRE and POST that row
# will contain 'NA' instead of data. Let's remove those rows.

diffDF = diffDF.dropna()

# create the histograms
#histograms = diffDF.hist()



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


ax1 = plt.subplot2grid((4,4),(0,0), rowspan=1,colspan=1)
ax2 = plt.subplot2grid((4,4),(0,1), rowspan=1,colspan=1)
ax3 = plt.subplot2grid((4,4),(0,2), rowspan=1,colspan=1)
ax4 = plt.subplot2grid((4,4),(0,3), rowspan=1,colspan=1)
ax5 = plt.subplot2grid((4,4),(1,0), rowspan=1,colspan=1)
ax6 = plt.subplot2grid((4,4),(1,1), rowspan=1,colspan=1)
ax7 = plt.subplot2grid((4,4),(1,2), rowspan=1,colspan=1)
ax8 = plt.subplot2grid((4,4),(1,3), rowspan=1,colspan=1)

ax9 = plt.subplot2grid((4,4),(2,0), rowspan=1,colspan=1)
ax10 = plt.subplot2grid((4,4),(2,1), rowspan=1,colspan=1)
ax11 = plt.subplot2grid((4,4),(2,2), rowspan=1,colspan=1)
ax12 = plt.subplot2grid((4,4),(2,3), rowspan=1,colspan=1)
ax13 = plt.subplot2grid((4,4),(3,0), rowspan=1,colspan=1)
ax14 = plt.subplot2grid((4,4),(3,1), rowspan=1,colspan=1)
ax15 = plt.subplot2grid((4,4),(3,2), rowspan=1,colspan=1)
ax16 = plt.subplot2grid((4,4),(3,3), rowspan=1,colspan=1)

ax1.hist(x=PREavg["SA_GS_3"], bins='auto',alpha=0.5)
ax1.hist(x=POSTavg["SA_GS_3"], bins='auto',alpha=0.5)
ax1.axvline(Specs["SA_GS_3"]["USL"],color='r')
ax1.axvline(Specs["SA_GS_3"]["LSL"],color='r')

ax2.hist(x=PREavg["SA_GS_6"], bins='auto',alpha=0.5)
ax2.hist(x=POSTavg["SA_GS_6"], bins='auto',alpha=0.5)
ax2.axvline(Specs["SA_GS_6"]["USL"],color='r')
ax2.axvline(Specs["SA_GS_6"]["LSL"],color='r')

ax3.hist(x=PREavg["SA_GS_9"], bins='auto',alpha=0.5)
ax3.hist(x=POSTavg["SA_GS_9"], bins='auto',alpha=0.5)
ax3.axvline(Specs["SA_GS_9"]["USL"],color='r')
ax3.axvline(Specs["SA_GS_9"]["LSL"],color='r')

#ax4.hist(x=PREavg["SA_GS_12"], bins='auto',alpha=0.5)
ax4.hist(x=POSTavg["SA_GS_12"], bins='auto',alpha=0.5)
ax4.axvline(Specs["SA_GS_12"]["USL"],color='r')
ax4.axvline(Specs["SA_GS_12"]["LSL"],color='r')

ax5.hist(x=PREavg["SA_GS_15"], bins='auto',alpha=0.5)
ax5.hist(x=POSTavg["SA_GS_15"], bins='auto',alpha=0.5)
ax5.axvline(Specs["SA_GS_15"]["USL"],color='r')
ax5.axvline(Specs["SA_GS_15"]["LSL"],color='r')

ax6.hist(x=PREavg["SA_GS_17"], bins='auto',alpha=0.5)
ax6.hist(x=POSTavg["SA_GS_17"], bins='auto',alpha=0.5)
ax6.axvline(Specs["SA_GS_17"]["USL"],color='r')
ax6.axvline(Specs["SA_GS_17"]["LSL"],color='r')

ax7.hist(x=PREavg["SA_GS_19"], bins='auto',alpha=0.5)
ax7.hist(x=POSTavg["SA_GS_19"], bins='auto',alpha=0.5)
ax7.axvline(Specs["SA_GS_19"]["USL"],color='r')
ax7.axvline(Specs["SA_GS_19"]["LSL"],color='r')

ax8.hist(x=PREavg["SA_GS_21"], bins='auto',alpha=0.5)
ax8.hist(x=POSTavg["SA_GS_21"], bins='auto',alpha=0.5)
ax8.axvline(Specs["SA_GS_21"]["USL"],color='r')
ax8.axvline(Specs["SA_GS_21"]["LSL"],color='r')

#ax9.hist(x=PREavg["SA_GS_23"], bins='auto',alpha=0.5)
ax9.hist(x=POSTavg["SA_GS_23"], bins='auto',alpha=0.5)
ax9.axvline(Specs["SA_GS_23"]["USL"],color='r')
ax9.axvline(Specs["SA_GS_23"]["LSL"],color='r')

ax10.hist(x=PREavg["SA_GS_26"], bins='auto',alpha=0.5)
ax10.hist(x=POSTavg["SA_GS_26"], bins='auto',alpha=0.5)
ax10.axvline(Specs["SA_GS_26"]["USL"],color='r')
ax10.axvline(Specs["SA_GS_26"]["LSL"],color='r')

ax11.hist(x=PREavg["SA_GS_29"], bins='auto',alpha=0.5)
ax11.hist(x=POSTavg["SA_GS_29"], bins='auto',alpha=0.5)
ax11.axvline(Specs["SA_GS_29"]["USL"],color='r')
ax11.axvline(Specs["SA_GS_29"]["LSL"],color='r')

ax12.hist(x=PREavg["SA_GS_32"], bins='auto',alpha=0.5)
ax12.hist(x=POSTavg["SA_GS_32"], bins='auto',alpha=0.5)
ax12.axvline(Specs["SA_GS_32"]["USL"],color='r')
ax12.axvline(Specs["SA_GS_32"]["LSL"],color='r')

ax13.hist(x=PREavg["SA_DET_54"], bins='auto',alpha=0.5)
ax13.hist(x=POSTavg["SA_DET_54"], bins='auto',alpha=0.5)
ax13.axvline(Specs["SA_DET_54"]["USL"],color='r')
ax13.axvline(Specs["SA_DET_54"]["LSL"],color='r')


sn = "SAMP_NUM" # column containing sample numbers

# Show the plots
plt.show()


