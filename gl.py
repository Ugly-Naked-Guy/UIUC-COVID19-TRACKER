import csv
import hashdate as hd



with open('Grainger_Library.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)
del data[0]
gld = []
glo = []
data.sort(key=lambda x:x[1])

for i in range(0,len(data)):
    gld.append((data[i][1],data[i][2]))
print('ahd:')
#print(ahd)
glh = hd.hashdate(365,20200101)
for i in range(0,len(gld)):
    glh.insert(gld[i][0], gld[i][1])
print('ahh:')
glh.display()
for i in range(0,len(glh.t)):
    if glh.t[i] != None:
        glo.append((glh.outd(i),glh.outn(i)))
        #print(ahh.outd(i))
print('aho:')
print(glo)