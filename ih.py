import csv
import hashdate as hd



with open('Illini_Hall.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)
del data[0]
ihd = []
iho = []
data.sort(key=lambda x:x[1])

for i in range(0,len(data)):
    ihd.append((data[i][1],data[i][2]))
print('ahd:')
#print(ahd)
ihh = hd.hashdate(365,20200101)
for i in range(0,len(ihd)):
    ihh.insert(ihd[i][0], ihd[i][1])
print('ahh:')
ihh.display()
for i in range(0,len(ihh.t)):
    if ihh.t[i] != None:
        iho.append((ihh.outd(i),ihh.outn(i)))
        #print(ahh.outd(i))
print('aho:')
print(iho)