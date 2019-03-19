import os
import misc_functions as mf
import csv
import Solenoid_on_response
import Solenoid_off_response

rfile="warrants.csv"
RDR = csv.reader(open(rfile))
data_dir = "Parametric Data"
sep="\\"
log = open("log.txt", mode='a')

warrants = []
for row in RDR:
    warrants.append(int(row[0]))

good,bad = mf.gen_warrant_links(warrants)

paths = []
print("{} Good links".format(mf.timestamp()),file=log)
for g in good:
    sub_dir = mf.similar_dir(g,data_dir,0.5)
    if not sub_dir == None:
        path = sep.join([g,sub_dir])
        if os.path.isdir(path):
            paths.append(sep.join([g,sub_dir]))
        else:
            print("{} {} is not a directory.".format(mf.timestamp(),
                                                     path),
                  file=log)
    else:
        print("{} Parametric data folder not found in {}.".format(mf.timestamp(),
                                                                  g),
              file=log)
        bad.append(g)
    
print("\n{} Bad links".format(mf.timestamp()),file=log)
for b in bad:
    print("{} {}".format(mf.timestamp(),b),file=log)

log.close()
for p in paths:
    log = open("log.txt", mode='a')
    print("\n{} Processing {} On response time.".format(mf.timestamp(),
                                                      p),
          file=log)
    log.close()
    Solenoid_on_response.main(p)

    log = open("log.txt", mode='a')
    print("\n{} Processing {} Off response time.".format(mf.timestamp(),
                                                       p),
          file=log)
    log.close()
    Solenoid_off_response.main(p)
    
