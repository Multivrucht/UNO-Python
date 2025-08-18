from datetime import datetime
from typing import TYPE_CHECKING
from UNO.game_constants import CardType, GameEvent
from UNO.player import Player
from UNO.board import Board
from UNO.card import Card
from UNO.deck import Deck
from UNO.deck_builder import DeckBuilder

if TYPE_CHECKING:
    from UNO.game import Game

class GameEngine:
    """ Encapsulates game rules & core mechanics. 

        Current & future design:
        The GameEngine is manages the card- & gamemechanics, including the majority of the game rule validations.
        Currently, the card effect validation & execution is still encapsuilated in the card classes. This is due to an older
        refacator that hasn't been fully moved to the game engine, but for now I like to keep it in the card class.
        Due to the current CLI nature, it handles basic print messages, but that may change if I add a GUI. """
    def __init__(self, deck: Deck, board: Board, game_context: 'Game'):
            self._deck = deck
            self._board = board

            # Only used when required to notify observers or access global state
            self._game_context = game_context  

    def validate_play(self, card_to_validate: Card) -> bool:
        """" Method to validate whether the chosen card is a legal move. """
        top_card_on_board: Card | None = self._board.show_top_card_on_board()
        
        # Check if board is empty
        if top_card_on_board is None:
            return True
        
        try:
            # if card_to_validate.effective_color == top_card_on_board.effective_color if top_card_on_board.effective_color is not None else top_card_on_board.color:
            if card_to_validate.effective_color == top_card_on_board.effective_color:
                if card_to_validate.can_execute_effect(self._game_context):
                    return True     # Match by effective color
            if card_to_validate.card_type == CardType.NUMBER:
                if card_to_validate.card_value == top_card_on_board.card_value:
                    return True     # Match by number
            if card_to_validate.card_type in self._game_context.deck_config.WILD_CARDS:
                if card_to_validate.can_execute_effect(self._game_context):
                    return True     # Match by Wild Card (and effect is legal)
            return False            # No Match
        except AttributeError as e:
            print(f'Validation error: Incorect card attribute: {e}')
            return False
        except ValueError as e:
            print(f'Validation error: Invalid card value: {e}')
            return False
        except Exception as e:
            print(f'Validation error: Unexpected general error: {e}')
            return False
        
    def deal_cards(self, players: list[Player], cards_per_player: int = 7 ) -> None:
        """ Deal x cards to each player. """
        if not isinstance(cards_per_player, int) or cards_per_player <= 0:
            print(f"Warning: Invalid cards_per_player value '{cards_per_player}'. Using default value 7.")
            cards_per_player = 7
        for player in players:
            self.player_draw_card(player, cards_per_player)

    def execute_card_play(self, player: Player, card: Card) -> None:
        """ Execute a validated card play with all side effects. """
        
        # Step 1: Update game_context state
        self._board.add_card_to_board(card)


        # Dirty fix, prevents skip turn effects from altering current player.
        current_player = player

        # UI feedback
        color_display = (card.effective_color.value if card.effective_color is not None else card.color.value)
        print(
            f"--> {current_player.name} successfully played a {color_display}"
            f"{f' {card.card_value}' if card.card_value is not None else ''} {card.card_type.value}")
        # Step 2: Execute card effects
        card.execute_effect(self._game_context)


        # Remove Card
        current_player.hand.remove_card(card)
        
        # Observer notification
        event_data = {
            'card': card,
            'player': current_player,
            'timestamp': datetime.now()
        }

        # FIX OBSERVER
        self._game_context.notify_observers(GameEvent.CARD_PLAYED, event_data)

    def check_win_condition(self, player: Player) -> None:
        """ Check for UNO and win condition. """
        hand_size = len(player.hand.get_hand())
        if hand_size == 1: # Check for UNO
            print(f"{player.name}: UNO!")
        if hand_size == 0: # Check win condition
            print(f"{player.name} wins! \n Closing the game..")
            self._game_context.stop_game()

    def player_draw_card(self, player: Player, amount: int = 1) -> None:
        """ Makes a player draw a card x times. """
        cards_drawn = 0 
        no_draw_error = True    # Dirty fix, ensures either error or succes is printed. 
        
        for _ in range(amount):
            # Attempt to draw a card
            card = self._deck.draw_card()
            if not card:
                # Apply scenario strategies
                card = self._handle_empty_deck_scenario()
            if card:
                player.draw_card(card)
                cards_drawn += 1
                # if self._game_context.game_active:  # Dirty fix - prevents printing during game_context init
                #     print(f"{player.name} took a {card}") 
                if cards_drawn == amount:
                        if no_draw_error and self._game_context.game_active:  
                            print(f"* {player.name} took {cards_drawn} card(s)! *") 

                # Logic for the observer
                event_data = {
                'card': card,                       # Actual Card object
                'player': player,                   # Actual Player object
                'timestamp': datetime.now()}

                # Notify observer
                self._game_context.notify_observers(GameEvent.CARD_DRAWN, event_data)

            else:
                if cards_drawn < amount:
                    no_draw_error = False
                    print(f"Warning: {player.name} could only draw {cards_drawn} of {amount} requested cards")
                    break

    def _handle_empty_deck_scenario(self) -> Card | None:
        """ Handles empty deck scenario based on game rules. """

        # Strategy 1: Try deck recycling
        if self._deck.get_deck_length() == 0:
            self._deck.attempt_recycle_deck(self._board)
        try:
            return self._deck.draw_card()
        except IndexError:
            pass

        # Strategy 2: Check multiple deck rule
        if self._game_context.rules.ALLOW_MULTIPLE_DECKS:
            print("Adding another deck of cards..")
            try:
                DeckBuilder.populate_deck(self._game_context.deck_config, self._deck)
                print("New deck added..")
                return self._deck.draw_card()
            except IndexError:
                print("Failed to create deck/grab a card..")
                return None
                    
        print("No cards are available to draw..")
        return None