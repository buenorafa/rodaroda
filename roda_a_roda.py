from utils.terminal_cleaner import terminal_cleaner
from modules.cliente_tcp import Client
from modules.server_tcp import Server
from multiprocessing import Process
from modules.gerenciador_palavra import Gerenciador
import modules.protocol

def main():
    print("\nBem-vindo(a)(e) ao RODA A RODA")
    while True:
        print("\nEscolha uma opção")
        print("(1) Iniciar um novo jogo")
        print("(2) Conectar a uma partida")
        print("(3) Adicionar uma nova palvra")
        option = input("Escolha uma opção: ")
        if option == "1" or option == "2" or option =="3":
            break
        else:
            print("Opção inválida. Tente novamente.")

    if option == "1":
        qnt_players = int(input("Informe a quantidade de jogadores: "))
        server = Server(qnt_players)
        server.start()


    elif option == "2":
        HOST = input("Informe o HOST: ")
        PORT = int(input("Informe a PORTA: "))
        client = Client(HOST, PORT)
        client.start()

    elif option == "3":
        gerenciador = Gerenciador("utils/words.txt")
        gerenciador.inserir_palavras()

    else:
        print("Opção inválida")
        input("Pressione Enter para continuar...")

if __name__ == "__main__":
    main()
