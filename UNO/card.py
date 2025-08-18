from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional
from UNO.game_constants import Color, CardType, EffectCategory
from UNO.utils import UserInput
from UNO.basic_ai import AI

if TYPE_CHECKING:
    from UNO.game import Game

class Card(ABC):
    """ Abstract base card class with integrated effect behavior.

    Args:
    - Color: The color of the card, colorless for wild cards
    - Card Value: The int value of the card, only for number cards
    - Card ID: Unique int ID of the card
    - Effect Types: A set with an EffectCategory enum. This set can combine multiple effectcategories. 
        These categories are used to identify similar effects over different cards, to for example check if a card
        is a draw card, and if it can be stacked. This approach was introduced with the idea of introducing more custom effects.
    - SUBCLASS: Effective color: The color that is selected by a player: e.g. wild card gets a yellow effective color.


    Current & Future Design Choices:
    - Special FX validation & execution is done in the cards itself, not the GameEngine. This is a relic from an older refactor. 
        Might extract the effects from the card in an effect handler class that handles effecttypes, making it easier to customize and stack effects.
    - Cards are currently generated in a rather specific way, having quite tight coupling with the card_factory.
    -- Due to that, the difference betwenen propertymethods and attributes might feel a little random. 
    -- The attributes do not encapsulate access properly. They offer no return methods but do indicate they are protected
    
        Needs fixing: 
        - Color, card_value and ID should also be a property.
        - Verbose If None check, which is already done in the validation logic in Game.
        - Type Hints & effect type
        - Correct private/protected attribute properties
        - Clean up init parameters.. 
          """
    
    def __init__(self, color: Color, card_value: Optional[int] = None, card_id: int = None):
        self._color = color
        self._card_value = card_value
        self._card_id = card_id
        self._effect_types: set[EffectCategory] = set()  # Default to empty set
    
    @property
    @abstractmethod
    def color(self) -> Color:
        """ Returns the card color. """
        pass

    @property
    @abstractmethod
    def card_value(self) -> int | None:
        """ Returns the value of the card, non-number cards is None.  """
        pass

    @property
    @abstractmethod
    def card_id(self) -> int:
        """ Returns the card_id.  """
        pass

    @property
    @abstractmethod
    def effect_types(self) -> set:
        """ Returns the card_id.  """
        pass

    @property
    @abstractmethod
    def card_type(self) -> CardType:
        """ Define the card type - implemented by subclasses. """
        pass

    @property
    @abstractmethod
    def effective_color(self) -> Color:
        """ Get the color for matching purposes. """
        pass
    
    @abstractmethod
    def execute_effect(self, game_context: 'Game') -> None:
        """Execute this card's special effect"""
        pass
    
    @abstractmethod
    def can_execute_effect(self, game_context: 'Game') -> bool:
        """Validate if this card's effect can be executed"""
        pass
    
    def _validate_last_card_allowed(self, game_context: 'Game') -> bool:
        # Check if special card is players' last card and if allowed
        if game_context.rules.ALLOW_FINAL_SPECIAL_CARD is False:
            if len(game_context.tm.get_current_player().hand.show_hand()) == 1:
                return False
        return True

    def __str__(self) -> str:
        return (f"Card: {self.__class__.__name__:<16}| "
        f"ID: {self._card_id:<3} | "
        f"Color: {self._color.value:<10} | "
        f"Effective: {self.effective_color.value:<10} | "
        f"Value: {self._card_value if self._card_value is not None else 'N/A':<4} | "
        f"Type: {self.card_type.value}")

class NumberCard(Card):
    """ Standard numbered card with no special effects. """
    
    def __init__(self, color: Color, card_value: int, card_id: int):
        super().__init__(color=color, card_value=card_value, card_id=card_id)
    
    @property
    def color(self) -> Color:
        """ Returns the card color. """
        return self._color

    @property
    def card_value(self) -> int | None:
        """ Returns the value of the card, non-number cards is None.  """
        return self._card_value

    @property
    def card_id(self) -> int:
        """ Returns the card_id.  """
        return self._card_id

    @property
    def effect_types(self) -> set:
        """ Returns the card_id.  """
        return self._effect_types

    @property
    def card_type(self) -> CardType:
        return CardType.NUMBER
    
    @property
    def effective_color(self) -> Color:
        return self._color
    
    def execute_effect(self, game_context: 'Game') -> None:
        pass # Number card has no effect 
    
    def can_execute_effect(self, game_context: 'Game') -> bool:
        return True  # Number cards can always be played

