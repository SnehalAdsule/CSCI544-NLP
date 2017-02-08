import random
import numpy as np
a=[1,2,3,4,5]
y=a[:]
for i in range(0,20):
    random.shuffle(a)
    print a