import csv
import hashdate as hd



with open('Altgeld_Hall.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)
del data[0]
ahd = []
aho = []
data.sort(key=lambda x:x[1])

for i in range(0,len(data)):
    ahd.append((data[i][1],data[i][2]))
print('ahd:')
#print(ahd)
ahh = hd.hashdate(365,20200101)
for i in range(0,len(ahd)):
    ahh.insert(ahd[i][0], ahd[i][1])
print('ahh:')
#ahh.display()
for i in range(0,len(ahh.t)):
    if ahh.t[i] != None:
        aho.append((ahh.outd(i),ahh.outn(i)))
        #print(ahh.outd(i))
print('aho:')
print(aho)