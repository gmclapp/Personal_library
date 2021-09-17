import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.ticker import (FixedLocator,MultipleLocator, AutoMinorLocator,FormatStrFormatter)

import datetime as dt

def parse_time(timestring):
    '''takes a string in format HH:MM:SS and returns an integer representing
    the equivalent total seconds.'''
    try:
        t = dt.datetime.strptime(timestring,"%H:%M:%S")
        return(t.second + t.minute*60 + t.hour*3600)
    except TypeError:
        # catches NaN
        return(0)
    except ValueError:
        # Catches "DNF"
        return(0)

def hist_helper(ax,data,col,title=None,xlabel=None,ylabel=None,color='b'):
    '''takes a matplotlib axis, data, and labels and plots the data on the axis after
    some cleanup operations'''
    data = data.loc[(data[[col]] != 0).all(axis=1)]
    minimum = data[col].min()

    IQR = data[col].quantile(0.75) - data[col].quantile(0.25)
    median = data[col].quantile(0.5)

    maximum = median + 3*IQR+median
    step = (maximum-minimum)/10
    binlist = []
    for i in range(10):
        binlist.append(minimum+step*i)
    binlist.append(maximum)
    
    data = data.loc[(data[[col]] <= maximum).all(axis=1)]
    
    ax.hist(data[col],bins=binlist,rwidth=0.95,color=color)
##    ax.xaxis.set_major_locator(MultipleLocator(step))
    ax.xaxis.set_major_locator(FixedLocator(binlist))
    ax.set_xticklabels(ax.get_xticks(),rotation = 45)
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    
    if title:
        ax.set_title(title)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)

def individual_helper(ax,data,color,text_x_offset=0,text_y_offset=0,text_rot=0):
    ax.axvline(data,color=color)
    minutes = int(data/60)
    seconds = int(data - minutes*60)
    txt = "{:02d}:{:02d}".format(minutes,seconds)
    ax.text(data+text_x_offset,1+text_y_offset,txt,color=color,rotation=text_rot)

def characterizeElite(DF):
    is_elite = DF['Time']<=4800
    EliteDF = DF[is_elite]

    has_run = EliteDF["Run"]!=0
    EliteDF = EliteDF[has_run]

    has_cycle = EliteDF["Cycle"]!=0
    EliteDF = EliteDF[has_cycle]

    has_swim = EliteDF["Swim"]!=0
    EliteDF = EliteDF[has_swim]

    EliteDF = EliteDF[EliteDF.Name != "TEAM LEGION OF ZOOM"]

    Elite = {"Name":"Elite",
             "Swim":EliteDF["Swim"].mean(),
             "T1":EliteDF["T1"].mean(),
             "Cycle":EliteDF["Cycle"].mean(),
             "T2":EliteDF["T2"].mean(),
             "Run":EliteDF["Run"].mean()}
    
    EliteMin = {"Name":"EliteMin",
             "Swim":EliteDF["Swim"].min(),
             "T1":EliteDF["T1"].min(),
             "Cycle":EliteDF["Cycle"].min(),
             "T2":EliteDF["T2"].min(),
             "Run":EliteDF["Run"].min()}

    EliteMax = {"Name":"EliteMax",
             "Swim":EliteDF["Swim"].max(),
             "T1":EliteDF["T1"].max(),
             "Cycle":EliteDF["Cycle"].max(),
             "T2":EliteDF["T2"].max(),
             "Run":EliteDF["Run"].max()}
    
    return(EliteMin,EliteMax,Elite)

def transitionPlot(DF,Glenn,Matt,Elite):
    fig2, axes2 = plt.subplots(1,2,sharey=True,figsize=(12,10),dpi=100)
    hist_helper(axes2[0],DF,"T1",title="Transition 1",xlabel="Time(seconds)",ylabel="# of Competitors",color=(0.9,0.9,0.9,0.75))
    axes2[0].axvline(Glenn["T1"],color='r')
    axes2[0].axvline(Matt["T1"],color='b')
    axes2[0].axvline(Elite["T1"],color='g')
    individual_helper(axes2[0],Glenn["T1"],
                      'r',
                      text_x_offset=5,
                      text_y_offset=140,
                      text_rot=90)
    
    individual_helper(axes2[0],Matt["T1"],
                      'b',
                      text_x_offset=5,
                      text_y_offset=130,
                      text_rot=90)
    
    individual_helper(axes2[0],Elite["T1"],
                      'g',
                      text_x_offset=5,
                      text_y_offset=120,
                      text_rot=90)
    

    hist_helper(axes2[1],DF,"T2",title="Transition 2",xlabel="Time(seconds)",color=(0.9,0.9,0.9,0.75))
    individual_helper(axes2[1],Glenn["T2"],
                      'r',
                      text_x_offset=5,
                      text_y_offset=140,
                      text_rot=90)
    
    individual_helper(axes2[1],Matt["T2"],
                      'b',
                      text_x_offset=5,
                      text_y_offset=130,
                      text_rot=90)
    
    individual_helper(axes2[1],Elite["T2"],
                      'g',
                      text_x_offset=5,
                      text_y_offset=120,
                      text_rot=90)
    
