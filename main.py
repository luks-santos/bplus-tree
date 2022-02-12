from BplusTree import BplusTree

arvore = BplusTree(4)
while(True):  
    print("RAIZ: ", arvore.root.keys)          
    print("\n1 - Inserir valor na Árvore")
    print("2 - Remover valor na Árvore")
    print("3 - Buscar valor na Árvore")
    print("4 - Buscar valor por intervalo na Árvore")
    print("5 - Mostrar B+")
    print("0 - sair")
    n = int(input("Digite uma opção: "))
    if n == 1:
        #key = int(input("Digite o valor para ser inserido: "))
       # key = int(input("informe uma chave: "))
        #vv = [7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 30, 40, 50, 51, 52, 53, 54,20,21,22]
        vv = [7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,21,22,23,24,25,26,6,5,4]
       #remove 14
        for i in vv:
            arvore.insert(i, [i, 0])
    elif n == 2:
        numero = int(input("Digite o valor para ser removido: "))
        arvore.delete(numero)
    elif n == 3:
        #numero = int(input("Digite o valor para ser buscado: "))
        key = int(input("Digite o valor para ser inserido: "))
        arvore.insert(key, [key, 0])
    elif  n== 4:
        numero1 = int (input("Digite o primeiro valor para ser buscado: "))
        numero2 = int (input("Digite o segundo valor para ser buscado: "))
    elif  n== 5:
        arvore.print_tree()
    else:
        break
