from random import shuffle
from UNO.card import Card
from UNO.game_constants import GameEvent


class Deck():
    """ Deck, responsible for the cards"""

    def __init__(self):
        self._card_deck = []
        self._observers = []
        
    def get_deck(self):
        """ Returns a (safe) copy of the deck. """
        return self._card_deck.copy()
    
    def add_card_to_deck(self, card: Card) -> None:
        """ Add a card to the Deck. """
        self._card_deck.append(card)

        # Observer logic
        self.notify_observers(GameEvent.ADD_CARD_TO_DECK, {'card': card})

    def shuffle_deck(self) -> None:
        """ Shuffles the deck. """
        shuffle(self._card_deck)
    
    def get_deck_length(self) -> int:
        """ Get the length of the deck, excluding the board (if it contains any). """
        return len(self._card_deck)

    def draw_card(self) -> Card | None:
        """ Attempts to draw a card, returns None if it failed.  """
        if self._card_deck:
            # Explicit code for the observer
            card = self._card_deck.pop()
            self.notify_observers(GameEvent.REMOVE_CARD_FROM_DECK, {'card': card})
            return card
        return None
        
    def attempt_recycle_deck(self, board) -> None:
        """ Recycles the cards from the board to be put back in the deck. """
        board_cards_to_recycle = board.clear_all_except_last()
        for card in board_cards_to_recycle:
            self.add_card_to_deck(card)

    def subscribe(self, observer):
        self._observers.append(observer)

    def notify_observers(self, event, data):
        for observer in self._observers:
            observer.on_game_event(event, data)