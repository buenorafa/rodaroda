import random

class Word:
    def __init__(self, category=None):
        with open("utils/words.txt", "r") as file:
            content = file.read().split("\n")
            for i in range(len(content)):
                content[i] = content[i].split(";")
            if category is None:
                choosen_word = random.choice(content)
                self.__word = choosen_word[0]
                self.__clue = choosen_word[1]
                self.__category = choosen_word[2]
            else:
                content_categorized = []
                for i in range(len(content)):
                    if content[i][-1] == category:
                        content_categorized.append(content[i])
                if len(content_categorized) == 0:
                    raise ValueError("Categoria Inexistente.")
                content_categorized = random.choice(content_categorized)
                self.__word = content_categorized[0]
                self.__clue = content_categorized[1]
                self.__category = content_categorized[2]


    @property
    def word(self) -> str:
        return self.__word
    

    @property
    def category(self) -> str:
        return self.__category
    

    @property
    def clue(self) -> str:
        return self.__clue
    
    @word.setter
    def word(self, word):
        self.__word = word

    
    def __len__(self) -> int:
        return len(self.__word)

    def __str__(self) -> str:
        return f"Palavra: {self.__word.upper()}\nDica: {self.__clue.upper()}\nCategoria: {self.__category.upper()}"