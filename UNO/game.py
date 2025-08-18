import time
from random import randrange
from UNO.player import Player
from UNO.board import Board
from UNO.card import Card
from UNO.deck_builder import DeckBuilder
from UNO.turn_manager import TurnManager
from UNO.game_constants import GameState, GameEvent
from UNO.game_observer import GameContext, GameObserver
from UNO.game_config import GameRulesEnum, DeckConfigEnum
from UNO.basic_ai import AI
from UNO.game_engine import GameEngine

class Game:
    """ Game class, the orchestrator of the game session.

        Responsibilities:
        - Starts, stops, and manages the main game loop and session.
        - Handles player and AI turns (but delegates turn management)
        - Coordinates interaction between components (e.g., Deck, Board, GameEngine).
        - Handles majority of user input and high-level UI flow.


        Currently:
        - Still a little too tightly coupled: Instance gets passed as variable a little too much for my liking (but due scoping not fixed yet..)
    """

    def __init__(self, player_names: list[Player], rules: GameRulesEnum , deck_config: DeckConfigEnum):
        self.__observers: list[GameObserver] = []
        self.game_active = False

        # Get configuration
        self.rules = rules.value                # Unpacked Enum of type GameRules - Tightly coupled in game mechanics
        self.deck_config = deck_config.value    # Unpacked Enum of type DeckConfiguration - - Tightly coupled in game mechanics
        self.players = player_names             # List of Player objects
        
        # Create an empty board & deck
        self.deck =  DeckBuilder.create_deck()
        self.board = Board()
       
        # Create GameEngine & Turnmanager
        self.engine = GameEngine(self.deck, self.board, self)
        self.tm = TurnManager(self.players)

        # Observer class
        self.gc = GameContext(self)

        # Populate Deck with selected config
        DeckBuilder.populate_deck(self.deck_config, self.deck)
        print(f"> Total deck length: {self.deck.get_deck_length()}")

        # Deal cards according to the rules
        self.engine.deal_cards(self.players, self.rules.STARTING_HAND_SIZE)
        
    def _handle_user_main_menu(self, player: Player) -> GameState | None:
        """ Handle main menu interactions with clear escape paths. """
        print("Options: [1] Draw card, [2] Play card, [3] Quit game")

        action = input("Choose action (or 'b' to see options again)\nSelection: ")
        
        match action:
            case '1':
                self.engine.player_draw_card(player)
                # self.engine.player_draw_card(player, self.rules.DRAW_PENALTY)
                return GameState.END_TURN  # Return to menu after draw
            case '2':
                return GameState.CARD_SELECTION  # Transition to card selection
            case '3' | 's':
                print("Exiting game..")
                self.stop_game()
            case 'b':
                return GameState.MAIN_MENU  # Refresh menu
            case _:
                print("Invalid option. Try again.")
                return GameState.MAIN_MENU
    
    def _get_card_from_user_input(self, player: Player) -> str | None:
        """Handle user input collection with UI feedback. Returns None if user cancels."""
        
        print("\nCard Selection Mode")
        print(player.hand.show_hand())
        print(f"Top card: {self.board.show_top_card_on_board() or 'None (first play)'}")
        print("Choose a card to play, or type 'b' to go back to main menu")
        
        action = input("Selection: ").strip()
        
        if action == 'b':
            return None  # Signal cancellation
        return action
        
    def _resolve_card_from__user_input(self, player: Player, user_input: str) -> Card | None:
        """ Converts user input to a card.  """
        
        try:
            action_int = int(user_input)
            return player.hand.select_card(action_int)
        except ValueError:
            return None  # Invalid input format
        except IndexError:
            return None  # Invalid card index   
    
    def _human_card_selecion_loop(self, player: Player) -> GameState:

        while True:
            # Step 1: Get user input
            user_input = self._get_card_from_user_input(player)
            if user_input is None:
                return GameState.MAIN_MENU  # User cancelled
            
            # Step 2: Convert to card
            selected_card = self._resolve_card_from__user_input(player, user_input)
            if selected_card is None:
                print("Invalid selection. Please try again.")
                continue  # Retry input
            
            # Step 3: Validate play
            if not self.engine.validate_play(selected_card):
                print("Illegal move. Try another card or go back ('b').")
                continue  # Retry input
            
            # Step 4: Execute valid play
            self.engine.execute_card_play(player, selected_card)

            return GameState.END_TURN
          
    def _handle_human_turn(self, player: Player) -> None:
        """ Handle complete human turn with state management. """
        
        game_state = GameState.MAIN_MENU
        # Later introduce the validation mechanic beforehand here as well
        # Right now its more engaging to not do that to be honest
        while game_state != GameState.END_TURN and self.game_active:
            if game_state == GameState.MAIN_MENU:
                game_state = self._handle_user_main_menu(player)
            elif game_state == GameState.CARD_SELECTION:
                game_state = self._human_card_selecion_loop(player)

    def _handle_ai_turn(self, player: Player) -> None:
        """ Handle AI turn, skipping the human I/O parts. """
        
        time.sleep(randrange(1, 3))
        
        # Get a list of playable (validated) cards
        playable_cards = AI.get_playable_cards(self)
        if playable_cards is None:
            self.engine.player_draw_card(player)
            # self.engine.player_draw_card(player, self.rules.DRAW_PENALTY)
        else:
            selected_card = AI.pick_card(self, playable_cards)
            self.engine.execute_card_play(player, selected_card)

    def play(self) -> None:
        """ The main loop of the game. """
        self.game_active = True
        print("==> GAME STARTED! <== \n")
        try:
            while self.game_active:
                player = self.tm.get_current_player()
                print(f"\n<< It's {player.name}'s turn! >>")

                if not player.is_human_controlled():
                    self._handle_ai_turn(player)
                else:
                    self._handle_human_turn(player)

                if self.game_active:
                    self.engine.check_win_condition(player)
                    # Signals to end current players turn
                    self.tm.end_turn() 
                
                # To be replaced
                # self.gc.print_complete_snapshot()

        except KeyboardInterrupt:
            print("\nGame interrupted by user. Exiting game...")
            action = input("Type to stop: 's' or to continue: 'c': ")
            if action == "c":
                self.play()
            if action != "c":
                self.stop_game()     

    def stop_game(self) -> None:
        """Stop the game"""
        self.game_active = False
        
    def subscribe(self, observer: GameObserver) -> None:
        """ Subscribe as observer. """
        self.__observers.append(observer)
    
    def notify_observers(self, event: GameEvent, data: dict[str, set]) -> None:
        """ Notify all subscribed observers """
        for observer in self.__observers:
            observer.on_game_event(event, data)