class SkipCard(Card):
    """Skip card - skips next player's turn"""
    
    def __init__(self, color: Color, card_id: Optional[int]):
        super().__init__(color=color, card_id=card_id)
        self._effect_types = {EffectCategory.TURN}
    
    @property
    def color(self) -> Color:
        """ Returns the card color. """
        return self._color

    @property
    def card_value(self) -> int | None:
        """ Returns the value of the card, non-number cards is None.  """
        return self._card_value

    @property
    def card_id(self) -> int:
        """ Returns the card_id.  """
        return self._card_id

    @property
    def effect_types(self) -> set:
        """ Returns the card_id.  """
        return self._effect_types
        
    @property
    def card_type(self) -> CardType:
        return CardType.SKIP
    
    @property
    def effective_color(self) -> Color:
        return self._color

    def execute_effect(self, game_context: 'Game') -> None:
        game_context.tm.skip_turn()
        print(f"* Next player skipped! *")
    
    def can_execute_effect(self, game_context: 'Game') -> bool:
        top_card = game_context.board.show_top_card_on_board()
        # Check if first card
        if top_card is None:
            return True
        
        # Check if special card is players' last card and if allowed
        if not self._validate_last_card_allowed(game_context):
            return False
            
        return True  # Skip can always be executed

class DrawTwoCard(Card):
    """Draw Two card - forces next player to draw 2 cards"""
    
    def __init__(self, color: Color, card_id: Optional[int]):
        super().__init__(color=color, card_id=card_id)
        self._effect_types = {EffectCategory.DRAW}

    @property
    def color(self) -> Color:
        """ Returns the card color. """
        return self._color

    @property
    def card_value(self) -> int | None:
        """ Returns the value of the card, non-number cards is None.  """
        return self._card_value

    @property
    def card_id(self) -> int:
        """ Returns the card_id.  """
        return self._card_id

    @property
    def effect_types(self) -> set:
        """ Returns the card_id.  """
        return self._effect_types 
    
    @property
    def card_type(self) -> CardType:
        return CardType.DRAW_TWO
    
    @property
    def effective_color(self) -> Color:
        return self._color
    
     #. TO FIX TYPE HINTING -->>>>>>>>>>>>>>>>>>>>>>>
    def execute_effect(self, game_context: 'Game') -> None:
        next_player = game_context.tm.get_next_player()
        game_context.engine.player_draw_card(next_player, amount=2)

        if game_context.rules.SKIP_TURN_ON_DRAW:
            print("* and loses their turn! *")
            game_context.tm.skip_turn()
        
    def can_execute_effect(self, game_context: 'Game') -> bool:
        top_card = game_context.board.show_top_card_on_board()
        # Check if first card
        if top_card is None:
            return True
        
        # Check if special card is players' last card and if allowed
        if not self._validate_last_card_allowed(game_context):
            return False
        
        # Check if this effect may be stacked
        if game_context.rules.STACKABLE_DRAW_CARDS is False:
            if EffectCategory.DRAW in top_card._effect_types: 
                return False

        return True

class ReverseCard(Card):
    """Reverse card - reverses direction of play"""
    
    def __init__(self, color: Color, card_id: Optional[int] = None):
        super().__init__(color=color, card_id=card_id)
        self._effect_types = {EffectCategory.TURN}

    @property
    def color(self) -> Color:
        """ Returns the card color. """
        return self._color

    @property
    def card_value(self) -> int | None:
        """ Returns the value of the card, non-number cards is None.  """
        return self._card_value

    @property
    def card_id(self) -> int:
        """ Returns the card_id.  """
        return self._card_id

    @property
    def effect_types(self) -> set:
        """ Returns the card_id.  """
        return self._effect_types
    
    @property
    def card_type(self) -> CardType:
        return CardType.REVERSE
    
    @property
    def effective_color(self) -> Color:
        return self._color 
    
    def execute_effect(self, game_context: 'Game') -> None:
        game_context.tm.reverse_play_order()
        print("* Direction of play reversed! *")
    
    def can_execute_effect(self, game_context: 'Game') -> bool:
        top_card = game_context.board.show_top_card_on_board()
        # Check if first card
        if top_card is None:
            return True
    
        # Check if special card is players' last card and if allowed
        if not self._validate_last_card_allowed(game_context):
            return False
            
        return True

