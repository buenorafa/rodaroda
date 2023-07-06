import socket
from modules import protocol
from threading import Lock
from prettytable import PrettyTable
from utils import terminal_cleaner

class Client():
    def __init__(self, HOST: str, PORT:int):
        self.name = None
        self.server = (HOST, PORT)
        self.MSG_LEN = 1024     # Message's max length
        self.lock = Lock()
        self.choosed_letters = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    # Método para receber msg do servidor
    def msg_receive(self):
        while True:
            new_msg = self.socket.recv(self.MSG_LEN).decode().split(":")
            if not self.treat_msg(new_msg):
                break


    # Método para tratar as mensagens recebidas pelo servidor
    def treat_msg(self, msg: str):
        # Recebe solicitação GET_NAME do nome do jogador
        if msg[0] == "GET_NAME":
            while True:
                try:
                    data = input("Nick: ")
                except EOFError:
                    print("Nenhuma entrada fornecida.")
                self.name = data

                # Responde ao GET_NAME enviando um PUT_NAME [ NOME ]
                msg_back = protocol.put_name(self.name)
                self.socket.send(msg_back.encode())

                # Aguarda a confirmação do servidor pelo SEND_CONF
                resp_server = self.socket.recv(self.MSG_LEN).decode().split(":")
                if resp_server[1] == "+FAIL":
                    continue
                if resp_server[1] == "+OK":
                    self.socket.send(protocol.send_conf("+OK").encode())
                    terminal_cleaner.terminal_cleaner()
                    print("===================")
                    print("RODA A RODA")
                    print("===================")
                    print(f"Jogador {self.name} adicionado com sucesso")

                # Retorna para o msg_receive e espera nova msg do servidor
                return True
        
        elif msg[0] == "BROADCAST":
            # Imprime e trata o ESTADO DO JOGO do lado do cliente
            if msg[1] == "STATUS":
                if msg[4]:
                    self.choosed_letters.append(msg[4][-1])
                print("==================================")
                print(f"Dica: {msg[2]}")
                print("Palavra Secreta:")
                print(msg[3])
                print(f"[ {msg[4]} ]")
                print(f"Turno: {msg[5]}")
                print(f"Valor da Roleta: {msg[6]}")
                print("==================================")
                self.socket.send(protocol.send_conf("+OK").encode())
                # Retorna para o msg_receive e espera nova msg do servidor
                return True
            
            # Imprime o ranking final do jogo e envia a confirmação para o servidor
            elif msg[1] == "SEND_RANKING":
                terminal_cleaner.terminal_cleaner()
                print("===================")
                print("RODA A RODA")
                print("===================")
                print("Ranking de Jogadores:")
                for i in range(2,len(msg)):
                    print(msg[i])
                self.socket.send(protocol.send_conf("+OK").encode())
                # Retorna para o msg_receive e espera nova msg do servidor
                return True
            
            # Confirma para o servidor que recebeu a mensagem de game over e para de ouvir no msg_receive, indo para o encerramento do cliente
            elif msg[1] == "GAME_OVER":
                print("===================")
                print("GAME OVER")
                print("===================")
                self.socket.send(protocol.send_conf("+OK").encode())
                return False
                       
            # Imprime todas as mensagens de broadcast genéricas
            terminal_cleaner.terminal_cleaner()
            print("===================")
            print("RODA A RODA")
            print("===================")
            for i in range(1, len(msg)):
                print(msg[i])
            self.socket.send(protocol.send_conf("+OK").encode())

            # Retorna para o msg_receive e espera nova msg do servidor
            return True
        
        # trata o turno do jogador
        elif msg[0] == "SEND_TURN":
            # chama o menu do jogo de acordo com os parâmetros iformados pelo servidor, vide doc do protocolo
            option = self.menu(msg[1])
            if option == "1":
                while True:
                    letter = input("Escolha a letra: ").lower()
                    if letter in self.choosed_letters or len(letter) != 1:
                        print(f"Letra inválida, tente novamente!")
                        continue
                    break
                # Envia a letra pelo SEND_LETTER e espera a confirmação do servidor pelo SENDO_CONF
                while True:
                    msg_back = protocol.send_letter(letter)
                    self.socket.send(msg_back.encode())
                    resp_server = self.socket.recv(self.MSG_LEN).decode().split(":")
                    if resp_server[1] == "+FAIL":
                        continue
                    if resp_server[1] == "+OK":
                        self.socket.send(protocol.send_conf("+OK").encode())
                        break

            else:
                # Envia a palavra pelo SEND_WORD e espera a confirmação do servidor pelo SENDO_CONF
                while True:
                    word = input("Escolha a palavra: ").lower()
                    msg_back = protocol.send_word(word)
                    self.socket.send(msg_back.encode())
                    resp_server = self.socket.recv(self.MSG_LEN).decode().split(":")
                    if resp_server[1] == "+FAIL":
                        continue
                    if resp_server[1] == "+OK":
                        self.socket.send(protocol.send_conf("+OK").encode())
                        break
            return True


    # Método do menu do jogo
    def menu(self, option):
        print("\n====================================")
        print(" Digite o número da opção desejada:")
        print("====================================\n")

        if option == "0":
            print("1 - Escolher letra")
            print("2 - Escolher palavra\n")
        else:
            print("1 - Escolher letra (Não disponível)")
            print("2 - Escolher palavra\n")

        while True:
            chosen_option = input('Digite a opção: ')
            if option == "0" and chosen_option in ["1", "2"] or option != "0" and chosen_option == "2":
                return chosen_option
            else:
                print('Opção inválida! Tente novamente!')


    def start(self):
        self.socket.connect(("localhost", 8000))
        self.msg_receive()
        self.socket.close()
