import matplotlib.pyplot as plt
import pandas as pd

DF = pd.read_excel("Fidelity.xlsx")
DFA = DF.iloc[:14,:]

DFB = DF.iloc[20:33,:]
DFB.reset_index(inplace=True)

DFC = DF.iloc[35:51,:]
DFC.reset_index(inplace=True)

fig,ax = plt.subplots(1,1,figsize=(10,6))
ax.plot(DFA["n"],DFA["Portfolio value"])
ax.plot(DFB["n"],DFB["Portfolio value"])
ax.plot(DFC["n"],DFC["Portfolio value"])

plt.show()
