import datetime
import pandas as pd

def hashfunc(date):
    return datetime.date.fromisoformat(date)

def dtos(d):
    i = str(d)
    r = i[:4]+'-'+i[4:-2]+'-'+i[-2:]
    return r

def des(d):
    i = str(d)
    r = i[:5]+i[5:-3]+i[-4:]
    return r

class hashdate:
    def __init__(self,length,start):
        self.t = [None]*length
        self.start = datetime.date.fromisoformat(dtos(start))
        self.size = length
        
    def insert(self, date, id):
        if(isinstance(date,int)):
            i = (hashfunc(dtos(date)) - self.start).days
        else:
            i = (date - self.start).days
        if self.t[i] != None:
            self.t[i].append(id)
        else:
            self.t[i] = [id]
            
    def delete_id(self, date, id):
        if(len(date)==8):
            i = (hashfunc(dtos(date)) - self.start).days
        else:
            i = (hashfunc(des(date)) - self.start).days
        if self.t[i] != None:
            if id in self.t[i]:
                self.t[i].remove(id)
            else:
                print('id does not exist in this date')
        else:
            print('date does not exist')
            
    def delete_date(self, date):
        if(len(date)==8):
            i = (hashfunc(dtos(date)) - self.start).days
        else:
            i = (hashfunc(des(date)) - self.start).days
        if self.t[i] != None:
            self.t[i] = None
        else:
            print('date does not exist')
    
    def display(self):
        for i in range(0,self.size):
            if(self.t[i]!=None):
                date = (self.start + datetime.timedelta(days = i)).isoformat()
                print(date, ' : ', self.t[i])
                
        #print(self.t)
    
    def search(self, dateb, dated):
        b = (hashfunc(dtos(dateb)) - self.start).days
        e = pd.date_range(dtos(dateb),dtos(dated))
        print('b=',b)
        print('e=',len(e))
        rn = 0
        for i in range(b,b+len(e)-1):
            if(self.t[i]!=None):
                date = (self.start + datetime.timedelta(days = i)).isoformat()
                print(date, ' : ', self.t[i])
                rn+=len(self.t[i])
        print(rn)
        return rn

    def outd(self,index):
        d = (self.start + datetime.timedelta(days = index)).isoformat()
        ts = str(d)
        os = ts[:4] + ts[5:-3]+ ts[-2:]
        return os
    def outn(self,index):
        return len(self.t[index])
        
    def backsum (self,date):
        b = (hashfunc(dtos(date)) - self.start).days
        if(b<2):
            b=2
        if(b>self.size-1):
            b= self.size-1
        #print(b)
        rn = 0
        for i in range(b-2,b+1):
            if(self.t[i]!=None):
                rn+=len(self.t[i])
        return rn


#test code
'''
test = hashdate(30,20200601)
test.out(0)
test.out(1)
test.out(2)

test.insert(20200616, 2)
#test.display()
test.insert(20200601, 3)
test.insert(20200601, 4)
test.insert(20200601, 5)      
#test.display()
test.delete_id(20200601,5)
#test.display()
test.delete_date(20200602)
#test.display()
test.search(20200601,20200601)
print(test.out(20200601))
'''