class WildCard(Card):
    """Wild card - allows color change"""
    
    def __init__(self, card_id: Optional[int]):
        super().__init__(color=Color.COLORLESS, card_id=card_id)
        self._chosen_color: Optional[Color] = None
        self._effect_types = {EffectCategory.COLOR_CHANGE}

    @property
    def color(self) -> Color:
        """ Returns the card color. """
        return self._color

    @property
    def card_value(self) -> int | None:
        """ Returns the value of the card, non-number cards is None.  """
        return self._card_value

    @property
    def card_id(self) -> int:
        """ Returns the card_id.  """
        return self._card_id

    @property
    def effect_types(self) -> set:
        """ Returns the card_id.  """
        return self._effect_types

    @property
    def card_type(self) -> CardType:
        return CardType.WILD
    
    @property
    def effective_color(self) -> Color:
        """ Check if chosen color is assigned, else return COLORLESS. """
        return self._chosen_color if self._chosen_color else Color.COLORLESS
    
    def set_chosen_color(self, color: Color) -> None:
        """ Set the chosen color. """
        self._chosen_color = color
    
     #. TO FIX TYPE HINTING -->>>>>>>>>>>>>>>>>>>>>>>
    def execute_effect(self, game_context: 'Game') -> None:
        """ Card can always be played. 
            Has optional effect of: 
            - Make next player skip a turn.
            - Make current player select a color.
        
        Future refactoring:
        - Note that the skip mechanic currently just skips the current players turn - 
            the game loop then finishes the next players turn.  """
            
        if game_context.rules.WILD_CARD_ALLOW_PICK_COLOR:
            current_player = game_context.tm.get_current_player()
            if not current_player.is_human_controlled():
                selected_color = AI.auto_select_color(game_context)
            else:
                selected_color = UserInput.get_color_selection()
            self.set_chosen_color(selected_color)
            print(f"-> {current_player.name} changed the color to: {selected_color.value}")
    
    def can_execute_effect(self, game_context: 'Game') -> bool:
        top_card = game_context.board.show_top_card_on_board()
        # Check if first card
        if top_card is None:
            return True
        
        # Check if special card is players' last card and if allowed
        if not self._validate_last_card_allowed(game_context):
            return False
            
        return True

class WildDrawFourCard(Card):
    """ Wild Draw Four card - color change + draw 4 """
    
    def __init__(self, card_id: Optional[int]):
        super().__init__(color=Color.COLORLESS, card_id=card_id)
        self._chosen_color: Optional[Color] = None
        self._effect_types = {EffectCategory.DRAW, EffectCategory.COLOR_CHANGE}

    @property
    def color(self) -> Color:
        """ Returns the card color. """
        return self._color

    @property
    def card_value(self) -> int | None:
        """ Returns the value of the card, non-number cards is None.  """
        return self._card_value

    @property
    def card_id(self) -> int:
        """ Returns the card_id.  """
        return self._card_id

    @property
    def effect_types(self) -> set:
        """ Returns the card_id.  """
        return self._effect_types
    
    @property
    def card_type(self) -> CardType:
        return CardType.WILD_DRAW_FOUR

    @property
    def effective_color(self) -> Color:
        """ Check if chosen color is assigned, else return COLORLESS. """
        return self._chosen_color if self._chosen_color else Color.COLORLESS
    
    def set_chosen_color(self, color: Color) -> None:
        """ Set the chosen color. """
        self._chosen_color = color
    
    def execute_effect(self, game_context: 'Game') -> None:
        """ Card can always be played. Makes next player draw 4 cards.
            Has optional effect of: 
            - Make next player skip a turn.
            - Make current player select a color.
        
        Future refactoring:
        - Note that the skip mechanic currently just skips the current players turn - 
            the game loop then finishes the next players turn.  """

        if game_context.rules.WILD_CARD_ALLOW_PICK_COLOR:
            current_player = game_context.tm.get_current_player()
            if not current_player.is_human_controlled():
                selected_color = AI.auto_select_color(game_context)
            else:
                selected_color = UserInput.get_color_selection()
            self.set_chosen_color(selected_color)
            print(f"-> {current_player.name} changed the color to: {selected_color.value}")

        next_player = game_context.tm.get_next_player()
        game_context.engine.player_draw_card(next_player, amount=4)

        if game_context.rules.SKIP_TURN_ON_DRAW:
            # CAREFUL, WILL SKIP CURRENT PLAYER. WORKS, BUT IS UGLY AND NEEDS FIXING
            print("* and loses their turn! *")
            game_context.tm.skip_turn()

    def can_execute_effect(self, game_context: 'Game') -> bool:
        """ Checks if effect is a legal move. """
        top_card = game_context.board.show_top_card_on_board()
        # Check if first card
        if top_card is None:
            return True
        
        # Check if special card is players' last card and if allowed
        if not self._validate_last_card_allowed(game_context):
            return False

        # Check if this effect may be stacked
        if game_context.rules.STACKABLE_DRAW_CARDS is False:
            if EffectCategory.DRAW in top_card.effect_types: 
                return False
    
        return True
    

    