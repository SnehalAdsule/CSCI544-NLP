import operator

def sumWord(in_dict):
    sum=0
    for k,v in in_dict.items():
        sum=sum+v
    return sum
d={'a':1,'b':2,'c':5}
e={'a':10,'d':4,'c':2}
print sumWord(d)
word=None
try:
    if word!=None:
        print d['e']
    else:
        print word
except:
    print 'unknown'

for k,v in e.items():
    print 'v=',v
    if k in d.keys():
        d[k]=d[k]+e[k]
    else :
        d[k]=e[k]
print (d,'hello')
print (e)
d_list= sorted(d.items(),key=operator.itemgetter(1),reverse=True)
print str(d)
count=0
for k in d_list:
    print count,'Key',k[0],'val',k[1]
    count=count+1
    if count>4:
        break

class dummyC:
    def __init__(self):
        self.name='blank'


dummy=dummyC()
print dummy.__dict__['name']