def comboPlot(DF,Glenn,Matt,Elite):
    fig, axes = plt.subplots(1,3,sharey=True,figsize=(18,10),dpi=100)
    hist_helper(axes[0],DF,"Swim",title="Swim",ylabel="# of Competitors",color=(0.9,0.9,0.9,0.75))
    individual_helper(axes[0],Glenn["Swim"],
                      'r',
                      text_x_offset=5,
                      text_y_offset=200,
                      text_rot=90)
    
    individual_helper(axes[0],Matt["Swim"],
                      'b',
                      text_x_offset=5,
                      text_y_offset=200,
                      text_rot=90)
    
    individual_helper(axes[0],Elite["Swim"],
                      'g',
                      text_x_offset=5,
                      text_y_offset=200,
                      text_rot=90)

    hist_helper(axes[1],DF,"Cycle",title="Cycle",xlabel="Time(seconds)",color=(0.9,0.9,0.9,0.75))
    individual_helper(axes[1],Glenn["Cycle"],
                      'r',
                      text_x_offset=5,
                      text_y_offset=220,
                      text_rot=90)
    
    individual_helper(axes[1],Matt["Cycle"],
                      'b',
                      text_x_offset=5,
                      text_y_offset=200,
                      text_rot=90)
    
    individual_helper(axes[1],Elite["Cycle"],
                      'g',
                      text_x_offset=5,
                      text_y_offset=180,
                      text_rot=90)

    
    hist_helper(axes[2],DF,"Run",title="Run",color=(0.9,0.9,0.9,0.75))
    individual_helper(axes[2],Glenn["Run"],
                      'r',
                      text_x_offset=5,
                      text_y_offset=200,
                      text_rot=90)
    
    individual_helper(axes[2],Matt["Run"],
                      'b',
                      text_x_offset=5,
                      text_y_offset=200,
                      text_rot=90)
    
    individual_helper(axes[2],Elite["Run"],
                      'g',
                      text_x_offset=5,
                      text_y_offset=180,
                      text_rot=90)
    
def bigSwim(DF,Glenn,Matt,Elite,EliteMin,EliteMax):
    bigfig, ax = plt.subplots(1,1,figsize=(10,10),dpi=100)
    hist_helper(ax,DF,"Swim",title="Swim",xlabel="Time(seconds)",ylabel="# of Competitors",color=(0.9,0.9,0.9,0.75))
    individual_helper(ax,Glenn["Swim"],
                      'r',
                      text_x_offset=5,
                      text_y_offset=160,
                      text_rot=90)
    
    individual_helper(ax,Matt["Swim"],
                      'b',
                      text_x_offset=5,
                      text_y_offset=160,
                      text_rot=90)
    
    individual_helper(ax,Elite["Swim"],
                      'g',
                      text_x_offset=5,
                      text_y_offset=50,
                      text_rot=90)
    individual_helper(ax,EliteMin["Swim"],
                      'g',
                      text_x_offset=5,
                      text_y_offset=50,
                      text_rot=90)
    individual_helper(ax,EliteMax["Swim"],
                      'g',
                      text_x_offset=5,
                      text_y_offset=50,
                      text_rot=90)
    Glenn_legend = mlines.Line2D([],[],color='r',markersize=15,label="Glenn")
    Matt_legend = mlines.Line2D([],[],color='b',markersize=15,label="Matt")
    Elite_legend = mlines.Line2D([],[],color='g',markersize=15,label="Elite")
    
    ax.legend(handles=[Glenn_legend,Matt_legend,Elite_legend])
    
def bigCycle(DF,Glenn,Matt,Elite,EliteMin,EliteMax):
    bigfig, ax = plt.subplots(1,1,figsize=(10,10),dpi=100)
    hist_helper(ax,DF,"Cycle",title="Cycle",xlabel="Time(seconds)",ylabel="# of Competitors",color=(0.9,0.9,0.9,0.75))
    individual_helper(ax,Glenn["Cycle"],
                      'r',
                      text_x_offset=5,
                      text_y_offset=160,
                      text_rot=90)
    
    individual_helper(ax,Matt["Cycle"],
                      'b',
                      text_x_offset=5,
                      text_y_offset=160,
                      text_rot=90)
    
    individual_helper(ax,Elite["Cycle"],
                      'g',
                      text_x_offset=-150,
                      text_y_offset=50,
                      text_rot=90)
    individual_helper(ax,EliteMin["Cycle"],
                      'g',
                      text_x_offset=-150,
                      text_y_offset=50,
                      text_rot=90)
    individual_helper(ax,EliteMax["Cycle"],
                      'g',
                      text_x_offset=-150,
                      text_y_offset=50,
                      text_rot=90)
    Glenn_legend = mlines.Line2D([],[],color='r',markersize=15,label="Glenn")
    Matt_legend = mlines.Line2D([],[],color='b',markersize=15,label="Matt")
    Elite_legend = mlines.Line2D([],[],color='g',markersize=15,label="Elite")
    
    ax.legend(handles=[Glenn_legend,Matt_legend,Elite_legend])
    
