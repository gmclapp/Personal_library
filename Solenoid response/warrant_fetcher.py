import misc_functions as mf
import csv
import Solenoid_on_response

rfile="warrants.csv"
RDR = csv.reader(open(rfile))
data_dir = "Parametric Data"
sep="\\"

warrants = []
for row in RDR:
    warrants.append(int(row[0]))

good,bad = mf.gen_warrant_links(warrants)

paths = []
print("Good links")
for g in good:
    sub_dir = mf.similar_dir(g,data_dir)
    paths.append(sep.join([g,sub_dir]))
    
print("\nBad links")
for b in bad:
    print(b)
    
for p in paths:
    #print(p)
    Solenoid_on_response.main()
    
