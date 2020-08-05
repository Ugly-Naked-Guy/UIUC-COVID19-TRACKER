import csv
import hashdate as hd



with open('ECE_building.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)
del data[0]
ebd = []
ebo = []
data.sort(key=lambda x:x[1])

for i in range(0,len(data)):
    ebd.append((data[i][1],data[i][2]))
print('ahd:')
#print(ahd)
ebh = hd.hashdate(365,20200101)
for i in range(0,len(ebd)):
    ebh.insert(ebd[i][0], ebd[i][1])
print('ahh:')
ebh.display()
for i in range(0,len(ebh.t)):
    if ebh.t[i] != None:
        ebo.append((ebh.outd(i),ebh.outn(i)))
        #print(ahh.outd(i))
print('aho:')
print(ebo)