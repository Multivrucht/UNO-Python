from enum import Enum

class Color(Enum):
    """ Enums for a fixed type-safe value for colors"""

    RED = "Red"
    YELLOW = "Yellow"
    GREEN = "Green"
    BLUE = "Blue"
    COLORLESS = "Colorless"

class CardType(Enum):
    """ Enums for a fixed type-safe value for CardTypeNames.
        Used for identifying cards in the game. """  
    
    NUMBER = "Number"
    SKIP = "Skip"
    DRAW_TWO = "Draw +2"
    REVERSE = "Reverse"
    WILD = "Wild"
    WILD_DRAW_FOUR = "Wild Draw +4"
    CUSTOM_CARD_X = "Custom X"
    CUSTOM_ACTION_CARD_Y = "Custom Y"
    CUSTOM_WILD_CARD_Z = "Custom Z"

class GameState(Enum):
    """ Enums for a fixed type-safe value for various menus
        Used to switch between various screens within the game.  """
    
    MAIN_MENU = "Main Menu"
    CARD_SELECTION = "Card Selection"
    END_TURN = "End Turn"

class GameEvent(Enum):
    """ Enum events for game's Observer Pattern and for potential future multiplayer state management. """

    CARD_PLAYED = "Card Played"
    CARD_DRAWN = "Card Drawn"
    ADD_CARD_TO_DECK = "Added Card To Deck"
    ADD_CARD_TO_BOARD = "Added Card To Board"
    REMOVE_CARD_FROM_DECK = "Remove Card From Deck"
    PLAYER_TURN_CHANGED = "Player Turn Changed"
    TURN_ORDER_CHANGED = "Turn Order Changed"
    BOARD_CLEARED = "Board Cleared"
    # Ideas I want to implement later for more robust event management:
    # UNO = "UNO"
    # GAME_START = "Game Started" 
    # GAME_PAUSED = "Game Paused"
    # GAME_ENDED = "Game Ended"
    # GAME_WON = "Game Won"
    # CONFIG_CHANGED = "Game Configuration Changed"

class EffectCategory(Enum):
    """ Enums for a fixed type-safe value for various special effects.
        Used to classify similar effects so game rules can be applied. 
        
        BE AWARE:
        This works for a small scope, but will get complex quickly as custom effects and rules increase. """
    
    DRAW = "Draw"
    COLOR_CHANGE = "Color Change"
    TURN = "Turn"
    END_TURN = "End Turn"