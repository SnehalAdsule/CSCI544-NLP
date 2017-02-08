import os
import sys
import operator
import math

try:
    path = sys.argv[1]
except:
    print ('path not correct Resetting path to cwd')
    path= os.getcwd()
print (path)
unknown_spam_words={}
unknown_ham_words={}

def sumWord(in_dict):
    sum=0
    for k,v in in_dict.items():
        sum=sum+v
    return sum

class nbModel:
    def __init__(self):
        #self.vocabulary={}
        self.n_spam_doc=0.0
        self.n_ham_doc=0.0
        self.n_total_doc=0.0
        self.vocab_count=0.0
        self.n_spam_vocab=0.0
        self.n_ham_vocab=0.0
        self.spam_vocab={}
        self.ham_vocab={}
        self.p_spam=0.0
        self.p_ham=0.0
        self.output={}
    def readModelData(self):
        print('reading file')
        '''cwd=os.getcwd()
        out_filepath=os.path.join(cwd,"nbmodel.txt")
        with open("","r",encoding="latin1") as file:'''
        #with open("", "r", encoding="latin1") as file:
        with open('nbmodel.txt','r') as file:
            data=file.read()
            lines=data.split('\n')
            #print lines
            count=0
            for line in lines:
                count=count+1
                parts= line.split('=$#$')
                print count
                print parts[0],'\t :: \t',parts[1],'\n'
                if count<4:
                    self.__dict__[str(parts[0])]=float(parts[1])
                    print (parts[0],'\t :: \t',parts[1])
                elif count <6:
                    self.__dict__[str(parts[0])]=eval(parts[1])
                    #print parts[0],'\t :: \t',parts[1],'\n'

            #print count
    def spam_vocab_count(self,word=None):
        a=0
        try:
            if word in self.spam_vocab.keys():
                a=self.spam_vocab[word]
            else:
                a=0
        except:
            a=0

        return a
    def ham_vocab_count(self,word=None):
        a=0
        try:
            if word in self.ham_vocab.keys():
                a=self.ham_vocab[word]
            else:
                a=0
        except:
            a=0

        return a

    def calcProbability(self,label,word):
        if label=='ham':
            p_word_k=(self.ham_vocab_count(word)+1.0)/float(self.ham_vocab_count+self.vocab_count)
        else:
            p_word_k=(self.spam_vocab_count(word)+1.0)/float(self.spam_vocab_count(None)+self.vocab_count)
        return p_word_k

    def calcLogProbability(self,label,word):
        if label=='ham':
            p_word_k=math.log(self.ham_vocab_count(word)+1.0) -math.log(float(self.n_ham_vocab+self.vocab_count))
        else:
            p_word_k=math.log(self.spam_vocab_count(word)+1.0) -math.log(float(self.n_spam_vocab+self.vocab_count))
        return p_word_k

def outputLabel(dir_path,nb):
    try:
        outStream = open('nboutput.txt', 'w')
        #print (nb.output)
        #outStream.write('(vocabulary=$#$,'+str(nb.vocabulary)+')\n')
        for k,v in nb.output.items():
            outStream.write(nb.output[k]+' '+k+'\n')
        outStream.close()
        return 'check to nboutput.txt'
    except:
        return '[ERROR] Output to nboutput.txt',sys.exc_info()

def predictTrainingLabels(dir_path):
    #read test directory
    output={}
    for dirpath, sdirs, files in os.walk(dir_path):
        for filename in files:
            file_path = os.path.join(dirpath, filename)
            #print file_path,
            if filename.endswith('.txt'):
                '''
                # nbclassify - actual class not known
                a_flag='unknown'
                if filename.endswith('.ham.txt'):
                    a_flag='ham'
                elif filename.endswith('.spam.txt'):
                    a_flag='spam'
                else:
                    a_flag='unknown'
                    #print 'unknown reading File',a_flag ,filename
                    #continue
                '''
                #print flag,filename
                spl_char = '!%^_`{|}~"#$&\'()*+,-./:;<=>@[\\]\n'
                with open(file_path,"r") as f:
                #with open(file_path,"r",encoding="latin1") as f:
                    #tokens= map(lambda w: w.strip(spl_char), f.read().split())
                    tokens= map(lambda w: w, f.read().split())
                    p_spam_msg=math.log(nb.p_spam)
                    p_ham_msg=math.log(nb.p_ham)

                    for word in tokens:
                         p_word_spam=nb.calcLogProbability('spam',word)
                         p_word_ham=nb.calcLogProbability('ham',word)
                         p_spam_msg=p_spam_msg+p_word_spam
                         p_ham_msg=p_ham_msg+p_word_ham
                         #print word,p_word_spam,p_word_ham,p_spam_msg,p_ham_msg

                    if p_spam_msg >p_ham_msg:
                        label='SPAM'
                    else:
                        label='HAM'
                    f_name=os.path.join(dirpath, filename)
                    nb.output[f_name]=label
                    print nb.output
                    '''
                    if a_flag.upper()!=label:
                        print 'actual:',a_flag,'predicted:',label,'\tspam',p_spam_msg,'ham',p_ham_msg,'\t',f_name
                    '''
                    #break


nb=nbModel()
nb.readModelData()
print nb.n_ham_doc,nb.spam_vocab_count(None)
nb.n_total_doc=nb.n_spam_doc+nb.n_ham_doc
nb.p_spam=nb.n_spam_doc/nb.n_total_doc
nb.p_ham=nb.n_ham_doc/nb.n_total_doc
'''nb.n_spam_vocab=len(nb.spam_vocab)
nb.n_ham_vocab=len(nb.ham_vocab)'''
nb.n_spam_vocab=sumWord(nb.spam_vocab)
nb.n_ham_vocab=sumWord(nb.ham_vocab)
print 'test data'
predictTrainingLabels(path)
print ('over')
cwd=os.getcwd()
print (outputLabel(cwd,nb))
