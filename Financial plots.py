import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import misc_functions as mf

DF = pd.read_excel("Fidelity.xlsx")
DFA = DF.iloc[:14,:]
mA,bA,rsqA = mf.lin_reg(DFA["n"],DFA["Portfolio value"])
txtA = "y = {:4.2f}x + {:4.2f}, rsq = {:4.4f}".format(mA,bA,rsqA)

yA = []
for i in DFA["n"]:
    yA.append(mA*i + bA)

DFB = DF.iloc[20:33,:]
DFB.reset_index(inplace=True)
mB,bB,rsqB = mf.lin_reg(DFB["n"],DFB["Portfolio value"])
bB += DFB["n"][0]
txtB = "y = {:4.2f}x + {:4.2f}, rsq = {:4.4f}".format(mB,bB,rsqB)

yB = []
for i in DFB["n"]:
    yB.append(mB*i + bB)

DFC = DF.iloc[35:51,:]
DFC.reset_index(inplace=True)
mC,bC,rsqC = mf.lin_reg(DFC["n"],DFC["Portfolio value"])
bC += DFC["n"][0]
txtC = "y = {:4.2f}x + {:4.2f}, rsq = {:4.4f}".format(mC,bC,rsqC)

yC = []
for i in DFC["n"]:
    yC.append(mC*i+bC)

m = (mA+mB+mC)/3 # find the average slope of the three models
m_sd = np.array([mA,mB,mC]).std()
print("~N({:4.2f},{:4.4f})".format(m,m_sd))

## ------ Plotting section -------- ##
fig,ax = plt.subplots(1,1,figsize=(10,6))
ax.scatter(DFA["n"],DFA["Portfolio value"],color='b')
ax.plot(DFA["n"],yA,color='k')
ax.text(DFA["n"][0]+3,DFA["Portfolio value"][0],txtA)

ax.scatter(DFB["n"],DFB["Portfolio value"],color='b')
ax.plot(DFB["n"],yB,color='k')
ax.text(DFB["n"][0]-10,DFB["Portfolio value"][0]-4500,txtB)

ax.scatter(DFC["n"],DFC["Portfolio value"],color='b')
ax.plot(DFC["n"],yC,color='k')
ax.text(DFC["n"][0]-3,DFC["Portfolio value"][0]-4500,txtC)

plt.show()
