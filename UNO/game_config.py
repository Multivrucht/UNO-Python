from typing import Dict, List, Optional
from enum import Enum
from UNO.game_constants import Color, CardType


class DeckConfiguration:
    """ Base configuration class for the deck configuration.
        Allows the user to configure custom decks, with basic game logic validation.
        Initially I wanted to load this configuration from a JSON, 
        but I pivoted and settled for something hybrid. 
        
        HOW TO USE:
        To create a subset with your own deck, create/modify a class and your deck configuration changes.
        If you skip a deck configuration section, the system will use the base value for that specific section. 
        Once changed, adjust the 
    
        """

    # Base defaults
    FREQUENCY_OF_NUMBER_CARDS: Dict[int, int] = {0: 1, **{i: 2 for i in range(1, 10)}}
    ACTION_CARDS_PER_COLOR: int = 2
    WILD_CARDS_PER_TYPE: int = 4
    DECK_COLORS: List[Color] = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW]
    ACTION_CARDS: List[CardType] = [CardType.SKIP, CardType.DRAW_TWO, CardType.REVERSE]
    WILD_CARDS: List[CardType] = [CardType.WILD, CardType.WILD_DRAW_FOUR]
    
    @staticmethod
    def validate_deckconfig(decktemplate) -> List[str]:
        """ Basic deck validation logic. Essential for when loading user configured decks. 
            This configuration is little bit more elaborate than the rule validation, but still nothing fancy. """
        issues = []
        decktemplate = decktemplate.value
        
        # Validate FREQUENCY_OF_NUMBER_CARDS
        if hasattr(decktemplate, 'FREQUENCY_OF_NUMBER_CARDS'):
            freq_cards = decktemplate.FREQUENCY_OF_NUMBER_CARDS
            if not isinstance(freq_cards, dict):
                issues.append("FREQUENCY_OF_NUMBER_CARDS must be a dictionary")
            else:
                for card_value, frequency in freq_cards.items():
                    # Validate card values are in valid range (0-9 for UNO)
                    if not isinstance(card_value, int) or not (0 <= card_value):
                        issues.append(f"Invalid card value: {card_value}. Must be positive integer")
                    
                    # Validate frequencies are positive integers
                    if not isinstance(frequency, int) or frequency < 0:
                        issues.append(f"Invalid frequency {frequency} for card {card_value}. Must be non-negative integer")
        
        # Validate ACTION_CARDS_PER_COLOR
        if hasattr(decktemplate, 'ACTION_CARDS_PER_COLOR'):
            action_per_color = decktemplate.ACTION_CARDS_PER_COLOR
            if not isinstance(action_per_color, int) or action_per_color < 0:
                issues.append(f"ACTION_CARDS_PER_COLOR must be non-negative integer, got: {action_per_color}")
        
        # Validate WILD_CARDS_PER_TYPE  
        if hasattr(decktemplate, 'WILD_CARDS_PER_TYPE'):
            wild_per_type = decktemplate.WILD_CARDS_PER_TYPE
            if not isinstance(wild_per_type, int) or wild_per_type < 0:
                issues.append(f"WILD_CARDS_PER_TYPE must be non-negative integer, got: {wild_per_type}")
        
        # Validate DECK_COLORS
        if hasattr(decktemplate, 'DECK_COLORS'):
            deck_colors = decktemplate.DECK_COLORS
            if not isinstance(deck_colors, list) or len(deck_colors) == 0:
                issues.append("DECK_COLORS must be non-empty list")
            else:
                for color in deck_colors:
                    if not isinstance(color, Color):
                        issues.append(f"Invalid color type: {color}. Must be Color enum value")
        
        # Validate ACTION_CARDS
        if hasattr(decktemplate, 'ACTION_CARDS'):
            action_cards = decktemplate.ACTION_CARDS
            if not isinstance(action_cards, list):
                issues.append("ACTION_CARDS must be a list")
            else:
                valid_action_types = {CardType.SKIP, CardType.DRAW_TWO, CardType.REVERSE}
                for card_type in action_cards:
                    if not isinstance(card_type, CardType):
                        issues.append(f"Invalid action card type: {card_type}. Must be CardType enum")
                    elif card_type not in valid_action_types:
                        issues.append(f"Invalid action card: {card_type}. Must be SKIP, DRAW_TWO, or REVERSE")
        
        # Validate WILD_CARDS
        if hasattr(decktemplate, 'WILD_CARDS'):
            wild_cards = decktemplate.WILD_CARDS
            if not isinstance(wild_cards, list):
                issues.append("WILD_CARDS must be a list")
            else:
                valid_wild_types = {CardType.WILD, CardType.WILD_DRAW_FOUR}
                for card_type in wild_cards:
                    if not isinstance(card_type, CardType):
                        issues.append(f"Invalid wild card type: {card_type}. Must be CardType enum")
                    elif card_type not in valid_wild_types:
                        issues.append(f"Invalid wild card: {card_type}. Must be WILD or WILD_DRAW_FOUR")
        
        return issues
    
class StandardDeck(DeckConfiguration):
    """ Standard UNO deck configuration, uses base defaults. """

class HardcoreDeck(DeckConfiguration):
    """ Hardcore variant with 2 of each number and more wild/action cards.  """

    FREQUENCY_OF_NUMBER_CARDS: Dict[int, int] = {i: 2 for i in range(0, 10)}
    ACTION_CARDS_PER_COLOR: int = 3
    WILD_CARDS_PER_TYPE: int = 6

