import os.path
from random import randint


def random_file(fileName, IdSize, nodeNumber):
    nodeList = list()
    while True:
        # clear list
        del nodeList[:]

        if os.path.isfile(fileName):
            if file_len(fileName) == nodeNumber:
                # file already exist, and its number of line is true
                with open(fileName) as f:
                    for num in f:
                        nodeList.append(int(num))
                f.close()
                return nodeList

        # enter, file is not exist or is not correct
        while len(nodeList) < nodeNumber:
            n = randint(0, IdSize-1)
            if n not in nodeList:
                nodeList.append(n)
            # else:
                # number repeated, ignore the num (just do noting)

        f = open(fileName, 'a')
        for i in range(nodeNumber):
            f.write(str(nodeList[i]) + "\n")
        f.close()
        return nodeList


def file_len(fname):
    i = 0
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
