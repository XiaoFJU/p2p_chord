import os
import sys
import operator
from random import randint
from math import log

import chord
import myRandom
from log import Log
from progressBar import ProgressBar


# static value
RANDOM_FILE = 'random.txt'
ID_SIZE = 2**32
NODE_NUMBER = 10000
ENABLE_LOG = False

# RANDOM_FILE = '100.txt'
# ID_SIZE = 2**10
# NODE_NUMBER = 100

if __name__ == "__main__":
    logs = Log(ENABLE_LOG)

    # if file not exist, create it.
    nodes = myRandom.random_file(RANDOM_FILE, ID_SIZE, NODE_NUMBER)
    # get file sha1 to check the random data same
    comment = "sha1sum " + RANDOM_FILE
    sha1sum = os.popen(comment).readline().replace('\n', '')

    # assume we already have all nodes at first time
    chord = chord.Chord(nodes, ID_SIZE)

    for i in sorted(nodes):
        print(i, end='')

    #################################
    # Q1: 每一個節點所需負責之key值個數  #
    #################################
    print("\n===========Q1=============")

    count = dict()

    # no matter what node start, get same answer
    node_index = nodes[randint(0, NODE_NUMBER-1)]
    node = chord.chord[node_index]
    print("start node:", node)
    for i in range(1, 11):
        file_count = i*10 * NODE_NUMBER
        print("numK:", file_count)
        bar = ProgressBar(total=file_count)

        # clear count
        for j in nodes:
            count[j] = 0

        for _ in range(file_count):
            file_key = randint(0, ID_SIZE-1)
            addr, record = node.search(file_key, list())

            logs.debug(node, "find", file_key, ">> ")
            logs.debug("\tnode:", addr, " record:", record)

            # use random list `nodes` mapping
            count[addr] += 1

            bar.log()

        # cacalculate ans
        ans = sorted(count.items(), key=operator.itemgetter(1))

        max = ans[0][1]
        mid = ans[NODE_NUMBER//2][1]
        min = ans[NODE_NUMBER-1][1]

        print(max, mid, min)

    #######################
    # Q2: 搜尋時所需之hop數  #
    #######################
    print("\n===========Q2=============")

    hops = [0] * int(log(ID_SIZE, 2))

    bar = ProgressBar(total=100*NODE_NUMBER)
    for i in nodes:
        node = chord.chord[i]
        for j in range(100):
            k = randint(0, ID_SIZE-1)
            addr, record = node.search(k, [])

            hops_num = len(record)-1
            hops[hops_num] += 1

            bar.log()

    print(hops)
    print([x/(100*NODE_NUMBER) for x in hops])
