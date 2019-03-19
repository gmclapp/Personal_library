import pandas as pd
import numpy as np
from nptdms import TdmsFile
import os
import matplotlib.pyplot as plt
import csv
import datetime as dt
import time
import misc_functions as mf

__version__ = '0.1.2'
plt.rcParams["figure.figsize"]=(16,8) # default figure size in inches.

def dxdt(df, pos_col, time_col, noise_thres):
    ''' 1st derivative of position data is noisy. Values below noise_thres 
    should be considered zero.'''
    
    df_shifted = df.shift(1)
    change = (df[pos_col]-df_shifted[pos_col])/(df[time_col]-df_shifted[time_col])
    filtered = round(change/noise_thres,0)*noise_thres
    df["Velocity [m/s]"] = filtered
    
def response_time(tdms_file, directory, log):
    # The solenoid distance beyond which it is considered activated
    threshold = 4.5 #mm
    
    # This tab contains the sample number information
    MetaDF = tdms_file.object("Meta Data").as_dataframe()
    MetaDict = MetaDF.set_index("Name").to_dict()
    MetaDict = MetaDict["Value"]

    sample_number = MetaDict["SAMP_NUM"]
    warrant_number = MetaDict['WARR_NUM']
    test_condition = MetaDict['TEST_COND']
    temp = MetaDict['TEST_TEMP']
    volt = MetaDict['TEST_VOLT']

    newrow = [warrant_number,sample_number, temp, volt]
    
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

        first_response_flag = False
        bounce_flag = False
        error_flag = False
        rebound_min = float('Inf')
        rebound_time = 0
        for j,x in enumerate(resp_DFs[i]["Laser [mm]"]):
            if (float(x) > threshold
                and float(resp_DFshifted.at[j, "Laser [mm]"]) <= threshold):
                
                act_time = resp_DFs[i].at[j,"Time Elapsed [ms]"]
                act_times.append(act_time)
                act_flags[i] = True
                if not first_response_flag:
                    first_response_flag = True
                    
                elif first_response_flag:
                    bounce_flag = True

                resp_times.append(act_time - cmd_times[i])
            elif first_response_flag and float(x) < rebound_min:
                rebound_min = float(x)

            if (first_response_flag
                and float(x) < threshold
                and float(resp_DFshifted.at[j, "Laser [mm]"]) >= threshold):
                
                rebound_time = resp_DFs[i].at[j,"Time Elapsed [ms]"] - cmd_times[i]

        if bounce_flag:
            newrow.append(resp_times[-2])
            newrow.append(resp_times[-1])
            relocked_time = resp_times[-1] - rebound_time
            #print("down time: {}, up time: {}, difference: {}".format(rebound_time, resp_times[-1],relocked_time))
        else:
            try:
                newrow.append(resp_times[-1])
            except IndexError:
                error_flag = True
                newrow.append("N/A")
                print("{} No response time!".format(mf.timestamp()),file=log)
                
            newrow.append("N/A")
            relocked_time = 0

        newrow.append(rebound_min)
        newrow.append(relocked_time)
            
    for i,ax in enumerate(axes):
        ax.plot(resp_DFs[i]["Time Elapsed [ms]"],
                resp_DFs[i]["Laser [mm]"],
                resp_DFs[i]["Time Elapsed [ms]"],
                resp_DFs[i]["Velocity [m/s]"])
        
        for t in act_times:
            ax.scatter(t,threshold)

    axes[1].set_xlabel("Time since test start [ms]")
    axes[0].set_ylabel("Displacement [mm]")
        
    plt.subplots_adjust(left=0.10,
                        bottom=0.1,
                        right=0.95,
                        top=0.70,
                        wspace=0.2,
                        hspace=0.4)

    if bounce_flag or error_flag:
        suffix = 1
        filename = str(sample_number)+str(temp)+str(volt)+'.png'
        f_exists = os.path.isfile(filename)
        while f_exists:
            filename=str(warrant_number)+str(sample_number)+str(temp)+str(volt)+'_'+str(suffix)+'.png'
            
            f_exists = os.path.isfile(filename)
            suffix += 1

        pathname = warrant_number+"_ON"
        if os.path.exists(pathname):
            #print("Directory already exists.")
            pass
        else:
            try:
                os.mkdir(pathname)
            except OSError:
                print("{} Directory creation failed.".format(mf.timestamp()),
                      file=log)
            else:
                print("{} Successfully created directory {}".format(mf.timestamp(),
                                                                    pathname),
                      file=log)
        plt.savefig((pathname+"\\"+filename), bbox_inches='tight')
        #plt.show()
    else:
        pass
    
    csvfile = open('response times.csv','a',newline='')
    WRT = csv.writer(csvfile, dialect='excel')        
    WRT.writerow(newrow)
    csvfile.close()
    
def main(directory=None):
    log = open("log.txt", mode='a')
    # Define the directory in which the test data are found
    if directory == None:
        directory = input("Enter directory\n>>>")
    print(mf.timestamp(),directory,file=log)
    tdms_files = []
    csvfile = open('response times.csv','a',newline='')
    WRT = csv.writer(csvfile, dialect='excel')
    WRT.writerow(["Warrant","Sample number","Temperature (C)","Voltage (V)",
                  "Response 1A [ms]","Response 1B [ms]","Rebound distance 1 [mm]","Re-locked time [ms]",
                  "Response 2A [ms]","Response 2B [ms]","Rebound distance 2 [mm]","Re-locked time [ms]",
                  "Response 3A [ms]","Response 3B [ms]","Rebound distance 3 [mm]","Re-locked time [ms]",])
    csvfile.close()

    for file in os.listdir(directory):
        if file.endswith(".tdms"):
            tdms_files.append(os.path.join(directory,file))

    for f in tdms_files:
        tdms_file = TdmsFile(f)
        try:
            response_time(tdms_file, directory, log)
        except KeyError:
            print("{} Faulty tdms file {}.".format(mf.timestamp(),
                                                   str(f)),
                  file=log)
            continue
        except Exception as ex:
            raise

    print("{} Finished processing {}".format(mf.timestamp(),
                                             directory),
          file=log)
    log.close()

if __name__ == '__main__':
    main()