def bigRun(DF,Glenn,Matt,Elite,EliteMin,EliteMax):
    bigfig, ax = plt.subplots(1,1,figsize=(10,10),dpi=100)
    hist_helper(ax,DF,"Run",title="Run",xlabel="Time(seconds)",ylabel="# of Competitors",color=(0.9,0.9,0.9,0.75))
    individual_helper(ax,Glenn["Run"],
                      'r',
                      text_x_offset=5,
                      text_y_offset=160,
                      text_rot=90)
    
    individual_helper(ax,Matt["Run"],
                      'b',
                      text_x_offset=5,
                      text_y_offset=160,
                      text_rot=90)
    
    individual_helper(ax,Elite["Run"],
                      'g',
                      text_x_offset=-120,
                      text_y_offset=50,
                      text_rot=90)
    individual_helper(ax,EliteMin["Run"],
                      'g',
                      text_x_offset=-120,
                      text_y_offset=50,
                      text_rot=90)
    individual_helper(ax,EliteMax["Run"],
                      'g',
                      text_x_offset=-120,
                      text_y_offset=50,
                      text_rot=90)

    Glenn_legend = mlines.Line2D([],[],color='r',markersize=15,label="Glenn")
    Matt_legend = mlines.Line2D([],[],color='b',markersize=15,label="Matt")
    Elite_legend = mlines.Line2D([],[],color='g',markersize=15,label="Elite")
    
    ax.legend(handles=[Glenn_legend,Matt_legend,Elite_legend])
    
def main():
    pd.set_option('display.max_columns',None)
    pd.set_option('display.max_rows',None)

    with open("Triathlon Data.csv") as f:
        TriDF = pd.read_csv(f)

    with open("Duathlon data.csv") as f:
        DuaDF = pd.read_csv(f)

    with open("Aquabike data.csv") as f:
        AquaDF = pd.read_csv(f)

    ##DuaDF = DuaDF.rename(columns={"Run2":"Run"})

    DFs = [TriDF,DuaDF,AquaDF]
    DF = pd.concat(DFs,ignore_index=True,sort=False)
    EliteDF = pd.concat([TriDF,DuaDF],ignore_index=True,sort=False)
    ##print(DF.head(10))

    cols = ["Swim","T1","CycleLap1","CycleLap2","Cycle","T2","Run","Run1","Run2","Time"]
    for c in cols:
        DF[c] = DF[c].apply(parse_time)    
        EliteDF[c] = EliteDF[c].apply(parse_time)
    
    EliteMin,EliteMax,Elite = characterizeElite(EliteDF)
    
    for i, row in DF.iterrows():
        if row["Name"].lower() == "glenn clapp":
            Glenn = {"Name":row["Name"],
                     "Swim":row["Swim"],
                     "T1":row["T1"],
                     "Cycle":row["Cycle"],
                     "T2":row["T2"],
                     "Run":row["Run"]}
            
        elif row["Name"].lower() == "matthew clapp":
            Matt = {"Name":row["Name"],
                     "Swim":row["Swim"],
                     "T1":row["T1"],
                     "Cycle":row["Cycle"],
                     "T2":row["T2"],
                     "Run":row["Run"]}
    
    bigSwim(DF,Glenn,Matt,Elite,EliteMin,EliteMax)
    bigCycle(DF,Glenn,Matt,Elite,EliteMin,EliteMax)
    bigRun(DF,Glenn,Matt,Elite,EliteMin,EliteMax)
    comboPlot(DF,Glenn,Matt,Elite)
    transitionPlot(DF,Glenn,Matt,Elite)

    Glenn_legend = mlines.Line2D([],[],color='r',markersize=15,label="Glenn")
    Matt_legend = mlines.Line2D([],[],color='b',markersize=15,label="Matt")
    Elite_legend = mlines.Line2D([],[],color='g',markersize=15,label="Elite")
    
    plt.legend(handles=[Glenn_legend,Matt_legend,Elite_legend])

    plt.show()
    
if __name__ == "__main__":
    main()
