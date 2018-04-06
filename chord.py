from collections import OrderedDict
from progressBar import ProgressBar

class Chord:
    def __init__(self, int_nodeList, ID_SIZE):
        print("init chord...")
        bar = ProgressBar(total = len(int_nodeList))

        self.node_list = sorted(int_nodeList)

        #create Node object
        self.chord = OrderedDict()
        for num in self.node_list:
            self.chord[num] = Node(num, self) 
            bar.log()

        print("done.")

        self.total = len(self.chord)
        
        # size of chord
        self.SIZE = ID_SIZE

        self.set_neighbor()
        self.creat_finger_table()

    # find predecessor and successor
    def set_neighbor(self):
        print("set neighbor...")
        bar = ProgressBar(total = self.total)

        first = None
        previous = None
        for _, now in self.chord.items():
            # save first node address
            if first == None:
                first = now
            elif previous != None:
                # set the previous of now Node
                now.predecessor = previous
                # set the next of previous Node 
                previous.successor = now
            previous = now
            bar.log()

        # next of last node is first node 
        previous.successor = first 
        # pre of first node is last node
        first.predecessor = previous 
        print("done.")

    def creat_finger_table(self):
        print("creat_finger_table...")
        bar = ProgressBar(total = self.total)

        # finger list is like [1, 2, 4, 8...]
        finger = list()
        i = 1
        while i < self.SIZE/2 + 1:
            finger.append(i)
            i *= 2

### 可能需要想想別的 ###
        for _, now in self.chord.items():
            for i in finger:
                target = (i + now.address) % self.SIZE

                finded_flag = False
                first_address = None
                for _, node in self.chord.items():
                    if first_address is None:
                        first_address = node.address
                    if node.address >= target and node.address is not now.address :
                        now.finger_table[i] = node.address
                        finded_flag = True
                        break
                if not finded_flag:
                    now.finger_table[i] = first_address
            bar.log()
#####################

class Node:
    def __init__(self, address, chord):
        self.address = address
        self.parent_chord = chord

        self.successor = None
        self.predecessor = None
        self.finger_table = dict()
        self.fileList = []

    def __str__(self):
        return str(self.address)

    # return a address of the node which manage the file
    def search(self, target, record=[]):
        # record hop
        record.append(self.address)

# debug
        if (len(record) > 30): 
            print(">>> not good at find [", target, "]")
            print(record)
            return None, None
# end debug

        size = self.parent_chord.SIZE
        # if at self cover range...
        predecessor_address = self.predecessor.address
        if self.address > predecessor_address:
            # check range
            if self.address >= target and target > predecessor_address:
                return self.address, record
        else:
            if self.address+size >= target+size and target+size > predecessor_address:
                return self.address, record   

        # target file is in finger table
        for address in self.finger_table.values():
            if address == target:
                return address, record 

        # check next 
        successor_address = self.successor.address
        
        if  self.address > successor_address:
            # it mean carry
            successor_address += size
        if successor_address > target:
            # print( "at {}, {} > {}".format(self.address,successor_address,target) )
            successor_address %= size
            record.append(successor_address)
            return successor_address, record

        # search finger table and find which none we should start from 
        previous_address = None
        for key, address in self.finger_table.items():
            # recover, (42+16)%64 => 42+16
            if self.address > address:
                address += size

            if address > target:
                # continue to query next node
                if previous_address is None:
                    previous_address = address % size
                n = self.get_node(previous_address)
                return n.search(target, record)
            previous_address = address % size

        # it mean last one 
        n = self.get_node(previous_address)
        return n.search(target, record)

### 我忘記這個幹麻的了
    # find target from "the node"
    def find(self, target, from_address):
        chord_list = self.parent_chord
        
        index_of = lambda ordered_dict, key: list(ordered_dict).index(key) 
        now_index = index_of(chord_list, from_address)
        # find which node should provide the file (the node is less then)
###

    # use address, return the node
    def get_node(self, address=0):
        return self.parent_chord.chord[address]


if __name__ == "__main__":
    nodes = [1, 42, 8, 14, 48, 21, 32, 51, 38, 34, 59]
    
    c = Chord(nodes, 2**6)

    # for key, node in c.chord.items():
    #     print("[ node", node, " ]")
    #     print("finger_table\n\t", node.finger_table)

    #     target = 54
    #     print("find", target, ">> ")
    #     n, record = node.search(target, [])
    #     print("\tnode:", n, " record:", record)

    #     print("----------")

    # from random import randint
    
    # ls = [0]*len(nodes)
    # for i in range(10000):
    #     k = randint(0, 2**6)
    #     n, record = c.chord.items.search(k, [])
    #     ls[ nodes.index(n) ]