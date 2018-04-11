from collections import OrderedDict
from progressBar import ProgressBar
from log import Log

ENABLE_LOG = False
logs = Log(ENABLE_LOG)

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
    def search(self, target, record):
        logs.log("\tenter",self.address)
        chrod_size = self.parent_chord.SIZE

        # record now
        record.append(self.address)

#  debug
        if (len(record) > 32): 
            logs.debug(">>> not good at find [", target, "]")
            logs.debug(record)
            return None, None
#  end debug

        # check match
        logs.debug("[self]", end=" ")        
        if self.at_cover_range(target):
            return self.address, record

        # target file is in finger table
        for address in self.finger_table.values():
            if address == target:
                return address, record  

        # search next node form finger table
        previous_address = None
        for key, address in self.finger_table.items():
            if previous_address is not None:
                A = address
                B = previous_address

                # check 
                logs.debug("[fing]", end=" ")
                if at_range(A, B, target):
                    the_node = self.get_node(B) 
                    return the_node.search(target, record)

            previous_address = address

        # it mean last one
        the_node =  self.get_node(previous_address)
        return the_node.search(target, record)

    def at_cover_range(self, target):    
        now  = self.address
        next = self.successor.address
        return at_range(next, now, target)

    # use address, return the node
    def get_node(self, address=0):
        return self.parent_chord.chord[address]


def at_range(A, B, target):
    logs.log("is {} in {} to {}?".format(target, A, B), end='')
    if A > B:
        if B <= target and target < A:
            logs.log("YES")                
            return True
    elif B > A:
        if A > target or target >= B:
            logs.log("YES")    
            return True

    logs.log("NO")
    return False

if __name__ == "__main__":
    LOG_SWITCH = True
    log = Log(LOG_SWITCH)

    nodes = [1, 8, 14, 21, 32, 38, 42, 48, 51, 56]
    
    c = Chord(nodes, 2**6)

    for key, node in c.chord.items():
        print("[ node", node, " ]")
        print("finger_table\n\t", node.finger_table)

        target = 54
        print("find", target, ">> ")
        n, record = node.search(target, [])
        print("\tnode:", n, " record:", record)

        print("----------")