import csv
import hashdate as hd



with open('Bookstore.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)
del data[0]
bsd = []
bso = []
data.sort(key=lambda x:x[1])

for i in range(0,len(data)):
    bsd.append((data[i][1],data[i][2]))
print('ahd:')
#print(ahd)
bsh = hd.hashdate(365,20200101)
for i in range(0,len(bsd)):
    bsh.insert(bsd[i][0], bsd[i][1])
print('ahh:')
bsh.display()
for i in range(0,len(bsh.t)):
    if bsh.t[i] != None:
        bso.append((bsh.outd(i),bsh.outn(i)))
        #print(ahh.outd(i))
print('aho:')
print(bso)