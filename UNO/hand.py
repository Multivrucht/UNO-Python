from UNO.card import Card

class Hand():
    """ Hand class, used as a composition within the Player class.
        Represents the cards held by a player. 
        
        Args: 
        - cards: A protected attribute for holding all player cards. """

    def __init__(self):
        self._cards = []

    def add_card(self, card: Card) -> None:
        """ Add card to hand. """
        self._cards.append(card)

    def show_hand(self) -> str:
        """ Returns a formatted hand string - CLI display method. """
        if not self._cards:
            return "Hand is empty"
        
        lines = []
        for index, card in enumerate(self._cards):
            lines.append(f"{index}: {card}")
        return "\n".join(lines)

    def get_hand(self) -> list:
        """ Returns a copy of player's hand. Preserves integrity of original. """
        return self._cards.copy()
    
    def remove_card(self, card: Card) -> None:
        """ Remove specific card from hand. """
        self._cards.remove(card)

    def select_card(self, user_input: int) -> Card | None:
        """ Select a card from player's Hand. 
            Returns None when retrieval failed.  """
        card_selection = None
        try:
            card_selection = self._cards[int(user_input)]
        except IndexError as e:
            print(f'Not a valid index number, try again. Error: {e}')
        except ValueError as e:
            print(f'Not a valid value provided, try again. Error: {e}')
        except Exception as e: 
            print(f'A generic error occured, try again. Error: {e}')

        return card_selection
    