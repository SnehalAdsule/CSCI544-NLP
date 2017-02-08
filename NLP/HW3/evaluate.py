import csv
import sys

#file1=sys.argv[1]
#file2=sys.argv[2]
file1=r'C:\Users\Snehal\Desktop\Acads\CSCI 544\labeled data\0001.csv'
file2=r"C:\Users\Snehal\Desktop\Acads\CSCI 544\sample labeled data\train\0001.csv"

print("/".join("a"))
list_token=['1', 'TOKEN_What', 'TOKEN_are', 'TOKEN_your', 'TOKEN_favorite', 'TOKEN_programs', 'TOKEN_?',
            'POS_WP', 'POS_VBP', 'POS_PRP$', 'POS_JJ', 'POS_NNS', 'POS_.'], \
           ['1', 'TOKEN_Uh', 'TOKEN_,', 'TOKEN_it', "TOKEN_'s", 'TOKEN_kind', 'TOKEN_of', 'TOKEN_hard', 'TOKEN_to', 'TOKEN_put', 'TOKEN_my', 'TOKEN_finger', 'TOKEN_on', 'TOKEN_a', 'TOKEN_,', 'TOKEN_on', 'TOKEN_a', 'TOKEN_favorite', 'TOKEN_T', 'TOKEN_V', 'TOKEN_program', 'TOKEN_,', 'POS_UH', 'POS_,', 'POS_PRP', 'POS_BES', 'POS_RB', 'POS_RB', 'POS_JJ', 'POS_TO', 'POS_VB', 'POS_PRP$', 'POS_NN', 'POS_IN', 'POS_DT', 'POS_,', 'POS_IN', 'POS_DT', 'POS_JJ', 'POS_NN', 'POS_NN', 'POS_NN', 'POS_,']
token_bigrams = zip(list_token, list_token[1:])
print(token_bigrams)
for i in token_bigrams:
    #bigram = "/".join(i)
    print(i)
