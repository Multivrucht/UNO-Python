from UNO.deck import Deck
from UNO.card_factory import CardFactory
from UNO.game_config import Color, CardType, DeckConfiguration


class DeckBuilder:
    """ DeckBuilder used for generating a deck with a given configuration. """

    @staticmethod
    def create_deck() -> Deck:
        """ Create a new deck and returns the instantiation for further use. """
        deck = Deck()
        return deck

    @staticmethod
    def populate_deck(deck_config: DeckConfiguration, deck: Deck) -> None:
        """ Populate a deck with cards as defined in the configuration. """

        # Generate x amount of number cards. x defined by frequency_of_number_cards.
        for color in deck_config.DECK_COLORS:
            for card_value, frequency in deck_config.FREQUENCY_OF_NUMBER_CARDS.items():
                for _ in range(frequency):
                    deck.add_card_to_deck(CardFactory.create_card(color=color, card_type=CardType.NUMBER, card_value=card_value))
           
           # Generate x amount of special cards. x defined by action_cards_per_color.
            for card_type in deck_config.ACTION_CARDS:
                for _ in range(deck_config.ACTION_CARDS_PER_COLOR):
                    deck.add_card_to_deck(CardFactory.create_card(color=color, card_type=card_type))
        
        # Generate x amount of wild cards. x defined by wild_cards_per_type.
        for card_type in deck_config.WILD_CARDS:
            for _ in range(deck_config.WILD_CARDS_PER_TYPE):
                deck.add_card_to_deck(CardFactory.create_card(color=Color.COLORLESS, card_type=card_type))
        
        deck.shuffle_deck()
