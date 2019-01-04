import pandas as pd
import numpy as np
from nptdms import TdmsFile
import os
import matplotlib.pyplot as plt

__version__ = '0.1.0'
plt.rcParams["figure.figsize"]=(16,8) # default figure size in inches.

def dxdt(df, pos_col, time_col, noise_thres):
    ''' 1st derivative of position data is noisy. Values below noise_thres 
    should be considered zero.'''
    
    df_shifted = df.shift(1)
    change = (df[pos_col]-df_shifted[pos_col])/(df[time_col]-df_shifted[time_col])
    filtered = round(change/noise_thres,0)*noise_thres
    df["Velocity [m/s]"] = filtered
    
def response_time(tdms_file):
    # The solenoid distance beyond which it is considered activated
    threshold = 4.3 #mm
    
    # This tab contains the sample number information
    MetaDF = tdms_file.object("Meta Data").as_dataframe()
    MetaDict = MetaDF.set_index("Name").to_dict()
    MetaDict = MetaDict["Value"]

    sample_number = MetaDict["SAMP_NUM"]
    warrant_number = MetaDict['WARR_NUM']
    test_condition = MetaDict['TEST_COND']
    temp = MetaDict['TEST_TEMP']
    volt = MetaDict['TEST_VOLT']

    # This tab contains the solenoid actuation times
    SolDF = tdms_file.object("Results").as_dataframe()
    SolDict = SolDF.set_index("Name").to_dict()
    SolDict = SolDict["Value"]

    # This tab contains the time/distance data for the solenoid
    LaserDF = tdms_file.object("Laser Data").as_dataframe()
    dxdt(LaserDF,"Laser [mm]","Time Elapsed [ms]",0.085)

    cmd_times = []
    resp_DFs = []
    axes = []
    
    act_flags = [False,False,False]
    act_times = []
    resp_times = []
    
    start_pad = 100
    end_pad = 500
    plt.close('all')

    row_labels = ["Warrant Number",
                  "Sample Number",
                  "Test Condition",
                  "Temperature",
                  "Voltage"]
    
    for i in range(1,4):
        SolDictstr = "T0_SOL_ON_" + str(i)
        cmd_times.append(float(SolDict[SolDictstr]))

        axes.append(plt.subplot2grid((1,3),(0,i-1),rowspan=1,colspan=1))

    for i in range(3):
        start = int(cmd_times[i])-start_pad
        end = int(cmd_times[i])+end_pad
        resp_DFs.append(LaserDF[start:end])

        axes[i].set_xlim(left=start,right=end)
        title_str = ("Warrant: {}\nSample: {}\nTest Condition: {}\nTemperature: {}\nVoltage: {}\nResponse: {}\n"\
                     .format(warrant_number,sample_number,test_condition,temp,volt,i+1))
        
        axes[i].set_title(title_str,loc='left',horizontalalignment='left')
        axes[i].hlines(threshold, start, end, linestyles='dashed')
        axes[i].vlines(cmd_times[i], 0, 10, colors='r', linestyles='dashed')

        resp_DFs[i] = resp_DFs[i].reset_index()
        resp_DFshifted = resp_DFs[i].shift(1)
        
        for j,x in enumerate(resp_DFs[i]["Laser [mm]"]):
            #if (float(x) > threshold
            if (float(x) > threshold and float(resp_DFshifted.at[j, "Laser [mm]"]) <= threshold):
                #and not act_flags[i]
                #and cmd_times[i] > j):

                act_times.append(resp_DFs[i].at[j,"Time Elapsed [ms]"])
                act_flags[i] = True

        resp_times.append(j - cmd_times[i])

    for i,ax in enumerate(axes):
        ax.plot(resp_DFs[i]["Time Elapsed [ms]"],
                resp_DFs[i]["Laser [mm]"],
                resp_DFs[i]["Time Elapsed [ms]"],
                resp_DFs[i]["Velocity [m/s]"])
        
        for t in act_times:
            print("act_time: ",t)
            ax.scatter(t,threshold)

    axes[1].set_xlabel("Time since test start [ms]")
    axes[0].set_ylabel("Displacement [mm]")
        

    plt.subplots_adjust(left=0.10,
                        bottom=0.1,
                        right=0.95,
                        top=0.70,
                        wspace=0.2,
                        hspace=0.4)
    
    plt.show()

# Define the directory in which the data are stored
directory = input("Enter directory\n>>>")
#directory = r"\\jsjcorp.com\data\GHSP\GH\webdata\Testing\2018\20184410\Parametric Data"

tdms_files = []
for file in os.listdir(directory):
    if file.endswith(".tdms"):
        #print(file)
        tdms_files.append(os.path.join(directory,file))

try:
    for f in tdms_files:
        tdms_file = TdmsFile(f)
        response_time(tdms_file)
except Exception as ex:
    #print(ex)
    raise


