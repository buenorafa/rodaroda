class Player:
    def __init__(self, name: str):
        self.name = name
        self.score = 0

    def __str__(self) -> str:
        return f"Nome: {self.name}\nPontuação: {self.score}"
    
    def __eq__(self, other: 'Player') -> bool:
        if not isinstance(other, Player):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.score == other.score

    def __ne__(self, other: 'Player') -> bool:
        if not isinstance(other, Player):
            return NotImplemented
        return self.score != other.score

    def __gt__(self, other: 'Player') -> bool:
        if not isinstance(other, Player):
            return NotImplemented
        return self.score > other.score

    def __lt__(self, other: 'Player') -> bool:
        if not isinstance(other, Player):
            return NotImplemented
        return self.score < other.score

    def __ge__(self, other: 'Player') -> bool:
        if not isinstance(other, Player):
            return NotImplemented
        return self.score >= other.score

    def __le__(self, other: 'Player') -> bool:
        if not isinstance(other, Player):
            return NotImplemented
        return self.score <= other.score