class TestingDeck(DeckConfiguration):
    """ Minimal deck for testing with more wild cards and less colors. """

    FREQUENCY_OF_NUMBER_CARDS: Dict[int, int] = {i: 2 for i in range(0, 10)}
    ACTION_CARDS_PER_COLOR: int = 4
    WILD_CARDS_PER_TYPE: int = 20
    DECK_COLORS: List[Color] = [Color.RED, Color.BLUE]
    ACTION_CARDS: List[CardType] = [CardType.SKIP, CardType.DRAW_TWO, CardType.REVERSE]
    WILD_CARDS: List[CardType] = [CardType.WILD, CardType.WILD_DRAW_FOUR]

class IntentionalBrokenDeck(DeckConfiguration):
    """ Intentionally broken deck for demonstration purposes.  """

    FREQUENCY_OF_NUMBER_CARDS: list = [3.5]
    ACTION_CARDS_PER_COLOR: int = -2
    WILD_CARDS_PER_TYPE: int = -4
    DECK_COLORS: List[Color] = [Color.RED, Color.BLUE, "GEEL"]
    ACTION_CARDS: List[CardType] = [CardType.SKIP, CardType.DRAW_TWO, "CardType.REVERSE"]
    WILD_CARDS: List[CardType] = [CardType.WILD, CardType.WILD_DRAW_FOUR]


class GameRules:
    """ Default base game rule configuration class. Allows the user to configure custom rules, with some basic rule validation.
        Initially I wanted to load this configuration from a JSON, but I pivoted and settled for something hybrid. 

        HOW TO USE:
        To create a subset with rules, create/modify a class and add the rules that you want to change.
        If a rule is not added, the system will use the base value for that specific rule. 
    
        GENERAL RULE: Applied to the game of itself
        CARD RULE: Applied or related to a specific type of card. Logic defined in the coressponding card or EffectCategory"""
   
   # BASE RULES. 
    FORCE_PLAY_IF_POSSIBLE: bool = True         # GENERAL RULE: INACTIVE, ADDED LATER - IF FALSE, set allow_multiple_decks = TRUE.
    ALLOW_MULTIPLE_DECKS: bool = True           # GENERAL RULE: Allow for multiple decks.
    STARTING_HAND_SIZE: int = 7                 # GENERAL RULE: Set starting hand size (>0)
    ALLOW_FINAL_SPECIAL_CARD: bool = True       # GENERAL RULE: IF Action and Wild cards can be played as final card
    DRAW_PENALTY: int = 1                       # GENERAL RULE: INACTIVE, ADDED LATER - Cards drawn when unable to play
    TIMEOUT_SECONDS: int = 30                   # GENERAL RULE: INACTIVE, ADDED LATER -
    STACKABLE_DRAW_CARDS: bool = True           # CARD RULE: IF you can stack Draw X amount cards. Affects any card with EffectCategory: DRAW
    WILD_CARD_ALLOW_PICK_COLOR: bool = True     # CARD RULE: IF you can select a color after playing a WILD card
    SKIP_TURN_ON_DRAW: bool = False             # CARD RULE: IF a Draw Card (Action or WILD) skips next players turn. Affects any card with EffectCategory: DRAW
    
    @staticmethod
    def validate_rules(ruleset) -> List[str]:
        """ Basic rule set validation logic. Essential for when loading user configured rules.
            Displayed at Config Selection to evaluate a (new) custom configuration. 
            This validation is a whole lot less extensive than the deck variant. 
            As such, this method is mostly used for demonstrative purposes.  """
    
        ruleset = ruleset.value
        issues = []

        if ruleset.STARTING_HAND_SIZE > 10:
            issues.append("Starting hand size may be too large")
        if ruleset.FORCE_PLAY_IF_POSSIBLE is False and ruleset.allow_multiple_decks is False:
            issues.append("Force Play: False may result in insufficient cards if allow_multiple_decks is: False")
        if ruleset.DRAW_PENALTY < 0:
            issues.append("Draw penalty cannot be negative")
        return issues
 
class StandardRules(GameRules):
    """ Standard gameplay rules, uses base defaults. """

class HardcoreRules(GameRules):
    """ Custom UNO gameplay rules"""

    FORCE_PLAY_IF_POSSIBLE: bool = True         # GENERAL RULE: INACTIVE, ADDED LATER - IF FALSE, set allow_multiple_decks = TRUE.
    ALLOW_FINAL_SPECIAL_CARD: bool = False      # GENERAL RULE: IF Action and Wild cards can be played as final card
    DRAW_PENALTY: int = 2                       # GENERAL RULE: INACTIVE, ADDED LATER - Cards drawn when unable to play
    TIMEOUT_SECONDS: int = 20                   # GENERAL RULE: INACTIVE, ADDED LATER -
    STACKABLE_DRAW_CARDS: bool = True           # CARD RULE: IF you can stack Draw X amount cards. Affects any card with EffectCategory: DRAW
    WILD_CARD_ALLOW_PICK_COLOR: bool = True     # CARD RULE: IF you can select a color after playing a WILD card
    SKIP_TURN_ON_DRAW: bool = True              # CARD RULE: IF a Draw Card (Action or WILD) skips next players turn. Affects any card with EffectCategory: DRAW

class GameRulesEnum(Enum):
    """ Fixed values with class objects for the rules. """
    STANDARD = StandardRules
    HARDCORE = HardcoreRules

class DeckConfigEnum(Enum):
    """ Fixed values with class objects for the deck configuration. """
    STANDARD = StandardDeck
    HARDCORE = HardcoreDeck
    TESTDECK = TestingDeck
    BROKENDECK = IntentionalBrokenDeck

