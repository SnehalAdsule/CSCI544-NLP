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

class avg_perModelClass:
    def __init__(self,iter=30):
        self.weights = {}
        self.arr_data_points=[]
        self.bias=0
        self.avg_weights={}
        self.avg_bias=0
        self.count=0
        self.max_iteration = iter



def outputData(dir_path, avg_per, filename):
    try:
        outStream = open(filename, 'w',encoding='latin1')
        #outStream = open(filename, 'w')
        # outStream.write('(vocabulary=$#$,'+str(avg_per.vocabulary)+')'+\n)
        outStream.write('bias=$#$' + str(avg_per.avg_bias) + '\n')
        outStream.write('weights=$#$' + str(avg_per.avg_weights))
        outStream.close()
        print (len(avg_per.weights))
        return 'Output to ' + filename
    except:
        return '[ERROR] Output to ' + filename


def readData(dir_path, avg_per):
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
                #with open(file_path, "r") as f:
                with open(file_path,"r",encoding="latin1") as f:
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
                avg_per.arr_data_points.append((y,temp_vocab))
                #print avg_per.arr_data_points

            else: #if not ".txt"
                continue
    print ('no of samples ',count)

def main(path):
    avg_per = avg_perModelClass()
    readData(path, avg_per)
    avg_per.weights={}
    avg_per.avg_weights={}
    avg_per.bias=0
    avg_per.avg_bias=0
    avg_per.count=1
    for i in range(0,avg_per.max_iteration):
        random.shuffle(avg_per.arr_data_points)
        for (y,word_list) in avg_per.arr_data_points:
            alpha=0
            #print y,x_d
            for word in word_list:
                if word not in avg_per.weights:
                    avg_per.weights[word]=0
                    avg_per.avg_weights[word]=0
                alpha=alpha + (avg_per.weights[word] * word_list[word])
            alpha=alpha+avg_per.bias

            check_update= y * alpha
            #print check_update ,'=(',y, alpha,'), bias=' , avg_per.bias, '\t',

            if check_update <= 0:
                avg_per.bias=avg_per.bias+y
                avg_per.avg_bias=avg_per.avg_bias+(y*avg_per.count)

                for word in word_list:
                    avg_per.weights[word]= avg_per.weights[word] + (word_list[word]*y)
                    avg_per.avg_weights[word]= avg_per.avg_weights[word] + ((word_list[word]*y)*avg_per.count)

            avg_per.count=avg_per.count+1
            #print (avg_per.count,"\t", check_update ,'=(',y, alpha,'), bias=' , avg_per.bias, avg_per.avg_bias,'\t '
            #,len(avg_per.avg_weights))

    for word in avg_per.avg_weights:
        avg_per.avg_weights[word]=avg_per.weights[word] -(avg_per.avg_weights[word]/avg_per.count)
    avg_per.avg_bias=avg_per.bias - (avg_per.avg_bias/avg_per.count)

    cwd = os.getcwd()
    print (outputData(cwd, avg_per, 'per_model.txt'))

print ('Running avg_per_learn')
main(path)