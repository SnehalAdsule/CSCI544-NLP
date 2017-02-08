import os
import sys
import operator
import sys
import shutil

path=sys.argv[1]
dest_path=sys.argv[2]
dest_path1=sys.argv[3]

if not os.path.exists(dest_path):
    os.makedirs(dest_path)
if not os.path.exists(dest_path1):
    os.makedirs(dest_path1)

def copyFile(train_path,dest_path):
    count=0
    print ('CopyFile')

    if not os.path.exists(dest_path1):
        os.makedirs(dest_path1)
    for root, sdirs, files in os.walk(train_path):

        for filename in files:
            file_path = os.path.join(root, filename)
            #print file_path,
            if filename.endswith('.txt'):
                count=count+1
                flag='unknown'
                src=os.path.join(root,filename)
                if filename.endswith('.ham.txt'):
                    flag='ham'
                    dest=os.path.join(dest_path,'ham',filename)
                elif filename.endswith('.spam.txt') :
                    flag='spam'
                    dest=os.path.join(dest_path,'spam',filename)

                if not os.path.exists(os.path.join(dest_path,'ham')):
                    os.makedirs(os.path.join(dest_path,'ham'))
                if not os.path.exists(os.path.join(dest_path,'spam')):
                    os.makedirs(os.path.join(dest_path,'spam'))

                shutil.copyfile(src, dest)
            #print count
    return count

def copy10(train_path,dest_path,count):
    print ('Copy 10 % training data',count,train_path,dest_path)
    spam_count=0
    ham_count=0
    for root, sdirs, files in os.walk(train_path):

        for filename in files:
            file_path = os.path.join(root, filename)
            if filename.endswith('.txt'):
                flag='unknown'
                src=os.path.join(root,filename)
                if filename.endswith('.ham.txt'):

                    dest=os.path.join(dest_path,filename)
                    if ham_count<=count :
                        ham_count=ham_count+1
                        shutil.copyfile(src, dest)
                elif filename.endswith('.spam.txt') :

                    dest=os.path.join(dest_path,filename)
                    if spam_count<=count :
                        spam_count=spam_count+1
                        shutil.copyfile(src, dest)
            #print count,ham_count,spam_count

count = copyFile(path,dest_path)
count_10=count/10
print (count_10)
equal_sample=count_10/2
copy10(dest_path,dest_path1,count_10)

