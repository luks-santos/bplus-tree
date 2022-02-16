from Node import Node
from math import floor,ceil
import sys

#depois conferir ordem para impar com o floor
#tratar caso chave repetida
class BplusTree:
    def __init__(self, lenPag, qtdReg ) -> None:
        self.orderNode, self.orderParent  = self.calc_order(lenPag, qtdReg)
        self.root = Node(self.orderNode)
        self.root.is_leaf = True
    

    def calc_order(self,lenPage, numReg): 
        return lenPage, numReg
        vet = [1]*numReg
        print("vetor: " , vet)
        registro = sys.getsizeof(vet) # Para um registro de 5 campos cada um terá 120 bytes
        orderLeaf = (lenPage//registro)
        print("order_folha: ", orderLeaf)
        print("order_not_folha: ", lenPage//sys.getsizeof(1))
        return (orderLeaf, lenPage//sys.getsizeof(1))

    def insert(self, key, record):
        node = self.__search(key)
        if (node):
            if (len(node.keys) == (node.get_order())):
                node_right = node.split_node(key, record)
                if (node_right):
                    self.__insert_parent(node, node_right.keys[0][0], node_right)
            else:
                node.insert_key_leaf(key, record)

    def __search(self, key):
        node_ = self.root
        while(not node_.is_leaf):
            temp = node_.keys
            for i in range(len(temp)):     
                if (key == temp[i]):
                    node_ = node_.children[i + 1]
                    break
                elif (key < temp[i]):
                    node_ = node_.children[i]
                    break
                elif (i + 1 == len(node_.keys)):
                    node_ = node_.children[i + 1]
                    break
        return node_

    def search_key(self,key):
        node_ = self.__search(key)
        temp = node_.keys
        for i in range(len(temp)):     
            if (key == temp[i][0]):
                print("Chave buscada: ", key)
                print("Nó da chave: ", node_.keys)
                return
        print("Chave não encontrada")


    def __insert_parent(self, node_left, key, node_right):
        if (self.root == node_left):
            node_root = Node(self.orderParent)
            node_root.keys = [key]
            node_root.children = [node_left, node_right]
            print('node_root:', node_root.keys)
            print('Filho esquerda raiz:', node_root.children[0].keys)
            print('Filho direita raiz:', node_root.children[1].keys)
            self.root = node_root
            node_left.parent = node_root
            node_right.parent = node_root
        else:
            parent_left = node_left.parent
            temp = parent_left.children
            for i in range(len(temp)):
                if (temp[i] == node_left and len(parent_left.keys) == (self.root.order)):
                    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                    parent_right = Node(self.orderParent)
                    parent_right.parent = parent_left.parent
                    mid = ceil(parent_left.order/2)
                    
                    parent_left.keys = parent_left.keys[:i] + [key] + parent_left.keys[i:]
                    parent_left.children = parent_left.children[:i + 1] + [node_right] + parent_left.children[i + 1:]
                    print('KEYS P ESQUERDA:', parent_left.keys)
                    print('FILHOS ESQUERDA: ')
                    for k in parent_left.children:
                        print(k.keys)

                    value = parent_left.keys[mid]

                    parent_right.keys = parent_left.keys[mid + 1:]
                    parent_right.children = parent_left.children[mid + 1:]
                    print('KEYS P DIREITA:',  parent_right.keys)
                    print('FILHOS DIREITA: ')
                    for k in parent_right.children:
                        print(k.keys)

                    parent_left.keys = parent_left.keys[:mid] 
                    parent_left.children = parent_left.children[:mid + 1]
                    print('KEYS P ESQUERDA:', parent_left.keys)
                    print('FILHOS ESQUERDA: ')
                    for k in parent_left.children:
                        print(k.keys)

                    for j in parent_left.children:
                        j.parent = parent_left
                    for j in parent_right.children:
                        j.parent = parent_right

                    self.__insert_parent(parent_left, value, parent_right)
                    print("++++++++++++++++++++++++++++++++++++++++++++++++")
                    break
                elif (temp[i] == node_left):
                    parent_left.keys = parent_left.keys[:i] + [key] + parent_left.keys[i:]
                    parent_left.children = parent_left.children[:i + 1] + [node_right] + parent_left.children[i + 1:]
                    print("Subi uma chave para raiz ficou com", len(parent_left.keys), "chaves")
                    break
    
    #Há mudanças nas chaves do pai, páginas não folha, somente quando pego emprestado, ou quando tem fusão 
    def delete(self, key):
        node = self.__search(key)
        print("1 - node no delete : " , node.keys)
        #caso 0 - Só tem chaves na raiz, ainda não houve divisão
        if(node == self.root):
            node.delete_key(key)
            print("é raiz")

        #caso 1 - Tem quantidade mínima para remoção 
        elif(len(node.keys) > floor(node.get_order()/2)):
            node.delete_key(key)

        else:
            self.delete_aux(node, key)


    def delete_aux(self, node, key):
        #caso 2 - Não tem quantidade mínima para remoção
        if (len(node.keys) == floor(node.get_order()/2)):
            #caso 2.a
            neighbor_left = node.previous_key
            if (neighbor_left and neighbor_left.parent == node.parent and len(neighbor_left.keys) > floor(node.get_order()/2)):
                neighbor_left.lend(node, 0)
                node.delete_key(key)
                for i in range(len(node.parent.keys)):
                    print( "i: ", node.parent.keys)
                    if(node.keys[0][0] <= node.parent.keys[i]):
                        node.parent.keys[i] = node.keys[0][0]
                        break
                print("3 - MUDANÇAS: " , node.parent.keys)
                print('3 - node:', node.keys)
                print('3- irmão esquerda:', neighbor_left.keys)
                return
            else:
                #caso 2.b
                neighbor_right = node.next_key
                if (neighbor_right and neighbor_right.parent == node.parent and len(neighbor_right.keys) > floor(node.get_order()/2)):
                    neighbor_right.lend(node, 1)
                    node.delete_key(key)
                    for i in range(len(node.parent.keys)-1, -1, -1):
                        print( "i: ", node.parent.keys)
                        print( "if: ", node.keys[0][0], " - ", node.parent.keys[i])
                        if (neighbor_right.keys[0][0] >= node.parent.keys[i]):
                            node.parent.keys[i] = neighbor_right.keys[0][0]
                            break
                    print("mudanças: " , node.parent.keys)
                    print('3 - node:', node.keys)
                    print('3- irmão direita:', neighbor_right.keys)
                else: 
                    #caso 3
                    node_merge = None
                    index = -1
                    if (neighbor_left and neighbor_left.parent == node.parent):
                        print('4 - FUSÃOOOOOOOO')
                        print("4 - chegou no irmão esquerda!")
                        node.delete_key(key)
                        index = node.parent.children.index(node)
                        node_merge = neighbor_left.merge(node)

                    elif (neighbor_right and neighbor_right.parent == node.parent):
                        print('4 - FUSÃOOOOOOOO')
                        print("chegou no irmão na direita!")
                        node.delete_key(key)
                        index = node.parent.children.index(node)
                        node_merge = node.merge(neighbor_right)
                    
                    del node
                    parent_node = node_merge.parent

                    if (parent_node == self.root and len(self.root.keys) == 1):
                        parent_node = None
                        self.root = node_merge
                        del node_merge
                        return

                    if (index > 0 and index < len(parent_node.keys)):
                        print('ENTREI NO CASO 1 DA FUSÃO')
                        parent_node.children.pop(index)
                        parent_node.keys.pop(index - 1)

                    elif (index == 0):
                        print('ENTREI NO CASO 2 DA FUSÃO')
                        parent_node.children.pop(index + 1)
                        parent_node.keys.pop(index)
                    
                    else:
                        print('ENTREI NO CASO 3 DA FUSÃO')
                        parent_node.children.pop(-1)
                        parent_node.keys.pop(-1)

                    if (parent_node != self.root and len(parent_node.keys) < int(floor(parent_node.get_order()/2))):
                        print("cheguei aqui?")
                        self.modify_parent(parent_node)
    
    def modify_parent(self, node): #Vai ser usado quando precisar reorganizar os pais do nó quando ficar abaixo da ordem mínima
     
        parent_node = node.parent
        neighbor_left = neighbor_right = None    
        index = parent_node.children.index(node)

        if(index != 0 or len(node.parent.keys) == index):
            neighbor_left = node.parent.children[index - 1]
            if(len(neighbor_left.keys) > floor(neighbor_left.get_order()/2)):
                print("cheguei na rotação pela esquerda")
                print("chaves do no: ", node.parent.children[index].keys)
                #conferir isso
                node.parent.rotate_keys(neighbor_left, node, index - 1, 0)
                return
                
        elif(index == 0 or index < len(node.parent.keys)): 
            neighbor_right = node.parent.children[index + 1]
            if(len(neighbor_right.keys) > floor(neighbor_right.get_order()/2)):
                node.parent.rotate_keys(node, neighbor_right, index + 1, 1)
                return
        
        if(neighbor_left):
            print('Fusão esquerda em nó não folha')
            print('index ', index)
            print('PARENT NODE', parent_node.keys)
            key = parent_node.keys.pop(index - 1)
            neighbor_left.insert_key(key)
            neighbor_left.keys += node.keys
            neighbor_left.children += node.children
            
            for c in node.children:
                c.parent = neighbor_left
            
            parent_node.children.pop(index)

            node = neighbor_left
        
        elif(neighbor_right):
            print('Fusão direita em nó não folha')
            #pode ter erro aqui
            print('Fusão esquerda em nó não folha')
            print('index ', index)
            print('PARENT NODE', parent_node.keys)
            print('NODE: ', node.keys)
            key = parent_node.keys.pop(index)
            node.insert_key(key)
            node.keys += neighbor_right.keys
            node.children += neighbor_right.children
            
            for c in neighbor_right.children:
                c.parent = node
            #conferir aqui
            parent_node.children.pop(index + 1)

        if len(parent_node.keys) == 0 and parent_node == self.root:
            print("TO AQQQQQQQQQQ DKDLJFKADMFD")
            self.root = node
        
        elif len(parent_node.keys) < floor(parent_node.get_order()/2) and parent_node != self.root:
            self.modify_parent(parent_node) 
    
    def print_node_leaf(self):
        if not self.root:
            return None
        
        node = self.root
        while not node.is_leaf:
            node = node.children[0]

        while node:
            print('{}'.format(node.keys), end=' -> ')
            node = node.next_key


    def print_tree(self):
        if (not len(self.root.keys)): 
            return

        delimiter = None
        queue = []

        queue.append(self.root)
        queue.append(delimiter)
        
        while (True):
            curr = queue.pop(0)
            if (curr != delimiter):
                if (curr.is_leaf):
                    print(curr.keys, end=' -> ')
                else:
                    print(curr.keys, end='    ')
                if (len(curr.children)):
                    for n in curr.children:
                        queue.append(n)
            else:
                print()
                if (not len(queue)):
                    break
                queue.append(delimiter) 
