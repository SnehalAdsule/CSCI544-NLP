import os
import sys
import operator
import sys
import random

if sys.version_info[0] >= 3:
    import argparse

    try:
        path = sys.argv[1]
    except:
        print ('path not correct Resetting path to cwd')
        path = os.getcwd()
else:

    try:
        print ('OK', sys.version_info[0])
        path = sys.argv[1]
    except:
        print ('path not correct Resetting path to cwd')
        path = os.getcwd()

print (path)

class data_point:
    def __init__(self,type,v_words):
        self.doc_class= type
        self.v_words=v_words

class perModelClass:
    def __init__(self,iter=20):
        self.weights = {}
        self.arr_data_points=[]
        self.bias=0
        self.max_iteration=iter



def outputData(dir_path, per, filename):
    try:
        #outStream = open(filename, 'w',encoding='latin1')
        outStream = open(filename, 'w')
        # outStream.write('(vocabulary=$#$,'+str(per.vocabulary)+')'+\n)
        outStream.write('bias=$#$' + str(per.bias) + '\n')
        outStream.write('weights=$#$' + str(per.weights))
        outStream.close()
        print (len(per.weights))

        ''
        return 'Output to ' + filename
    except:
        return '[ERROR] Output to ' + filename


def readData(dir_path, per):
    count=0
    if not os.path.exists(dir_path):
        print('Error! Given path is not a valid directory.')
        dir_path = r'./Spam or Ham/dev'

    for root, sdirs, files in os.walk(dir_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            # print file_path,
            if filename.endswith('.txt'):
                flag = 'unknown'
                if filename.endswith('.ham.txt'):
                    flag = 'ham'
                    y=-1
                elif filename.endswith('.spam.txt'):
                    flag = 'spam'
                    y=1
                else:
                    print ('[ERROR]', flag, filename)
                    continue
                # print flag,filename
                spl_char = '!%^_`{|}~"#$&\'()*+,-./:;<=>@[\\]\n'
                with open(file_path, "r") as f:
                #with open(file_path,"r",encoding="latin1") as f:
                    # tokens= map(lambda w: w.strip(spl_char).upper(), f.read().split())
                    tokens = map(lambda w: w, f.read().split())
                count=count+1
                temp_vocab={}
                for word in tokens:
                    if word in temp_vocab:
                        temp_vocab[word] = temp_vocab[word] + 1
                    else:
                        temp_vocab[word] = 1
                #print temp_vocab,flag,'\n'
                per.arr_data_points.append((y,temp_vocab))
                #print per.arr_data_points

            else: #if not ".txt"
                continue
    print ('no of samples ',count)

def main(path):
    per = perModelClass()
    readData(path, per)
    per.weights={}
    per.bias=0
    for i in range(0,per.max_iteration):
        random.shuffle(per.arr_data_points)
        for (y,word_list) in per.arr_data_points:
            alpha=0
            #print y,x_d
            for word in word_list:
                if word not in per.weights:
                    per.weights[word]=0
                alpha=alpha + (per.weights[word] * word_list[word])
            alpha=alpha+per.bias

            check_update= y * alpha
            #print check_update ,'=(',y, alpha,'), bias=' , per.bias, '\t',

            if check_update <= 0:
                per.bias=per.bias+y
                for word in word_list:
                    per.weights[word]= per.weights[word] + (word_list[word]*y)
        #print ("\t", check_update ,'=(',y, alpha,'), bias=' , per.bias, '\t ',len(per.weights))

    cwd = os.getcwd()
    print (outputData(cwd, per, 'per_model.txt'))

print ('Running per_learn')
main(path)