from typing import Optional
from UNO.hand import Hand

class Player():
    """ Player class. """
    _unique_player_id = 1 # Class variable to keep track of unique player IDs

    def __init__(self, name, is_human: Optional[bool] = True):
        self.name = name

        # Composite, Player HAS-A hand                          
        self.hand = Hand()

        # Assign a unique ID to the player and increment it
        self.player_id = Player._unique_player_id    
        Player._unique_player_id += 1  
        
        # For using AI
        self._is_human = is_human

    def change_player_control(self, is_human: bool) -> None:
        """ Set whether the given player is controlled by a human or AI. """
        _is_human = is_human

    def is_human_controlled(self) -> bool:
        """ Returns whether the player is human controlled. """
        if self._is_human is not None:
            return self._is_human
        raise RuntimeError("Player is in invalid state - control type undefined.")
    
    def draw_card(self, card) -> None:
        """ Draw a card, add to hand. """
        self.hand.add_card(card)
