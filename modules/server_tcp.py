import socket
from threading import Thread, Lock
from modules.game import Game
from modules import protocol

class Server():
    def __init__(self, qnt_players: int):
        self.HOST = "0.0.0.0"           # Server's IP address
        self.PORT = 8000                # Server's port
        self.MSG_LEN = 1024             # Message's max length
        self.game = Game(qnt_players)
        self.qnt_players = qnt_players
        self.players_connected = 0
        self.clients = {}
        self.lock = Lock()


    # Método que recebe os novos clientes e os cadastra, recebendo seus nomes e os adicionando ao jogo
    def treat_client(self, client_socket, client_address):
        print(f"Cliente {client_address[0]}:{client_address[1]} conectado.")
        client_socket.send((protocol.get_name()).encode())
        while True:
            resp_client = client_socket.recv(self.MSG_LEN).decode()
            resp_client = resp_client.split(":")
            if resp_client[0] != "PUT_NAME":
                client_socket.send((protocol.send_conf("+FAIL")).encode())
                continue
            else:
                name = resp_client[-1]
                player = [client_socket, client_address, name]
                with self.lock:
                    self.game.add_player(player)
                    self.clients[client_address] = client_socket
                    self.players_connected += 1
                client_socket.send((protocol.send_conf("+OK")).encode())
                resp_client = client_socket.recv(self.MSG_LEN).decode().split(":")
                if resp_client[-1] == "+OK":
                    break
        return

    # Método que gerencia a partida do jogo
    def game_on(self):
        print(self.game.secret_word)
        with self.lock:
            while True:
                secret_word_status = self.game.secret_word_status()
                clue = self.game.secret_word_clue()
                choosed_letters = ", ".join(self.game.choosed_letters)
                player_turn = self.game.first()
                wheel_value = self.game.spin_wheel()

                # Monta a string com os dados da atualização do estado do jogo e envia para todos os clientes
                status = "STATUS:"+clue+":"+secret_word_status+":"+choosed_letters+":"+player_turn[-1]+":"+wheel_value
                self.broadcast(self.clients, status)

                # Trata os valores da roda, considerando o 'Passa a vez' e o 'Perde tudo'
                if self.treat_wheel(wheel_value):
                    wheel_value = int(wheel_value)
                else:
                    continue

                # Testa se tem mais de uma letra para ser adivinhada, se só tiver uma letra, manda uma opção 1 para que o cliente só possa adivinhar a palavra, bloqueando a opção 'Escolher Letra' no menu.
                if self.game.try_blank_spaces():
                    op = "0"
                else:
                    op = "1"
                
                # Gerencia o turno do jogador
                client = player_turn[0]
                client.send((protocol.send_turn(op)).encode())
                while True:
                    resp_client = client.recv(self.MSG_LEN).decode().split(":")
                    if resp_client[0] == "SEND_LETTER" or resp_client[0] == "SEND_WORD":
                        client.send((protocol.send_conf("+OK")).encode())
                        ack_client = client.recv(self.MSG_LEN).decode().split(":")
                        if ack_client[-1] == "+OK":
                            break
                    else:
                        client.send((protocol.send_conf("+FAIL")).encode())
                        continue
                self.treat_msg(resp_client, wheel_value)

                # Verifica se a palavra foi descoberta
                if self.game.secret_word_status().count("_") > 0:
                    continue
                else:
                    break
            
            # Gera e envia o ranking final para todos os jogadores
            ranking = protocol.send_ranking(self.game.ranking())
            self.broadcast(self.clients, ranking)

            # Envia para todos o comando para encerrar a conexão
            self.broadcast(self.clients, protocol.game_over())
        return

    # Método que trata os valores da roleta
    def treat_wheel(self, wheel_value: any) -> bool:
        if wheel_value == "Passa a vez":
            self.game.change_turn()
            return False
        elif wheel_value == "Perde tudo":
            self.game.lose_all()
            self.game.change_turn()
            return False
        else:
            return True

    # Método que trata das funções 'escolher letra' e ' adivinhar palavra', tratando a mensagem enviada pelo jogador
    def treat_msg(self, msg, wheel_value):
        if msg[0] == "SEND_LETTER":
            letter = msg[1]
            self.game.update_choosed_letters(letter)
            if self.game.try_letter(letter):
                msg_back = f"Tem letra {letter}"
                self.broadcast(self.clients, msg_back)
                self.game.processing_letter(wheel_value, letter)
                return
            else:
                msg_back = f"Não tem letra {letter}"
                self.broadcast(self.clients, msg_back)
                self.game.change_turn()
                return
        elif msg[0] == "SEND_WORD":
            if self.game.guess_word(msg[1]):
                msg_back = f'Acertou, mizeravi!'
                self.broadcast(self.clients, msg_back)
                return
            else:
                msg_back = f'Não é a palavra "{msg[1]}"'
                self.broadcast(self.clients, msg_back)
                self.game.change_turn()
                return

    # Método que envia uma mensagem broadcast para todos
    def broadcast(self, clients, msg):
        for socket in clients.values():
            socket.send(protocol.send_all(msg).encode())
            while True:
                msg_back = socket.recv(self.MSG_LEN).decode().split(":")
                if msg_back[-1] == "+OK":
                    break
                else:
                    socket.send(protocol.send_all(msg).encode())
                    continue
        return True

    # Método que inicia o servidor
    def start(self):
        word_cat = input("Deseja escolher a categoria da palavra secreta? (s/n) : ")
        if word_cat == "s":
            self.game.choose_word(input("Digite a categoria da palavra: "))
        else:
            self.game.choose_word()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        server = (self.HOST, self.PORT)
        sock.bind(server)
        sock.listen()
        print("Servidor ONLINE")

        while self.players_connected < self.qnt_players:
            sock.settimeout(1)
            try:
                client_socket, client_address = sock.accept()
            except KeyboardInterrupt:
                print("\nFinalizando o servidor.")
                break
            except socket.timeout:
                sock.settimeout(None)
                continue
            Thread(target=self.treat_client, args=(client_socket,   client_address)).start()
        
        print("O jogo vai começar")
        self.game_on()

        print("Finalizando servidor...")
        sock.close()
        print("Servidor OFFLINE.")
