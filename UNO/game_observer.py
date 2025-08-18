from abc import ABC, abstractmethod
from typing import Dict, Any, TYPE_CHECKING
from datetime import datetime
from UNO.game_constants import GameEvent as Event
from UNO.player import Player
from UNO.card import Card

if TYPE_CHECKING:
    from UNO.game import Game 

class GameObserver(ABC):
    """ Observer abstract class for the game. 
        Mostly used for managing game states and for in the future, saving/restoring games and perhaps offering a small multiplayer version.  """

    @abstractmethod
    def on_game_event(self, event: Event, data: Dict[str, Any]) -> None:
        """ React to game state changes. """
        pass

class GameContext(GameObserver):
    """ OBSERVER: Context Manager for the Game. 
        
        Current & future design:
        This observer now notes and saves all game context related actions, so that in the future this can be used to pause and restore games.
        The saving functionality is already working mostly, as all data is beign serialized in the snapshots, it just needs a method to log it into a file.
        """
    
    def __init__(self, game: 'Game'):
        self.game = game # Dirty scoping, needs proper fix

        # Game static creation snapshots
        self._rule_snapshot = game.rules # Not proper serialization atm, but for now assumes rules stay the same for the configurations
        self._deck_config_snapshot = game.deck_config # Not proper serialization, but for now assumes deck configuration classes stays the same.
        self._players_snapshot = {player.player_id: {'name': player.name,'is_human': player.is_human_controlled()}
                                   for player in game.players} # Doesnt work with leaving players, needs fixing for a potential future multiplayer
        
        # Empty dynamic snapshots
        self._topcard_snapshot = {} # Same value as deck_snapshot[-1] but kept for easy-of-use
        self._hand_per_player_snapshot = {}
        self._deck_snapshot = {}
        self._board_snapshot = {}
        self._current_player_snapshot = {}
        self._turn_order_snapshot = {}
        self._last_updated = datetime.now()

        # Subscribe to game events
        self.game.subscribe(self)
        self.game.board.subscribe(self)
        self.game.deck.subscribe(self)

    def on_game_event(self, event: Event, data: Dict[str, Any]) -> None:
        """ When event XYZ happens, fire off the proper method. """
        if event == Event.CARD_DRAWN:
            self._update_player_held_cards(data['card'], data['player'], event)
            # self._update_deck()

        elif event == Event.CARD_PLAYED:
            self._update_player_held_cards(data['card'], data['player'], event)
            self._update_deck_remove_card(data['card'])

        elif event == Event.PLAYER_TURN_CHANGED:
            # Yet to implement
            pass
        
        elif event == Event.TURN_ORDER_CHANGED:
            # Yet to implement
            pass

        elif event == Event.ADD_CARD_TO_BOARD:
            self._update_top_card(data['card'])
            self._update_board_add_card(data['card'])

        elif event == Event.BOARD_CLEARED:
            self._update_board_after_clearing(data['board'])

        elif event == Event.ADD_CARD_TO_DECK:
            self._update_deck_add_card(data['card'])

    def _update_turn_order(self):
        # Yet to implement
        pass
    
    
    def _update_current_player_turn(self, player: Player):
        # Yet to implement
        pass

    def _update_deck_remove_card(self, card: Card) -> None:
        """ Update deck by removing a single card. """
       # Store card data as a dictionary
        card_data = {
            'card_type': card.card_type.value,
            'card_data': {
                'color': card.color.value,                      # Enum to string
                'card_type': card.card_type.value,              # Enum to string
                'card_value': card.card_value                   # Int
                }                  
        }

        self._deck_snapshot['deck_cards'].remove(card_data)
        
    # DOESNT WORK WITH SHUFFLE YET! DOESNT ADJUST THE ORDER BASED IN SHUFFLE.
    # Would like to preserve the order of the deck, so shuffled state needs to be added here
    def _update_deck_add_card(self, card: Card) -> None:
        """ Update deck snapshot with new card. """
        # Store card data as a dictionary
        card_data = {
            'card_type': card.card_type.value,
            'card_data': {
                'color': card.color.value,                      # Enum to string
                'card_type': card.card_type.value,              # Enum to string
                'card_value': card.card_value                   # Int
                }                  
        }
        if 'deck_cards' not in self._deck_snapshot:
            self._deck_snapshot['deck_cards'] = []
        self._deck_snapshot['deck_cards'].append(card_data)

    def _update_player_held_cards(self, card: Card, player: Player, event: Event) -> None:
        """ Update card to individual player snapshot with played card. Adds the player if first call. """

        # Add player to the list
        if player.name not in self._hand_per_player_snapshot:
            self._hand_per_player_snapshot[player.name] = []

        # Store card data as a dictionary
        card_data = {
            'card_type': card.card_type.value,
            'card_data': {
                'color': card.color.value,                      # Enum to string
                'card_type': card.card_type.value,              # Enum to string
                'card_value': card.card_value                   # Int
                }                  
        }

        # Add card to the snapshot
        if event is Event.CARD_DRAWN:
            self._hand_per_player_snapshot[player.name].append(card_data)
        # Remove card from snapshot
        if event is Event.CARD_PLAYED:
            self._hand_per_player_snapshot[player.name].remove(card_data)

    def _update_board_after_clearing(self, board: dict[str, Card]) -> None:
        """ Update board snapshot after clearing. """
        self._board_snapshot = {}
        self._board_snapshot = board
   
    def _update_board_add_card(self, card: Card) -> None:
        """ Update board after card gets played. """
        card_data = {
            'card_type': card.card_type.value,
            'card_data': {
                'color': card.color.value,                      # Enum to string
                'card_type': card.card_type.value,              # Enum to string
                'card_value': card.card_value                   # Int
                }
            }    

        if 'board_cards' not in self._board_snapshot:
            self._board_snapshot['board_cards'] = []
        self._board_snapshot['board_cards'].append(card_data)

    def _update_top_card(self, card: Card) -> None:
        """ Update game context with last played card (on board). 
            While this can be inferred from the whole board[-1], it's kept for ease of use. """

        card_data = {
            'card_type': card.card_type.value,
            'card_data': {
                'color': card.color.value,                      # Enum to string
                'card_type': card.card_type.value,              # Enum to string
                'card_value': card.card_value                   # Int
            }
        }

        self._topcard_snapshot['top_card'] = card_data
   
    def get_complete_snapshot(self) -> Dict[str, Any]:
        """ Get complete serializable snapshot for save/load. """
        return {
            'rules': self._rule_snapshot,
            'deck_config': self._deck_config_snapshot,
            'players': self._players_snapshot,
            'top_card': self._topcard_snapshot,
            'player_hands': self._hand_per_player_snapshot,
            'deck': self._deck_snapshot,
            'board': self._board_snapshot,
            'last_updated': self._last_updated.isoformat()
        }

    def print_complete_snapshot(self) -> None:
        """ Temporarily method: Prints the complete snapshot. 
            Purely for testing/demonstrtation purposes. 
            In the future, this will be a method that dumps the snapshot to a JSON for example. """
        serialized_snapshot = self.get_complete_snapshot()
        for data, values in serialized_snapshot.items():
            print(f"TOPIC: {data} \n ----- \n {values}\n\n")
