from UNO.game_constants import Color

class UserInput:
    """ Utility class for getting user input. """
    
    @staticmethod
    def get_color_selection() -> Color:
        """Shared color selection logic"""
        selectable_colors = [color for color in Color if color != Color.COLORLESS]
        
        print("Choose color:")
        for i, color in enumerate(selectable_colors, 1):
            print(f"[{i}] {color.value}")
        
        try:
            choice = int(input("Selection: ")) - 1
            if 0 <= choice < len(selectable_colors):
                return selectable_colors[choice]
            else:
                return selectable_colors[0]
        except (ValueError, IndexError):
            return selectable_colors[0]
