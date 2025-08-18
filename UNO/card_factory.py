from typing import Optional
from UNO.card import NumberCard, SkipCard, ReverseCard, DrawTwoCard, WildCard, WildDrawFourCard
from UNO.game_config import Color, CardType


class CardFactory():
    """ Factory responsible for card generation. """
    next_card_id = 0

    @classmethod
    def create_card(cls, color: Optional[Color], card_type: CardType, card_value: Optional[int] = None):
        """ Factory method* returning a new card object.
            
            - *Slight anti-pattern behaviour, not strictly a factory. Due to scoping not changed atm. 
            
            Args:
                color: Card color (COLORLESS for wild cards)
                card_type: Type of card to create
                card_value: Numeric value (required for NUMBER cards)
                
            Returns:
                Appropriate Card subclass instance.
                
            Raises:
                ValueError: For unknown card types or invalid parameters. """
        
        card_id = CardFactory.__generate_card_id()
        
        match card_type:
            case CardType.NUMBER:
                if (card_value is None or color is None):
                    raise ValueError("NUMBER cards require card_value parameter.")
                return NumberCard(color=color, card_value=card_value, card_id=card_id)
            case CardType.SKIP:
                if color is None:
                    raise ValueError("ACTION cards require color parameter.")
                return SkipCard(color=color, card_id=card_id)
            case CardType.DRAW_TWO:
                if color is None:
                    raise ValueError("ACTION cards require color parameter.")
                return DrawTwoCard(color=color, card_id=card_id)
            case CardType.REVERSE:
                if color is None:
                    raise ValueError("ACTION cards require color parameter.")
                return ReverseCard(color=color, card_id=card_id)
            case CardType.WILD:
                return WildCard(card_id=card_id)
            case CardType.WILD_DRAW_FOUR:
                return WildDrawFourCard(card_id=card_id)
            case _:
                raise ValueError(f"Unknown card type: {card_type}")
   
    @classmethod
    def __generate_card_id(cls) -> int:
        """  Method to abstract the unique card ID generation.
            This is local ID, meaning it is only unique during a single run. """
        card_id = cls.next_card_id
        cls.next_card_id += 1
        return card_id
