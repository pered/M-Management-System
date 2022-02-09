from typing import Optional, List
import itertools 
       
class Card:
    def __init__(self,
                 suit: str,
                 rank: str) -> None:
        self.suit = suit
        self.rank = rank

class Deck():
    cards: Optional[List[Card]] = []
    def __init__(self) -> None:
        self.description = None
        pass
    
class CardStyle():
    def __init__(self, 
                 description:str, 
                 cards:List[str], 
                 suits:List[str]) -> None:
        self.description:str = description
        self.cards = cards
        self.suits = suits
    
    def create(self, 
               deckcards:Deck) -> None:
        for rank,suit in itertools.product(self.cards,self.suits):
            deckcards.cards.append(Card(suit,rank))
        
    
def main():
    testDeck = Deck()
    testCardStyle = CardStyle("Test",
                              ["Ace","King","Queen","Jack","10","9","8","7","6","5","4","3","2","1"],
                              ["Spades","Hearts","Diamonds","Clubs"])
    
    testCardStyle.create(testDeck)
    
    
    
    
if __name__ == "__main__":
    main()