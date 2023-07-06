class No():
    def __init__(self,carga:any):
        self.carga = carga
        self.esq = None
        self.dir = None

    def __str__(self):
        return str(self.carga)


class ArvoreBinaria():        
    def __init__(self):
        self.__raiz = None

    def estaVazia(self)->bool:
        return self.__raiz == None
    
    def getRaiz(self)->any:
        return self.__raiz.carga if self.__raiz is not None else None


    def preordem(self):
        self.__preordem(self.__raiz)

    def __preordem(self, no:No):
        if no is not None:
            print(f'{no.carga}',end=' ')
            self.__preordem(no.esq)
            self.__preordem(no.dir)

    def emordem(self):
        self.__emordem(self.__raiz)

    def __emordem(self, no):
        if no is not None:
            self.__emordem(no.esq)
            print(f'{no.carga}',end=' ')
            self.__emordem(no.dir)

    def posordem(self):
        self.__posordem(self.__raiz)

    def __posordem(self, no):
        if no is not None:
            self.__posordem(no.esq)
            self.__posordem(no.dir)
            print(f'{no.carga}',end=' ')

    
    def remove(self, chave:any)->any:
        carga = self.busca(chave)
        if carga is not None:
            self.__remove(chave, self.__raiz)
            return carga
        else:
            return None



   
    # Dado um nó de uma BST e uma chave busca, este método
    # deleta o nó que contém a chave e devolve o novo nó raiz
    def __remove(self, key:any, no:No):
        # Caso primário: não há raiz
        if no is None: 
            return no
  
        # Se a chave a ser deletada é menor do que a chave do nó raiz (da vez),
        # então a chave se encontra na subárvore esquerda
        if key < no.carga:
            no.esq = self.__remove(key, no.esq) 
  
        # Se a chave a ser deletada é maior do que a chave do nó raiz (da vez),
        # então a chave se encontra na subárvore esquerda
        elif(key > no.carga):
            no.dir = self.__remove(key, no.dir) 
  
        # Se a chave é igual à chave do nó raiz, então este é o nó 
        # a ser removido
        else:
            # (1) Nó com apenas 1 filho ou nenhum filho
            if no.esq is None : 
                temp = no.dir  
                no = None 
                return temp

            elif no.dir is None :
                temp = no.esq  
                no = None
                return temp 
  
            # (2) Nó com dois filhos: obtem o sucessor inorder
            # (o menor nó da subárvore direita) 
            temp = self.__minValueNode(no.dir) 
  
            # copia o conteúdo do sucessor inorder para este nós
            no.carga = temp.carga
  
            # Deletao sucessor inorder
            no.dir = self.__remove(temp.carga, no.dir )

        return no


    
    def add(self, carga:any)->bool:
        if(self.__raiz == None):
            self.__raiz = No(carga)
        else:
            self.__add(carga,self.__raiz)   

    def __add(self, carga, no):
        if ( carga < no.carga):
            if( no.esq != None):
                self.__add(carga, no.esq)
            else:
                no.esq = No(carga)
        else:
            if( no.dir != None):
                self.__add(carga, no.dir)
            else:
                no.dir = No(carga)


    def __count(self, no:'No')->int:
        if no is None:
            return 0
        else:
            return 1 + self.__count(no.esq) + self.__count(no.dir)

    def __len__(self):
        return self.__count(self.__raiz)

    def busca(self, chave:any)->any:
        if( self.__raiz != None ):
            node = self.__busca(chave, self.__raiz)
            return node.carga if node is not None else None
        else:
            return None
    
    def __busca(self, chave:any, no:No):
        if ( chave == no.carga):
            return no
        elif ( chave < no.carga and no.esq != None):
            return self.__busca( chave, no.esq)
        elif ( chave > no.carga and no.dir != None):
            return self.__busca( chave, no.dir)
        else:
            return None
        # Dada uma BST não vazia, retorna o nó
    # com a menor chave encontrada na árvore. Note que a árvore
    # inteira não precisa ser percorrida
    def __minValueNode(self, no:'No')->'No':
        current = no 
  
        # loop para baixo a fim de encontrar a folha mais a esquerda
        while(current.esq is not None): 
            current = current.esq  
  
        return current

    # Dada uma BST não vazia, retorna o nó
    # com o maior valor de chave encontrada na árvore. Note que a árvore
    # inteira não precisa ser percorrida 
    # def __maxValueNode(self, node:'Node')->'Node':
    #     current = node 
  
    #      # loop para baixo a fim de encontrar a folha mais a direita
    #     while(current.rightChild is not None): 
    #         current = current.rightChild
  
    #     return current
        

    