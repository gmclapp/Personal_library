import random
import pandas as pd
import matplotlib.pyplot as plt

random.seed(6168850734)

Mold = [{"Offset":-2.5,"Variation":0.625,"Data":[]},
        {"Offset":0,"Variation":0.313,"Data":[]}]

Operators = [{"Name":"Andy","Offset":3.0,"Variation":1.25,"Data":[]},
             {"Name":"Susan","Offset":1.25,"Variation":0.125,"Data":[]},
             {"Name":"Brian","Offset":-5.5,"Variation":0.45,"Data":[]}]

Weibull_factor = [{"Name":"Glass fill","Scale":1,"Shape":1,"Data":[]}]

Parts = []

replicates = 20
ops = int(len(Operators))
cavities = int(len(Mold))
factors = int(len(Weibull_factor))
n = ops*cavities*replicates

for i in range(n):
    op_data = random.normalvariate(Operators[i%ops]["Offset"],
                                   Operators[i%ops]["Variation"])
    Operators[i%ops]["Data"].append(op_data)

    cavity_data = random.normalvariate(Mold[i%cavities]["Offset"],
                                       Mold[i%cavities]["Variation"])    
    Mold[i%cavities]["Data"].append(cavity_data)

    weibull_data = random.weibullvariate(Weibull_factor[i%factors]["Scale"],
                                         Weibull_factor[i%factors]["Shape"])
    Weibull_factor[i%factors]["Data"].append(weibull_data)

    part_data = op_data + cavity_data + weibull_data
    Parts.append({"Operator":i%ops,
                  "Cavity":i%cavities,
                  "Weibull factor":i%factors,
                  "Data":part_data})

df = pd.DataFrame.from_dict(Parts)
df.to_csv('Data.csv')
# print(Parts)
