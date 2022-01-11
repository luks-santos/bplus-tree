from Node import Node

class BplusTree:
    def __init__(self, order) -> None:
        self.root = Node(order)
        self.root.leaf = True
    
    def insert(self, key):
        node = self.search(key)
        node.insert_key_leaf(key)
        print(node.keys)
        
        if(len(node.keys) == (node.order*2)):
            node1 = node.split_node()
            self.insert_parent(node, node1.keys[0], node1)

        print(self.root.keys)

    def search(self, key):
        node1 = self.root
        while(not node1.leaf):
            temp = node1.keys
            for i in range(len(temp)):     
                if (key == temp[i]):
                    node1 = node1.children[i + 1]
                    break
                elif (key < temp[i]):
                    node1 = node1.children[i]
                    break
                elif (i + 1 == len(node1.keys)):
                    node1 = node1.children[i + 1]
                    break
        return node1
    
    def insert_parent(self, leftnode, key, rightnode):
        if(self.root == leftnode):
            rootNode = Node(leftnode.order)
            rootNode.keys = [key]
            rootNode.children = [leftnode, rightnode]
            print('rootNode:', rootNode.keys)
            print(rootNode.children[0].keys)
            print(rootNode.children[1].keys)
            self.root = rootNode
            leftnode.parent = rootNode
            rightnode.parent = rootNode
            return
    
        parentLeft = leftnode.parent
        temp = parentLeft.children
        for i in range(len(temp)):
            if (temp[i] == leftnode):
                parentLeft.keys = parentLeft.keys[:i] + [key] + parentLeft.keys[i:]
                parentLeft.children = parentLeft.children[:i + 1] + [rightnode] + parentLeft.children[i + 1:]
            if (len(parentLeft.keys) == parentLeft.order * 2):
                parentRight = Node(parentLeft.order)
                parentRight.parent = parentLeft.parent
                mid = parentLeft.order
                parentRight.keys = parentLeft.keys[mid + 1:]
                parentRight.children = parentLeft.children[mid + 1:]
                value = parentLeft.keys[mid]
                
                parentLeft.keys = parentLeft.keys[:mid]
                parentLeft.children = parentLeft.children[:mid + 1]
                print("direita:")
                print(parentRight.keys)
                print("esquerda:")
                print(parentLeft.keys)

                for j in parentLeft.children:
                    print("filho esquerda")
                    print(j.keys)
                    j.parent = parentLeft
                for j in parentRight.children:
                    print("filho direita")
                    print(j.keys)
                    j.parent = parentRight
                self.insert_parent(parentLeft, value, parentRight)

    def print_tree(self):
        if not self.root:
            return None
        
        node = self.root
        while not node.leaf:
            node = node.children[0]

        while node:
            print('{}'.format(node.keys), end=' -> ')
            node = node.nextKey

def printTree(tree):
    lst = [tree.root]
    level = [0]
    leaf = None
    flag = 0
    lev_leaf = 0

  
    while (len(lst) != 0):
        x = lst.pop(0)
        lev = level.pop(0)
        if (x.leaf == False):
            for i, item in enumerate(x.children):
                print(item.keys)
        else:
            for i, item in enumerate(x.keys):
                print(item.values)
            if (flag == 0):
                lev_leaf = lev
                leaf = x
                flag = 1