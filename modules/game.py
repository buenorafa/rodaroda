from modules.player import Player
from modules.word import Word
from modules.fila_encadeada import Fila as Quee
from prettytable import PrettyTable
import random


class Game:
    def __init__(self, player_count:int) -> None:
        self.__player_count = player_count
        self.__players = Quee()
        self.__ranking = []
        self.__secret_word = None
        self.__secret_word_hidden = None
        self.__wheel = ["Perde tudo", "Passa a vez", "Passa a vez", "Passa a vez", 100, 100, 100, 100, 100, 100, 100, 200, 200, 200, 200, 200, 200, 200,300, 300, 300, 300, 300, 400, 400, 400, 400, 500, 500, 1000]
        self.__choosed_letters = []
        # (- 1) Perde tudo; (0) Passa a vez.


    @property
    def secret_word(self) -> str:
        return self.__secret_word
    
    @property
    def choosed_letters(self) -> list:
        return self.__choosed_letters
    
    def secret_word_clue(self) -> str:
        return self.__secret_word.clue
    

    def first(self) -> str:
        if not self.__players.esta_vazia():
            return self.__players.primeiro.name


    def add_player(self, name:str) -> bool:
        if self.__player_count > 0:
            self.__players.enfileirar(Player(name))
            self.__player_count -= 1
            return True
        return False
    

    def choose_word(self, category=None) -> bool:
        if not self.__secret_word:
            self.__secret_word = Word(category)
            self.__secret_word_hidden = ["_"]*len(self.__secret_word.word)
            return True
        return False


    def ranking(self) -> str:
        ranking = self.get_ranking()
        table = PrettyTable()
        table.field_names = ["Posição", "Nome", "Pontuação"]
        for i in range(len(ranking)):
            table.add_row([i+1, ranking[i].name[-1], ranking[i].score])
        return table.get_string()


    def get_ranking(self) -> list:
        for i in range(len(self.__players)):
            player = self.__players.desenfileirar()
            self.__ranking.append(player)
            self.__players.enfileirar(player)
        self.__ranking.sort(reverse=True)
        return self.__ranking


    def spin_wheel(self) -> str:
        return str(random.choice(self.__wheel))


    def choose_letter(self, letter:str) -> bool:
        return letter in self.__secret_word


    def try_letter(self, letter) -> bool:
        return letter in self.__secret_word.word
    

    def try_blank_spaces(self) -> bool:
        return self.__secret_word_hidden.count("_") > 1


    def processing_letter(self, wheel_value: int, letter:str) -> str:
        multiplier = 0
        for i in range(len(self.__secret_word)):
            if self.__secret_word.word[i] == letter:
                self.__secret_word_hidden[i] = letter
                multiplier += 1
        self.__players.primeiro.score += wheel_value * multiplier
        return True
    

    def guess_word(self, word:str) -> bool:
        if word != self.__secret_word.word:
            return False
        multiplier = self.__secret_word_hidden.count("_")
        # Atualiza a hidden
        self.__secret_word_hidden = self.__secret_word.word
        # Atualiza os pontos
        self.__players.primeiro.score += 200 * multiplier
        return True
        

    def change_turn(self):
        self.__players.enfileirar(self.__players.desenfileirar())
        

    def lose_all(self):
        self.__players.primeiro.score = 0


    def secret_word_status(self):
        return " ".join(self.__secret_word_hidden)


    def check_choosed_letters(self, letter: str) -> bool:
        return letter in self.__choosed_letters
    

    def update_choosed_letters(self, letter: str):
        self.__choosed_letters.append(letter)