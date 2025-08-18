from UNO.player import Player
from UNO.game_constants import GameEvent

class TurnManager():
    """ Turn manager abstracts turn logic for the game class. """
    
    def __init__(self, players: list) -> None:
        self._players = players
        self._current = 0 # use dictionary later for better turn management...
        self._observers = []
        self._clockwise = True
    
    def get_next_player(self) -> Player:
        """ Controlled access to next player. """
        if self._clockwise is True:
            next_player = (self._current + 1) % len(self._players)
        else:
            next_player = (self._current - 1) % len(self._players)
        return self._players[next_player]
    
    # def start_turn(self):
    #     # Apply post-turn or targeted (?) effects

    #     # TURN_TIMER = False
    #     # if TURN_TIMER:
    #     #     import time
    #     #     seconds = 30
    #     #     time.sleep(seconds)

    
    def get_current_player(self) -> Player:
        """ Controlled access to current player. """
        return self._players[self._current] # this is incorrect, since __ indicates it should not be accessed, right?

    def end_turn(self) -> None:
        """ End player's turn. """
        if self._clockwise is True:
            self._current = (self._current + 1) % len(self._players)
        else:
            self._current = (self._current - 1) % len(self._players)

        # Observer logic
        current_player = self.get_current_player
        self.notify_observers(GameEvent.PLAYER_TURN_CHANGED, {'player': current_player})

    def reverse_play_order(self) -> None:
        """ Reverse the play order. """
        if self._clockwise is True:
            self._clockwise = False
        else:
            self._clockwise = True

        # Observer logic
        turn_order = self._clockwise
        self.notify_observers(GameEvent.TURN_ORDER_CHANGED, {'turn_order': turn_order})

    def skip_turn(self) -> None:
        """ Skip the next player.
            Due to placement in card logic, this gets called on top of end_turn.
            - This mechanic will be refactored when refactoring the game loop.  """
        self.end_turn()

    def subscribe(self, observer):
        """ Subscribe as a observer. """
        self._observers.append(observer)

    def notify_observers(self, event, data):
        """ Notify all subscribed observers. """
        for observer in self._observers:
            observer.on_game_event(event, data)

