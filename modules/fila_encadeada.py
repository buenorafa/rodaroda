class FilaException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class No:
    def __init__(self, elemento: any):
        self.__elemento = elemento
        self.__proximo = None

    @property
    def elemento(self) -> any:
        return self.__elemento

    @elemento.setter
    def elemento(self, elemento: any):
        self.__elemento = elemento

    @property
    def proximo(self) -> object:
        return self.__proximo

    @proximo.setter
    def proximo(self, proximo: object):
        self.__proximo = proximo

    def __str__(self) -> str:
        return str(self.__elemento)


class Fila:
    def __init__(self):
        self.__primeiro = None
        self.__ultimo = None
        self.__tamanho = 0

    @property
    def primeiro(self):
        if self.__primeiro is None:
            raise FilaException("A fila está vazia.")
        return self.__primeiro.elemento
    
    @property
    def ultimo(self):
        if self.__ultimo is None:
            raise FilaException("A fila está vazia.")
        return self.__ultimo.elemento


    def esta_vazia(self) -> bool:
        return self.__tamanho == 0

    def tamanho(self) -> int:
        return self.__tamanho
    
    def __len__(self) -> int:
        return self.__tamanho

    def elemento(self, posicao: int) -> any:
        if posicao < 1 or posicao > self.__tamanho:
            raise FilaException("Posição inválida.")
        no = self.__primeiro
        for i in range(posicao):
            if i == posicao - 1:
                return no.elemento
            no = no.proximo

    def busca(self, elemento: any) -> int:
        no = self.__primeiro
        posicao = 1
        while no:
            if no.elemento == elemento:
                return posicao
            else:
                no = no.proximo
                posicao += 1
        raise FilaException("Elemento não encontrado.")

    def modificar(self, posicao: int, novo_elemento: any):
        if posicao < 1 or posicao > self.__tamanho:
            raise FilaException("Posição inválida.")
        no = self.__primeiro
        for i in range(posicao):
            if i == posicao - 1:
                no.elemento = novo_elemento
            else:
                no = no.proximo

    def enfileirar(self, novo_elemento: any):
        enfileirado = No(novo_elemento)
        if not self.__primeiro:
            self.__primeiro = enfileirado
            self.__ultimo = enfileirado
        else:
            self.__ultimo.proximo = enfileirado
            self.__ultimo = enfileirado
        self.__tamanho += 1

    def desenfileirar(self) -> any:
        if self.esta_vazia():
            raise FilaException("A fila está vazia.")
        desenfileirado = self.__primeiro
        self.__primeiro = desenfileirado.proximo
        desenfileirado.proximo = None
        self.__tamanho -= 1
        return desenfileirado.elemento

    def __str__(self) -> str:
        if self.esta_vazia():
            raise FilaException("A fila está vazia")
        resultado = []
        elemento = self.__primeiro
        while elemento:
            resultado.append(str(elemento))
            elemento = elemento.proximo
        return f"Primeiro -> [ {' | '.join(resultado)} ] <- último."

    @classmethod
    def combina(cls, fres, f1, f2) -> object:
        while not f1.esta_vazia() or not f2.esta_vazia():
            if not f1.esta_vazia():
                fres.enfileirar(f1.desenfileirar())
            if not f2.esta_vazia():
                fres.enfileirar(f2.desenfileirar())

    @classmethod
    def combina2(cls, fres, f1, f2) -> object:
        for i in range(max(f1.tamanho(), f2.tamanho())):
            if not f1.esta_vazia():
                fres.enfileirar(f1.desenfileirar())
            if not f2.esta_vazia():
                fres.enfileirar(f2.desenfileirar())

    def inverte(self):
        fila_aux = Fila()
        for i in range(self.tamanho(), 0, -1):
            fila_aux.enfileirar(self.elemento(i))
        for i in range(fila_aux.tamanho()):
            self.desenfileirar()
            self.enfileirar(fila_aux.desenfileirar())
