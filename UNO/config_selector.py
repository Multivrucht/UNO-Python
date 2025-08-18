from UNO.game_config import GameRulesEnum, DeckConfigEnum
from UNO.player import Player

class ConfigSelector:
    """ Simple configuration selection before game start. 
        To be replaced later by a GUI.. """
    

    @staticmethod
    def provide_default_game() -> tuple[list[Player], GameRulesEnum, DeckConfigEnum]:
        """ Returns a standard default game. """
        players = [Player('Player 1'), Player('Danielle', False), Player('Nick', False), Player('Jasper', False)]
        rules = GameRulesEnum.STANDARD
        deck_config = DeckConfigEnum.STANDARD
        return players, rules, deck_config

    @staticmethod
    def select_game_config() -> tuple[list[Player], GameRulesEnum, DeckConfigEnum]:
        """ Interactive configuration selection. """
        print("UNO Configuration Setup")
        print("=" * 30)
        
        setup_game = input("Do you want to configure the game settings? \nType y (yes). Type any other key to quickplay): ").strip()
        if setup_game == "y":

            # Select player names
            players = ConfigSelector._select_players()

            # Select rules
            rules = ConfigSelector._select_rules()
            
            # Select deck
            deck_config = ConfigSelector._select_deck()

            return players, rules, deck_config

        return ConfigSelector.provide_default_game()


    @staticmethod
    def _select_players() -> list:
        """ Choose your players """

        # Step 1: Get player count with validation
        while True:
            try:
                player_count = input("Select number of players (2-4): ").strip()
                player_count = int(player_count)
                if 2 <= player_count <= 4:
                    break
                else:
                    print("Please enter a number between 2 and 4")
            except ValueError:
                print("Please enter a valid number")
        
        # Step 2: Collect player names
        players = []
        for i in range(player_count):
            name = input(f"Enter name for player {i + 1} (press empty Enter to insert a NPC): ").strip()
            if name:  # Non-empty name provided
                players.append(Player(name))
            else:  # Empty name - use NPC
                npc_name = f"NPC_{i + 1}"
                players.append(Player(npc_name, False))
                print(f"  → Added {npc_name}")
        
        return players

    @staticmethod
    def _select_rules() -> GameRulesEnum:
        """ Select game rules. """
        print("\n Select Rules:")
        print("1. Standard UNO   (Default)")
        print("2. Hardcore Rules (Custom)")
               
        choice = input("Choose rules (1-2): ").strip()
        
        if choice == "2":
            return GameRulesEnum.HARDCORE  # Hardcore
        return GameRulesEnum.STANDARD  # Standard
    
    @staticmethod
    def _select_deck() -> DeckConfigEnum:
        """ Select deck configuration. """
        print("\n Select Deck:")
        print("1. Standard Deck (Default)")
        print("2. Hardcore Deck (Custom)")
        print("3. (DEV) Testing Deck")
        print("4. (DEV) Intentionally Broken Deck")
        
        choice = input("Choose deck (1-2): ").strip()
        
        if choice == "2":
            return DeckConfigEnum.HARDCORE
        if choice == "3":
            return DeckConfigEnum.TESTDECK
        if choice == "4":
            return DeckConfigEnum.BROKENDECK
        return DeckConfigEnum.STANDARD