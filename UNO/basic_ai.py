from typing import TYPE_CHECKING
from collections import Counter
from random import randint
from UNO.game_constants import CardType, EffectCategory, Color

if TYPE_CHECKING:
    from UNO.card import Card


class AI:
    """ Static class that holds methods used to direct AI behaviour.  """

    @staticmethod
    def auto_select_color(game_context) -> Color:
        """ Auto-select color based on current player's hand. """
        current_player = game_context.tm.get_current_player()
        hand = current_player.hand.get_hand()
        hand_colors = [card.color for card in hand if card.color is not Color.COLORLESS]
        
        if hand_colors:
            # Choose most common color in hand
            most_commmon_color = Counter(hand_colors).most_common(1)[0][0]
            return most_commmon_color 
        
        # Fallback to red
        return Color.RED
    
    @staticmethod
    def get_playable_cards(game_context) -> list | None:
        """ Get a list of cards that are all validated and are all legal moves. 
            If None is returned, there are no legal moves.  """

        player = game_context.tm.get_current_player()
        hand = player.hand.get_hand()

        # Filter playable cards
        playable_cards = [card for card in hand if game_context.engine.validate_play(card)]
        
        if not playable_cards:
            return None  # No valid moves
        
        return playable_cards


        #. TO FIX TYPE HINTING -->>>>>>>>>>>>>>>>>>>>>>>
    @staticmethod
    def pick_card(game_context, playable_cards: list):
        """ Simple AI with some startegy mechanics. 

            Mechanics
            - Bully Strategy: If a draw +2, +4, or +x card was played, add another draw card to the pile.
            - MAIN Strategy: Play to your most common color and play a regular color over a wild color
            - MAIN Strategy: If 2 color types are left in your hand, play the ACTION/WILD card to prevent
              a potential draw next turn (depends on gamerules)
            - Requires no validation: only valid plays are considered and inserted into cards. 
             """

        cards = playable_cards # Only contains valid plays and cannot be empty.
        topcard = game_context.board.show_top_card_on_board()
        
        # ==== Bully Strategy ====
        # Try to stack a draw card for the next player on a recently played draw card
        # -> Step 1: Check if attribute exists for Card (not for Number cards)
        if topcard is not None: # Requires None check for hasattr       
            if hasattr(topcard, "effect_types"):  
                # -> Step 2: Check if card contains DRAW category (default: +2 and +4 cards)
                if EffectCategory.DRAW in topcard.effect_types:
                    try:
                        stackable_draw_cards_list: list[Card] = [card for card in cards if EffectCategory.DRAW in card.effect_types]
                        random_int = randint(0, len(stackable_draw_cards_list) - 1)
                        stackable_draw_card: Card = stackable_draw_cards_list[random_int]
                        return stackable_draw_card
                    except ValueError:
                        # Empty list, no cards to play.
                        pass

        # ==== Prevent Final Draw Strategy ====
        # Try to avoid having ACTION/WILD as last card to prevent potential draw next turn
        # -> Step 1: Check if this rule is active
        if not game_context.rules.ALLOW_FINAL_SPECIAL_CARD:
            card_type_count = Counter(card.card_type for card in cards)
            number_cards = [card for card in cards if card.card_type == CardType.NUMBER]
            # -> Step 2: Check if 1 number card is one of the 2 final TYPES of cards
            if len(number_cards) == 1 and sum(card_type_count.values()) == 2:
                non_number_cards = [card for card in cards if card.card_type != CardType.NUMBER]
                
                # -> Step 3: Random select from list
                if non_number_cards:
                    random_int = randint(0, len(non_number_cards) - 1)
                    non_number_card = non_number_cards[random_int]
                    return non_number_card
        
        # ==== MAIN Strategy ====
        # Play the most common color card
        # ->  Step 1: Count most common color
        color_count = Counter(card.color for card in cards)        
        most_common_color: Color = color_count.most_common(1)[0][0]

        # -> Step 2: Ceate list with the cards with most common color
        most_common_cards = [common_card for common_card in cards if common_card.color == most_common_color]
        
        # -> Step 3: Random select from list
        if most_common_cards:
            random_int = randint(0, len(most_common_cards) - 1)
            return most_common_cards[random_int]
        
        # Defensive fallback: play any card
        return cards[randint(0, len(cards) - 1)]








        