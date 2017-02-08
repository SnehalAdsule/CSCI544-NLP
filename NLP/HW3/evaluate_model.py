import sys
import os
import csv
import string
testdir=sys.argv[1]
#testdir=r'C:\Users\Snehal\Desktop\Acads\CSCI 544\sample labeled data\test'
outpufile=sys.argv[2]
#outpufile='output.txt'
total=0.0
correct=0.0
print(outpufile)
output_dict={}
test_dict={}
with open(outpufile, 'r') as file:
    data = file.read()
    lines = data.split('\n')
    # print lines
    count = 0
    for line in lines:
        count = count + 1
        if line.startswith("Filename="):
            parts = line.split('=')
            filename=r''+os.path.join(testdir, parts[1].replace("\"","")).replace("//","'")
            output_dict[filename] =[]
        else:
            output_dict[filename].append(line)
print('reading the test labels')
for filename,list_labels in output_dict.items():
    #filename = r'' + os.path.join(testdir, parts[1].replace("\"", "")).replace("//", "'")
    print('test files',filename)
    first_line=True
    with open(filename, 'r') as testfile:
                testdata = testfile.read()
                testlines = testdata.split('\n')

                for row in testlines:
                    if first_line:
                        first_line=False
                        test_dict[filename] = []
                    else:
                        col=row.split(",")
                        test_dict[filename].append(col[0])
                        #print('test row',col[0])


for k,v in output_dict.items():
    list2=test_dict[k]
    print (string.punctuation)
    for i in range(len(list2)):

        if(list2[i].replace("\"","")==v[i].replace("\"","")):
            correct+=1
        total+=1
        print(list2[i], v[i],correct,total)
print("Baseline Acccuracy = "+str(correct/total)+'\n')

print("Advanced Acccuracy = "+str(correct/total)+'\n')
