import os
import sys
from sklearn.cross_validation import train_test_split
path = sys.argv[1]#r'C:\Users\Snehal\Desktop\Acads\CSCI 544\sample labeled data'
os.listdir(path)
X = y= os.listdir(path)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)
#print (X_train)
#print (X_test)

if not os.path.exists(os.path.join(path, 'train')):
    os.makedirs(os.path.join(path, 'train'))
if not os.path.exists(os.path.join(path, 'test')):
    os.makedirs(os.path.join(path, 'test'))

for x in X_train:
     org = os.path.join(path, x)
     train = os.path.join(path,'train', x)
     print (org,train)
     os.rename(org ,train)

for x in X_test:
    org = os.path.join(path, x)
    test = os.path.join(path, 'test', x)
    print(org, test)
    os.rename(org, test)
