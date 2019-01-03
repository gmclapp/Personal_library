import pandas as pd
import numpy as np
from nptdms import TdmsFile
import os
import matplotlib.pyplot as plt

def dxdt(df, pos_col, time_col, noise_thres):
    ''' 1st derivative of position data is noisy. Values below noise_thres 
    should be considered zero.'''
    
    df_shifted = df.shift(1)
    change = (df[pos_col]-df_shifted[pos_col])/(df[time_col]-df_shifted[time_col])
    filtered = round(change/noise_thres,0)*noise_thres
    df["Velocity [m/s]"] = filtered
    
def response_time(tdms_file):
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
    
    # These lines retrieve the solenoid activation command times
    cmd_time_1 = float(SolDict["T0_SOL_ON_1"])
    cmd_time_2 = float(SolDict["T0_SOL_ON_2"])
    cmd_time_3 = float(SolDict["T0_SOL_ON_3"])
    
    # This tab contains the time/distance data for the solenoid
    LaserDF = tdms_file.object("Laser Data").as_dataframe()
    dxdt(LaserDF,"Laser [mm]","Time Elapsed [ms]",0.085)

    # Solenoid command times are used to break the laser data into sub frames
    # one for each response.
    firstDF = LaserDF[int(cmd_time_1):int(cmd_time_2)]
    secondDF = LaserDF[int(cmd_time_2):int(cmd_time_3)]
    thirdDF = LaserDF[int(cmd_time_3):]


    print(firstDF.head())
    print(secondDF.head())
    print(thirdDF.head())
    
    print(firstDF.tail())
    print(secondDF.tail())
    print(thirdDF.tail())
    
    #print(LaserDF.head())
    LaserDF.plot(kind='line',x="Time Elapsed [ms]",y=["Laser [mm]","Velocity [m/s]"])
    plt.show()

    act_1_flag = False
    act_2_flag = False
    act_3_flag = False
    for i,x in enumerate(LaserDF["Laser [mm]"]):
        if (float(x) > threshold
            and not act_1_flag
            and cmd_time_2 > i > cmd_time_1):
            
            act_time_1 = i
            act_1_flag = True

        elif (float(x) > threshold
              and not act_2_flag
              and cmd_time_3 > i > cmd_time_2):

            act_time_2 = i
            act_2_flag = True

        elif (float(x) > threshold
              and not act_3_flag
              and i > cmd_time_3):

            act_time_3 = i
            act_3_flag = True

    resp_time_1 = act_time_1 - cmd_time_1
    resp_time_2 = act_time_2 - cmd_time_2
    resp_time_3 = act_time_3 - cmd_time_3

    print("\nSample number:",sample_number)
    print("Test Condition:",test_condition)
    print("Temperature: {} Voltage:{}".format(temp, volt))
    print("Response time 1: {} ms\nResponse time 2: {} ms\nResponse time 3: {} ms"\
          .format(resp_time_1,resp_time_2,resp_time_3))

# Define the directory in which the data are stored
directory = input("Enter directory\n>>>")
#directory = r"\\jsjcorp.com\data\GHSP\GH\webdata\Testing\2018\20184410\Parametric Data"

# The solenoid distance beyond which it is considered activated
threshold = 4.3 #mm

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
    print(ex)

print("Exit?")
while(True):
    pass

