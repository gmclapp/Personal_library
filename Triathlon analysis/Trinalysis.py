import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
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

def hist_helper(ax,data,col,title=None,xlabel=None,ylabel=None):
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
    
    ax.hist(data[col],bins=binlist,rwidth=0.95)
    if title:
        ax.set_title(title)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    
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
    ##print(DF.head(10))

    cols = ["Swim","T1","CycleLap1","CycleLap2","Cycle","T2","Run","Run1","Run2","Time"]
    for c in cols:
        DF[c] = DF[c].apply(parse_time)

    Elite = {"Name":"Elite",
             "Swim":1200,
             "T1":45,
             "Cycle":2100,
             "T2":45,
             "Run":1410}
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

    fig, axes = plt.subplots(1,3,sharey=True,figsize=(18,10),dpi=100)
    fig2, axes2 = plt.subplots(1,2,sharey=True,figsize=(12,10),dpi=100)
    
    hist_helper(axes[0],DF,"Swim",title="Swim",ylabel="# of Competitors")
    axes[0].axvline(Glenn["Swim"],color='r')
    axes[0].axvline(Matt["Swim"],color='b')
    axes[0].axvline(Elite["Swim"],color='g')

    hist_helper(axes[1],DF,"Cycle",title="Cycle",xlabel="Time(seconds)")
    axes[1].axvline(Glenn["Cycle"],color='r')
    axes[1].axvline(Matt["Cycle"],color='b')
    axes[1].axvline(Elite["Cycle"],color='g')

    
    hist_helper(axes[2],DF,"Run",title="Run")
    axes[2].axvline(Glenn["Run"],color='r')
    axes[2].axvline(Matt["Run"],color='b')
    axes[2].axvline(Elite["Run"],color='g')

    hist_helper(axes2[0],DF,"T1",title="Transition 1",xlabel="Time(seconds)",ylabel="# of Competitors")
    axes2[0].axvline(Glenn["T1"],color='r')
    axes2[0].axvline(Matt["T1"],color='b')
    axes2[0].axvline(Elite["T1"],color='g')

    hist_helper(axes2[1],DF,"T2",title="Transition 2",xlabel="Time(seconds)")
    axes2[1].axvline(Glenn["T2"],color='r')
    axes2[1].axvline(Matt["T2"],color='b')
    axes2[1].axvline(Elite["T2"],color='g')

    Glenn_legend = mlines.Line2D([],[],color='r',markersize=15,label="Glenn")
    Matt_legend = mlines.Line2D([],[],color='b',markersize=15,label="Matt")
    Elite_legend = mlines.Line2D([],[],color='g',markersize=15,label="Elite")
    
    plt.legend(handles=[Glenn_legend,Matt_legend,Elite_legend])

    plt.show()
    
if __name__ == "__main__":
    main()
