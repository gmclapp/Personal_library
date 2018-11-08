import random
import pandas as pd
import matplotlib.pyplot as plt

random.seed(6168850734)
n = 50

true_meas = []
true_mean = 8.5
true_variability = 1.3

measurements = []

Operator_1 = {"Name":"Andy","Offset":2.4,"Variability":0.05}
Operator_2 = {"Name":"Susan","Offset":-0.3,"Variability":0.12}
Operator_3 = {"Name":"Brian","Offset":1.25,"Variability":0.23}

operators = [Operator_1,Operator_2,Operator_3]

machine = {"Offset":-0.25,"Variability":0.45}

no_repetitions = 10

# Create data that represents the actual state of hypothetical parts
for i in range(n):
    true_meas.append([i+1,
                      random.normalvariate(true_mean,true_variability**0.5)])

data = [["Part","Operator","Run","Observation"]]
# Run the MSA procedure (crossed ANOVA with interaction)
for m in true_meas:
    for op in operators:
        for k in range(no_repetitions):
            op_err = random.normalvariate(op["Offset"],op["Variability"]**0.5)
            mach_err = random.normalvariate(machine["Offset"],machine["Variability"]**0.5)
            data.append([m[0],op["Name"],k+1,m[1]+op_err+mach_err])
            
##for d in data:
##    print(d)
headers = data.pop(0)
df = pd.DataFrame(data,columns=headers)
#print(df)

'''Now run the Gage R&R'''
xbar_grand = df["Observation"].mean()

ops = dict((x,y) for x,y in df.groupby("Operator"))
# The line above splits the data into dictionaries where the key is the name of
# each unique operator found, and the value is a panda dataframe containing
# observations made by that operator.

reps = dict((x,y) for x,y in df.groupby("Run"))
parts = dict((x,y) for x,y in df.groupby("Part"))
# Similarly, the data is split by run number and part number.
# These numbers were defined above in the sample data, but it is calculated here
# so that this code can be used to perform this test on arbitrary data from
# a CSV database.

# Determine the number of levels for each factor
n_ops = len(ops)
n_reps = len(reps)
n_parts = len(parts)
n_total = n_ops*n_parts*n_reps

# Next the degrees of freedom for each factor are calculated following the
# procedure for a crossed ANOVA with interaction.
DOF_total = n_total - 1
DOF_ops = n_ops-1
DOF_parts = n_parts-1
DOF_partxop = DOF_parts*DOF_ops
DOF_rep = n_parts*n_ops*(n_reps-1)

# The following finds the sum of squares for the difference between the mean
# observation of a given part and the mean of the observations across the
# entire study.
SSpart = 0
for part in parts.keys():
    SSpart += (parts[part]["Observation"].mean() - xbar_grand)**2

SSpart = SSpart * n_ops * n_reps

SSop = 0
for op in ops.keys():
    SSop += (ops[op]["Observation"].mean() - xbar_grand)**2

SSop = SSop * n_parts * n_reps

# For the operator * part interaction, a sub-dataframe is defined.
subdf = dict((x,y) for x,y in df.groupby(["Operator","Part"]))

# Initialize a list to hold the means for the interactions
interaction_xbar = {}
for key in subdf.keys():
    temp = subdf[key]["Observation"].mean()
    interaction_xbar[key] = temp

# The repeatability sum of squares and the total sum of squares can be computed
# in the same loop as they both require us to iterate over the entire dataset.
SSrep = 0
SStot = 0
for index, x in df.iterrows():
    key = (x["Operator"],x["Part"])
    SSrep += (x["Observation"] - interaction_xbar[key])**2
    SStot += (x["Observation"]-xbar_grand)**2

SSpartxop = SStot - SSpart-SSop-SSrep

# The following section calculates the mean squares for various sources
MSpart = SSpart/DOF_parts
MSop = SSop/DOF_ops
MSpartxop = SSpartxop/DOF_partxop
MSrep = SSrep/DOF_rep

print("SSpart      = {0:>4.3f} DFpart      = {1:>4.3f} MSpart      = {2:>4.3f}".format(SSpart, DOF_parts, MSpart))
print("SSop        = {0:>4.3f} DFop        = {1:>4.3f} MSop        = {2:>4.3f}".format(SSop, DOF_ops, MSop))
print("SSrep       = {0:>4.3f} DFrep       = {1:>4.3f} MSrep       = {2:>4.3f}".format(SSrep, DOF_rep, MSrep))
print("SSpartxop   = {0:>4.3f} DFpartxop   = {1:>4.3f} MSpartxop   = {2:>4.3f}".format(SSpartxop, DOF_partxop, MSpartxop))
print("SStotal     = {0:>4.3f} DFtotal     = {1:>4.3f}".format(SStot, DOF_total))
