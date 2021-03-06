import os
import sys
import operator
import math

try:
    path = sys.argv[1]
    output_file=sys.argv[2]
except:
    print ('path not correct Resetting path to cwd')
    path= os.getcwd()
    output_file='per_output.txt'

print (path)

class perModel:
    def __init__(self):
        self.weights = {}
        self.bias = 0
        self.output={}

    def readModelData(self):
        print('reading file')
        with open("per_model.txt", "r", encoding="latin1") as file:
        #with open('per_model.txt','r') as file:
            data=file.read()
            lines=data.split('\n')
            print (len(lines))
            count=0
            for line in lines:
                parts= line.split('=$#$')
                if count <1:
                    self.__dict__[str(parts[0])]=float(parts[1])
                    print (parts[0],'\t :: \t',parts[1])
                else:
                    self.__dict__[str(parts[0])]=eval(parts[1])
                    #print parts[0],'\t :: \t',parts[1],'\n'
                count = count + 1
            print (len(per.weights))

def outputLabel(dir_path,per):
    try:
        outStream = open(output_file, 'w',encoding="latin1")
        #outStream = open(output_file, 'w')
        #print (per.output)
        for k,v in per.output.items():
            outStream.write(per.output[k]+' '+k+'\n')
        outStream.close()
        return 'check to peroutput.txt'
    except:
        return '[ERROR] Output to peroutput.txt',sys.exc_info()

def predictTrainingLabels(dir_path):
    #read test directory
    output={}
    num=0
    for dirpath, sdirs, files in os.walk(dir_path):
        for filename in files:
            file_path = os.path.join(dirpath, filename)
            #print file_path,
            if filename.endswith('.txt'):
                #print flag,filename
                spl_char = '!%^_`{|}~"#$&\'()*+,-./:;<=>@[\\]\n'
                with open(file_path,"r",encoding="latin1") as f:
                #with open(file_path,"r") as f:
                    #tokens= map(lambda w: w.strip(spl_char), f.read().split())
                    tokens= map(lambda w: w, f.read().split())
                    alpha = 0
                    # print y,x_d

                word_list={}
                for word in tokens:
                    if word not in word_list:
                        word_list[word] = 1
                    else:
                        word_list[word]=word_list[word]+1
                    if word not in per.weights:
                        per.weights[word] = 0
                #print len(tokens),len(word_list),len(per.weights)
                for word in word_list:
                    alpha = alpha + (per.weights[word] * word_list[word])
                alpha = alpha + per.bias

                if alpha > 0:
                    label = 'SPAM'
                else:
                    label = 'HAM'
                f_name = os.path.join(dirpath, filename)
                per.output[f_name] = label
                #print per.output

                '''
                    if a_flag.upper()!=label:
                        print 'actual:',a_flag,'predicted:',label,'\tspam',p_spam_msg,'ham',p_ham_msg,'\t',f_name
                '''
print ('Running per_classify')
per=perModel()
per.readModelData()
print ('test data')
predictTrainingLabels(path)
print ('prediction over, Output Data')
cwd=os.getcwd()
print (outputLabel(cwd,per))
