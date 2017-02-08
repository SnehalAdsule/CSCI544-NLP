try:
    import pycrfsuite
except:
    print ('not able to load pycrfsuite')
from collections import namedtuple
import csv
import glob
import os
import ntpath
import sys


def get_utterances_from_file(dialog_csv_file):
    """Returns a list of DialogUtterances from an open file."""
    reader = csv.DictReader(dialog_csv_file)
    return [_dict_to_dialog_utterance(du_dict) for du_dict in reader]

def get_utterances_from_filename(dialog_csv_filename):
    """Returns a list of DialogUtterances from an unopened filename."""
    with open(dialog_csv_filename, "r") as dialog_csv_file:
        return get_utterances_from_file(dialog_csv_file)

def get_data(data_dir):
    """Generates lists of utterances from each dialog file.

    To get a list of all dialogs call list(get_data(data_dir)).
    data_dir - a dir with csv files containing dialogs"""
    dialog_filenames = sorted(glob.glob(os.path.join(data_dir, "*.csv")))
    for dialog_filename in dialog_filenames:
        yield get_utterances_from_filename(dialog_filename)
def get_data2(data_dir):
    """Generates lists of utterances from each dialog file.

    To get a list of all dialogs call list(get_data(data_dir)).
    data_dir - a dir with csv files containing dialogs"""
    dialog_filenames = sorted(glob.glob(os.path.join(data_dir, "*.csv")))
    for dialog_filename in dialog_filenames:
        yield dialog_filename, get_utterances_from_filename(dialog_filename)

DialogUtterance = namedtuple("DialogUtterance", ("act_tag", "speaker", "pos", "text"))

PosTag = namedtuple("PosTag", ("token", "pos"))

def _dict_to_dialog_utterance(du_dict):
    """Private method for converting a dict to a DialogUtterance."""

    # Remove anything with
    for k, v in du_dict.items():
        if len(v.strip()) == 0:
            du_dict[k] = None

    # Extract tokens and POS tags
    if du_dict["pos"]:
        du_dict["pos"] = [
            PosTag(*token_pos_pair.split("/"))
            for token_pos_pair in du_dict["pos"].split()]
    return DialogUtterance(**du_dict)



train_data=list(get_data(sys.argv[1]))
val_data=list(get_data2(sys.argv[2]))


features=[]
labels=[]

x_labels=[]
x_val_labels=[]
x_train_token=[]
x_val_token=[]
filelist=[]


for val in train_data:
    prev_speaker = ''
    curr_speaker = ''
    count = 0
    list_token = []
    list_label = []

    for item in val:
        toklist = []
        poslist = []
        features_list=[]
        curr_speaker=getattr(item, "speaker")

        if count==0:
            features_list.append("9")
        if count>0:
            if prev_speaker!=curr_speaker:
                features_list.append("1")
            else:
                features_list.append("0")

        items=getattr(item, "pos")
        if items is not None:
            for x in items:
                features_list.append("TOKEN_"+getattr(x, "token"))
                toklist.append(getattr(x, "token"))

            token_bigrams = zip(toklist, toklist[1:])
            for i in token_bigrams:
                bigram = "/".join(i)
                features_list.append("TOKEN_" + bigram)
            token_trigrams = zip(toklist, toklist[1:], toklist[2:])
            for i in token_trigrams:
                trigram = "/".join(i)
                features_list.append("TOKEN_" + trigram)

            for x in items:
                features_list.append("POS_"+getattr(x, "pos"))
                poslist.append(getattr(x, "pos"))
            pos_bigrams = zip(poslist, poslist[1:])
            for i in pos_bigrams:
                bigram = "/".join(i)
                features_list.append("POS_" + bigram)

            pos_trigrams = zip(poslist, poslist[1:], poslist[2:])
            for i in pos_trigrams:
                trigram = "/".join(i)
                features_list.append("POS_" + trigram)

        list_label.append(getattr(item, "act_tag"))
        list_token.append(features_list)

        prev_speaker = curr_speaker
    x_train_token.append(list_token)
    x_labels.append(list_label)

trainer=pycrfsuite.Trainer(verbose=False)

for x, y in zip(x_train_token, x_labels):
    trainer.append(x, y)

trainer.set_params({
    'c1': 1.0,   # coefficient for L1 penalty
    'c2': 1e-3,  # coefficient for L2 penalty
    'max_iterations': 75,  # stop earlier

    # include transitions that are possible, but not observed
    'feature.possible_transitions': True
})

trainer.train('advanced.crfsuite')

for val in val_data:
    prev_speaker = ''
    curr_speaker = ''
    count = 0
    list_token = []
    list_label = []

    for item in val[1]:
        toklist = []
        poslist = []

        features_list = []
        curr_speaker = getattr(item, "speaker")

        if count == 0:
            features_list.append("9")
        if count > 0:
            if prev_speaker != curr_speaker:
                features_list.append("1")
            else:
                features_list.append("0")

        items = getattr(item, "pos")
        if items is not None:
            for x in items:
                features_list.append("TOKEN_" + getattr(x, "token"))
                toklist.append(getattr(x, "token"))

            token_bigrams = zip(toklist, toklist[1:])
            for i in token_bigrams:
                bigram = "/".join(i)
                features_list.append("TOKEN_" + bigram)
            token_trigrams = zip(toklist, toklist[1:], toklist[2:])
            for i in token_trigrams:
                trigram = "/".join(i)
                features_list.append("TOKEN_" + trigram)

            for x in items:
                features_list.append("POS_" + getattr(x, "pos"))
                poslist.append(getattr(x, "pos"))
            pos_bigrams = zip(poslist, poslist[1:])
            for i in pos_bigrams:
                bigram = "/".join(i)
                features_list.append("POS_" + bigram)

            pos_trigrams = zip(poslist, poslist[1:], poslist[2:])
            for i in pos_trigrams:
                trigram = "/".join(i)
                features_list.append("POS_" + trigram)

        list_label.append(getattr(item, "act_tag"))
        list_token.append(features_list)
        count += 1
        prev_speaker = curr_speaker
    x_val_token.append(list_token)
    x_val_labels.append(list_label)
    filelist.append(val[0])

tagger = pycrfsuite.Tagger()
tagger.open('advanced.crfsuite')

f = open(sys.argv[3], 'w')
for i in range(len(x_val_token)):
    f.write('Filename="' + ntpath.basename(filelist[i])+'"\n')
    pred=tagger.tag(x_val_token[i])
    for j in range(len(pred)):
        f.write(pred[j]+'\n')
    f.write('\n')
f.close()