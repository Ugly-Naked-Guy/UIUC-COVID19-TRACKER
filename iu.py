import csv
import hashdate as hd



with open('Illini_Union.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)
del data[0]
iud = []
iuo = []
data.sort(key=lambda x:x[1])

for i in range(0,len(data)):
    iud.append((data[i][1],data[i][2]))
print('ahd:')
#print(ahd)
iuh = hd.hashdate(365,20200101)
for i in range(0,len(iud)):
    iuh.insert(iud[i][0], iud[i][1])
print('ahh:')
iuh.display()
for i in range(0,len(iuh.t)):
    if iuh.t[i] != None:
        iuo.append((iuh.outd(i),iuh.outn(i)))
        #print(ahh.outd(i))
print('aho:')
print(iuo)