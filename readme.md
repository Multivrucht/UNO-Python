**UNO Card Game**

A Python implementation of the classic UNO card game, designed with clean architecture and object-oriented principles. This project holds the core logic of the game which will later be refactored into a multiplayer variant. 

Current version: V0.1

**Project Disclaimer:**
- Built using Python 3.15.5
- This project was built as a learning experience; the usage of AI assisted coding was very limited
- This is an early version


**Project Overview**
This project implements the UNO card game with support for:

- Human players and AI opponents
- Selecting and creating unique game configurations, which include:
  - Different game rules you can customize which impact the core gameplay
  - Ability to pick & create different decks
  - Built-in custom configuration error checking and correction
- Command-line interface (for now!)
- Event-driven architecture, using an "observer pattern" to track game events
- The implementation focuses on modularity, extensibility, and clean code practices (check the limitations section)

**Current Limitations**
- Text-Only Interface: Currently only works in command-line, which isn't very exciting visually. Will be refactored later on to include UI.
- Error messages: These are mostly print based due to the current UI nature
- Typehinting errors: While the code works correctly and has proper failsafes, some typehint errors might indicate some less optimal code, fixing this would be right thing to do
- Better interfacing for main game object: The main game object is passed on more than I like as an object, which is dangerous and should be avoided. This requires proper interfacing.
- Save/loading: Currently partially implemented
- Card effect validation: Currently effect validaiton is in the card class, not in the validation method. This is a refactor relic of a previous implementation decision
- Builder/factory: Not properly implemented the builder and factory pattern, does not support extensibility of new cards


**Refactor Plans:**
- Better interface separation
- Consolidate card validation game logic
- Proper factory and builder methods for card generation
- Consistent error handking
- Separate card effect handling
- Multiplayer: Improve gamestates + observer pattern to support multiplayer
- Multiplayer: Remove all console messages and replace with proper UI feedback


**Planned Features:**
- Adding a HTML/CSS/Vanilla JS frontend + FASTAPI backend
- Multiplayer support
- Runtime rule changes
- Packaging upon release
- Cheating options, because why not
