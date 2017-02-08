import os
import sys
import operator
import sys

if sys.version_info[0] >= 3:
    import argparse
    try:
        path = sys.argv[1]
    except:
        print ('path not correct Resetting path to cwd')
        path= os.getcwd()
else:

    try:
        print ('OK',sys.version_info[0])
        path = sys.argv[1]
    except:
        print ('path not correct Resetting path to cwd')
        path= os.getcwd()


print (path)

class nbModelClass:

    def __init__(self):
        self.vocabulary={}
        self.n_spam_doc=0.0
        self.n_ham_doc=0.0
        self.n_total_doc=0.0
        self.vocabulary_count=0.0
        self.spam_vocab={}
        self.ham_vocab={}    
    def spam_vocab_count(self,word=None):
        a=0
        if word!=None:
            a=self.spam_vocab[word]
        else:
            for k,val in self.spam_vocab.items():
                a=a+val
        return a

        
def outputData(dir_path,nb,filename):
    try:
        outStream = open(filename, 'w')
        #outStream = open(filename, 'w',encoding='latin1')
        #outStream.write('(vocabulary=$#$,'+str(nb.vocabulary)+')'+\n)
        outStream.write('n_spam_doc=$#$'+str(nb.n_spam_doc)+'\n')
        outStream.write('n_ham_doc=$#$'+str(nb.n_ham_doc)+'\n')
        nb.vocabulary_count=len(nb.vocabulary)
        outStream.write('vocab_count=$#$'+str(nb.vocabulary_count)+'\n')
        outStream.write('spam_vocab=$#$'+str(nb.spam_vocab)+'\n')
        outStream.write('ham_vocab=$#$'+str(nb.ham_vocab))
        outStream.close()
        print len(nb.ham_vocab)
        return 'Output to '+filename
    except:
        return '[ERROR] Output to '+filename

def readData(dir_path,nb):
    if not os.path.exists(dir_path):
        print('Error! Given path is not a valid directory.')
        dir_path=r'./Spam or Ham/dev'

    for root, sdirs, files in os.walk(dir_path):
        for filename in files:

            file_path = os.path.join(root, filename)
            #print file_path,
            if filename.endswith('.txt'):
                flag='unknown'
                if filename.endswith('.ham.txt'):
                    nb.n_ham_doc=nb.n_ham_doc+1
                    flag='ham'
                elif filename.endswith('.spam.txt') :
                    nb.n_spam_doc=nb.n_spam_doc+1
                    flag='spam'

                else:
                    print ('[ERROR]',flag ,filename)
                    continue

                #print flag,filename
                spl_char = '!%^_`{|}~"#$&\'()*+,-./:;<=>@[\\]\n'
                with open(file_path,"r") as f:
                #with open(file_path,"r",encoding="latin1") as f:
                    #tokens= map(lambda w: w.strip(spl_char).upper(), f.read().split())
                    tokens= map(lambda w: w, f.read().split())
                for word in tokens:

                    if word in nb.vocabulary:
                        nb.vocabulary[word]=nb.vocabulary[word]+1
                    else:
                        nb.vocabulary[word]=1

                    if flag=='ham':
                        if word in nb.ham_vocab:
                            nb.ham_vocab[word]=nb.ham_vocab[word]+1
                        else:
                            nb.ham_vocab[word]=1

                    if flag=='spam':
                        if word in nb.spam_vocab:
                            nb.spam_vocab[word]=nb.spam_vocab[word]+1
                        else:
                            nb.spam_vocab[word]=1
            else:
                continue
    print (nb.n_spam_doc,nb.n_ham_doc)
    nb.n_total_doc=nb.n_spam_doc+nb.n_ham_doc
    if(nb.n_total_doc >0):
        p_spam=nb.n_spam_doc/nb.n_total_doc
        p_ham=nb.n_ham_doc/nb.n_total_doc
        print ('P(spam)=',p_spam,'P(ham)=',p_ham)
    print ('V=',len(nb.vocabulary), 'V_spam',len(nb.spam_vocab),'V_ham',len(nb.ham_vocab))
def main(path):
    nb=nbModelClass()
    readData(path,nb)
    cwd=os.getcwd()
    print (outputData(cwd,nb,'nbmodel.txt'))
main(path)