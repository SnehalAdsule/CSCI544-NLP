import csv
import os
import sys


train_file='test.csv'
rank, song,artist,year,lyrics, source, label=[],[],[],[],[],[],[]
with open(train_file, "r") as file:
    data = file.read()
    lines = data.split('\n')

    count = 0
    for line in lines:
        row=line.split(',')
        if len(row)>1:
            rank.append(row[0])
            song.append(row[1])
            artist.append(row[2])
            year.append(row[3])
            lyrics.append(row[4])
            source.append(row[5])
            label.append(row[6])
