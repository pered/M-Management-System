from typing import Optional, List
        
class Card:
    def __init__(self,
                 suit: str,
                 rank: str) -> None:
        self.suit = suit
        self.rank = rank

class Deck():
    cards: Optional[List[Card]] = None
    def __init__(self) -> None:
        self.description = None
        