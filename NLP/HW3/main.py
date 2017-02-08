from hw3_corpus_tool import get_data
import sys

def check_structure(arr):
    len_arr=len(arr)
    for i in range(len_arr):
        try:
            if len(arr[i]):
                check_structure(arr[i])
        except:
            print "no furthur decomposition"
            print arr[i]

path = sys.argv[1]
print 'path',path
doc= get_data(path)

for i in doc:
    print i
