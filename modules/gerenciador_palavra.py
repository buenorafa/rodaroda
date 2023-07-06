from modules.word import Word as Palavra
from modules.lista_encadeada import Lista
from modules.arvore_binaria_busca import ArvoreBinaria
import random

class Gerenciador():
    def __init__(self, caminho: str) -> None:
        self.caminho = caminho

    def carregar_palavras(self) -> list:
        caminho_do_arquivo = self.caminho
        lista_de_palavras = Lista()
        with open(caminho_do_arquivo, 'r') as arquivo:
            for linha in arquivo:
                palavra, dica, categoria = linha.strip().split(';')
                lista_de_palavras.append(Palavra(palavra, dica, categoria))
        return lista_de_palavras

    def inserir_palavras(self):
        caminho_do_arquivo = self.caminho
        abb = ArvoreBinaria()

        try:
            with open(caminho_do_arquivo, 'a+') as arquivo:
                arquivo.seek(0)
                for linha in arquivo:
                    palavra, _, _ = linha.strip().split(';')
                    abb.add(palavra)

                while True:
                    palavra = input("Informe a palavra: ")
                    while not palavra or not palavra.isalpha():
                        print("A entrada não pode ser vazia ou conter caracteres não alfabéticos. Tente novamente.")
                        palavra = input("Informe a palavra: ")

                    dica = input("Informe a dica: ")
                    while not dica or not dica.isalpha():
                        print("A entrada não pode ser vazia ou conter caracteres não alfabéticos. Tente novamente.")
                        dica = input("Informe a dica: ")

                    categoria = input("Informe a categoria: ")
                    while not categoria or not categoria.isalpha():
                        print("A entrada não pode ser vazia ou conter caracteres não alfabéticos. Tente novamente.")
                        categoria = input("Informe a categoria: ")

                    nova_linha = f'{palavra};{dica};{categoria}'

                    if not abb.busca(palavra):
                        arquivo.write('\n')
                        arquivo.write(nova_linha + '\n')
                        abb.add(palavra)
                        print("A linha foi inserida com sucesso.")
                    else:
                        print("A palavra já existe no arquivo.")
                    op = input('Deseja adicionar uma nova palavra? (S/N)').lower()
                    if op == "s":
                        continue
                    else:
                        break
        except FileNotFoundError:
            print(f"O arquivo {caminho_do_arquivo} não foi encontrado.")
        except Exception as e:
            print(f"Ocorreu um erro ao tentar inserir uma nova palavra: {e}")

    def escolher_palavra_aleatoria(self, lista_de_palavras: Lista) -> Palavra:
        indice_aleatorio = random.randint(1, len(lista_de_palavras))
        return lista_de_palavras.elemento(indice_aleatorio)

    def escolher_palavra_aleatoria_por_categoria(self, categoria: str, lista_de_palavras: Lista) -> str:
        palavras_da_categoria = Lista()

        cursor = lista_de_palavras.head
        while cursor is not None:
            if cursor.carga.categoria == categoria:
                palavras_da_categoria.append(cursor.carga)
            cursor = cursor.prox

        if palavras_da_categoria.tamanho() == 0:
            raise Exception(f'Nenhuma palavra encontrada para a categoria "{categoria}"')

        indice_aleatorio = random.randint(1, palavras_da_categoria.tamanho())
        return palavras_da_categoria.elemento(indice_aleatorio)
