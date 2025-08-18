from UNO.card import Card
from UNO.game_constants import GameEvent

class Board():
    """ Board object that holds the cards that have been played. 
    
        Args: 
        - cards_on_board: A protected attribute for holding all board cards. 
        - observers: list of observers (only 1 currently)"""

    def __init__(self):
        self._cards_on_board = []
        self._observers = []

    def add_card_to_board(self, card: Card):
        """ Add card to the board. """
        self._cards_on_board.append(card)
        # Observer logic
        self.notify_observers(GameEvent.ADD_CARD_TO_BOARD, {'card': card})
        
    def get_board(self):
        """ Returns a (safe) copy of the board. """
        return self._cards_on_board.copy()
    
    def show_top_card_on_board(self) -> Card | None:
        """ Used to return the top card on the board, else return a None. """
        try:
            return self._cards_on_board[-1]
        except IndexError:
            return None
    
    def clear_all_except_last(self) -> list:
        """ Clears the board except for the last card. 
            Returns all cleared cards for recycling. """
        last_card: object = self.show_top_card_on_board()
        cards_to_recycle = [card for card in self._cards_on_board if card != last_card]
        self._cards_on_board = [last_card]
        # Observer logic
        self.notify_observers(GameEvent.BOARD_CLEARED, {'board_cards': self._cards_on_board})
        return cards_to_recycle
    
    def subscribe(self, observer):
        """ Subscribe as observer. """
        self._observers.append(observer)

    def notify_observers(self, event, data):
        """ Notify all subscribed observers """
        for observer in self._observers:
            observer.on_game_event(event, data)