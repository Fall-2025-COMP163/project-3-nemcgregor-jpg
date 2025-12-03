"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: Noble McGregor

AI Usage: [Document any AI assistance used]

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# python -m pytest tests/test_exception_handling.py -v
# python -m pytest tests/test_module_structure.py -v
# python -m pytest tests/test_game_integration.py -v




# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
import random
from custom_exceptions import *
# ============================================================================
# GAME STATE
# ============================================================================

# Global variables for game data
current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    """
    Display main menu and get player choice
    
    Options:
    1. New Game
    2. Load Game
    3. Exit
    
    Returns: Integer choice (1-3)
    """
    while True:
        print("=== Main Menu ===")
        print("1. New Game")
        print("2. Load Game")
        print("3. Exit")

        choice = input("Enter your choice 1-3: ")

        if choice in ["1", "2", "3"]:
            return int(choice)
        else:
            print("Invalid choice,enter 1, 2, or 3")
    pass

def new_game():
    """
    Start a new game
    
    Prompts for:
    - Character name
    - Character class
    
    Creates character and starts game loop
    """
    global current_character
    
    name = input("Enter character name: ")

    character_class = input("Enter characters class (Warrior, Mage, Rogue, or Cleric): ")

    try:
        current_character = character_manager.create_character(name, character_class)
        print(f"Character '{name}' the {character_class} created successfully!")
        return current_character

    except InvalidCharacterClassError:
        print(f" '{character_class}' is not a valid class. Please try again.")
        return None
    pass

def load_game():
    """
    Load an existing saved game
    
    Shows list of saved characters
    Prompts user to select one
    """
    global current_character
    
    saved_characters = character_manager.list_saved_characters()

    if not saved_characters:
        print("No saved games found")
        return None

    print("SAVED CHARACTERS")
    for index, char_name in enumerate(saved_characters, start=1):
        print(f"{index}. {char_name}")

    while True:
        choice = input("Enter the number of the character you want to choose:").strip()
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(saved_characters):
                selected_name = saved_characters[choice - 1]
                try:
                    current_character = character_manager.load_character(selected_name)
                    print(f"Character '{selected_name}' loaded")
                    return current_character
                except CharacterNotFoundError:
                    print(f"Character '{selected_name}' not found")
                    return None
                except SaveFileCorruptedError:
                    print(f"Save file for '{selected_name}' corrupted")
                    return None
            else:
                print("Invalid, please select a valid number")
        else:
            print("Invalid please enter a valid number")
    pass

# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """
    Main game loop - shows game menu and processes actions
    """
    global game_running, current_character
    
    game_running = True
    
    while game_running:
        choice = game_menu()

        if choice == 1:
            print("CHARACTER STATS")
            for stat, value in current_character.items():
                if stat not in ["inventory", "equipped_weapon", "equipped_armor"]:
                    print(f"{stat}: {value}")

        elif choice == 2:
            print("INVENTORY")
            if current_character.get("inventory"):
                for item in current_character["inventory"]:
                    print(f"- {item}")
            else:
                print("Inventory is empty")

        elif choice == 3:
            print("QUEST MENU")

        elif choice == 4:
            print("EXPLORATION")

        elif choice == 5:
            print("SHOP")

        elif choice == 6:
            print("SAVING GAME")
            print("Game saved succesfully")
            game_running = False
    pass

def game_menu():
    """
    Display game menu and get player choice
    
    Options:
    1. View Character Stats
    2. View Inventory
    3. Quest Menu
    4. Explore (Find Battles)
    5. Shop
    6. Save and Quit
    
    Returns: Integer choice (1-6)
    """
    while True:
        print("GAME MENU")
        print("1. View Character Stats")
        print("2. View Inventory")
        print("3. Quest Menu")
        print("4. Explore (Find Battles)")
        print("5. Shop")
        print("6. Save and Quit")

        choice = input("Enter a number 1-6: ")

        if choice in ["1", "2", "3", "4", "5", "6"]:
            return int(choice)
        else:
            print("Invalid please enter a number between 1 and 6")
    pass

# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character information"""
    global current_character
    
    print("CHARACTER STATS")
    print(f"Name: {current_character.get("name")}")
    print(f"Class: {current_character.get("class")}")
    print(f"Level: {current_character.get("level", 1)}")
    print(f"Health: {current_character.get("health", 0)}/{current_character.get('max_health', 0)}")
    print(f"Strength: {current_character.get("strength", 0)}")
    print(f"Magic: {current_character.get("magic", 0)}")
    print(f"Gold: {current_character.get("gold", 0)}")

    print("QUEST PROGRESS")
    quest_handler.display_progress(current_character)
    pass

def view_inventory():
    """Display and manage inventory"""
    global current_character, all_items
    
    while True:
        print("INVENTORY")
        if not current_character.get("inventory"):
            print("Inventory is empty")
        else:
            for index, item_id in enumerate(current_character["inventory"], start=1):
                item_info = all_items.get(item_id, {})
                item_name = item_info.get("name", item_id)
                item_type = item_info.get("type", "Unknown")
                print(f"{idx}. {item_name} ({item_type})")

        print("OPTIONS")
        print("1. Use Item")
        print("2. Equip Weapon or armor")
        print("3. Drop Item")
        print("4. Game Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            item_choice = input("Enter item number to use: ")
            if item_choice.isdigit():
                idx = int(item_choice) - 1
                if 0 <= idx < len(current_character["inventory"]):
                    item_id = current_character["inventory"][idx]
                    try:
                        inventory_system.use_item(current_character, item_id, all_items)
                        print(f"Used {all_items[item_id]['name']}.")
                    except Exception as e:
                        print(f"Could not use item: {e}")
                else:
                    print("Invalid item number.")
            else:
                print("Invalid input")

        elif choice == "2":
            item_choice = input("Enter item number to equip: ")
            if item_choice.isdigit():
                index = int(item_choice) - 1
                if 0 <= index < len(current_character["inventory"]):
                    item_id = current_character["inventory"][index]
                    try:
                        if all_items[item_id]["type"] == "weapon":
                            inventory_system.equip_weapon(current_character, item_id, all_items)
                            print(f"Equipped {all_items[item_id]['name']}.")
                        elif all_items[item_id]["type"] == "armor":
                            inventory_system.equip_armor(current_character, item_id, all_items)
                            print(f"Equipped {all_items[item_id]['name']}.")
                        else:
                            print("Item cannot be equipped")
                    except Exception as e:
                        print(f"Could not equip item: {e}")
                else:
                    print("Invalid item number")
            else:
                print("Invalid input")

        elif choice == "3":
            item_choice = input("Enter item number to drop: ")
            if item_choice.isdigit():
                index = int(item_choice) - 1
                if 0 <= index < len(current_character["inventory"]):
                    item_id = current_character["inventory"][index]
                    try:
                        inventory_system.drop_item(current_character, item_id)
                        print(f"Dropped {all_items[item_id]['name']}.")
                    except ItemNotFoundError:
                        print("Item not found in inventory")
                else:
                    print("Invalid item number")
            else:
                print("Invalid input")

        elif choice == "4":
            break
        else:
            print("Invalid, please try again")
    pass

def quest_menu():
    """Quest management menu"""
    global current_character, all_quests

    while True:
        print("QUEST MENU")
        print("1. View Active Quests")
        print("2. View Available Quests")
        print("3. View Completed Quests")
        print("4. Accept Quest")
        print("5. Abandon Quest")
        print("6. Complete Quest (for testing)")
        print("7. Back")

        choice = input("Enter your choice 1-7:")

        if choice == "1":
            print("ACTIVE QUEST")
            quest_handler.view_active(current_character)

        elif choice == "2":
            print("AVAILABLE QUEST")
            quest_handler.view_available(all_quests, current_character)

        elif choice == "3":
            print("COMPLETED QUEST")
            quest_handler.view_completed(current_character)

        elif choice == "4":
            quest_id = input("Enter quest ID to accept: ")
            try:
                quest_handler.accept_quest(current_character, quest_id, all_quests)
                print(f"Quest '{quest_id}' accepted")
            except QuestNotFoundError:
                print("Quest not found")

        elif choice == "5":
            quest_id = input("Enter quest ID to abandon: ")
            try:
                quest_handler.abandon_quest(current_character, quest_id)
                print(f"Quest '{quest_id}' abandoned")
            except QuestNotFoundError:
                print("Quest not found among active quests")

        elif choice == "6":
            quest_id = input("Enter quest ID to complete: ")
            try:
                quest_handler.complete_quest(current_character, quest_id)
                print(f"Quest '{quest_id}' completed")
            except QuestNotFoundError:
                print("Quest not found")

        elif choice == "7":
            break
        else:
            print("Invalid please enter a number between 1 and 7")
    pass

def explore():
    """Find and fight random enemies"""
    global current_character
    
    print("\n--- Exploration ---")
    try:
        level = current_character.get("level", 1)
        enemy = combat_system.generate_enemy(level)

        print(f"Encountered {enemy['name']} (Level {enemy['level']})")

        battle = combat_system.SimpleBattle(current_character, enemy)
        result = battle.start()

        if result == "victory":
            xp_gain = enemy.get("xp", 10)
            gold_gain = enemy.get("gold", 5)
            current_character["xp"] = current_character.get("xp", 0) + xp_gain
            current_character["gold"] = current_character.get("gold", 0) + gold_gain
            print(f"You defeated the {enemy['name']}! Gained {xp_gain} XP and {gold_gain} gold.")
        elif result == "defeat":
            print("You died, game over")
        else:
            print("The battle ended unexpectedly")

    except Exception as e:
        print(f"Error occurred during exploration: {e}")
    pass

def shop():
    """Shop menu for buying/selling items"""
    global current_character, all_items
    
    while True:
        print("SHOP MENU")
        print(f"Gold: {current_character.get('gold', 0)}")
        print("Available items:")
        for item_id, item_info in all_items.items():
            print(f"- {item_info['name']} ({item_info['type']}) : {item_info['cost']} gold")

        print("OPTIONS")
        print("1. Buy Item")
        print("2. Sell Item")
        print("3. Back")

        choice = input("Enter your choice: ")

        if choice == "1":
            item_id = input("Enter item ID to buy: ")
            if item_id in all_items:
                try:
                    inventory_system.purchase_item(current_character, item_id, all_items[item_id])
                    print(f"Purchased {all_items[item_id]['name']}")
                except InsufficientResourcesError:
                    print("Not enough gold to buy this item.")
                except InventoryFullError:
                    print("Inventory is full.")
                except Exception as e:
                    print(f"Error purchasing item: {e}")
            else:
                print("Invalid item ID")

        elif choice == "2":
            item_id = input("Enter item ID to sell: ")
            if item_id in current_character.get("inventory", []):
                try:
                    inventory_system.sell_item(current_character, item_id, all_items[item_id])
                    print(f"Sold {all_items[item_id]['name']}!")
                except ItemNotFoundError:
                    print("Item not found in inventory")
                except Exception as e:
                    print(f"Error selling item: {e}")
            else:
                print("Item not in inventory")

        elif choice == "3":
            break
        else:
            print("Invalid choice, please try again")


    pass

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
    global current_character
    try:
        character_manager.save_character(current_character)
        print(f"Game saved for {current_character.get('name', 'Unknown')}.")
    except IOError as e:
        print(f"Error saving game: {e}")
    pass

def load_game_data():
    """Load all quest and item data from files"""
    global all_quests, all_items
    
    try:
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()
        print("Game data loaded successfully.")
    except MissingDataFileError:
        print("Data files missing, creating data files")
        game_data.create_default_data_files()
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()
    except InvalidDataFormatError:
        print("Data files corrupted or have wrong format")
        game_data.create_default_data_files()
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()
    except Exception as e:
        print(f"Error loading game data: {e}")
    pass

def handle_character_death():
    """Handle character death"""
    global current_character, game_running
    print("YOU DIED")
    print("OPTIONS:")
    print("1. Revive (costs 50 gold)")
    print("2. Quit")

    choice = input("Enter your choice: ")

    if choice == "1":
        if current_character.get("gold", 0) >= 50:
            current_character["gold"] -= 50
            character_manager.revive_character(current_character)
            print(f"{current_character.get('name', 'Unknown')} has been revived")
        else:
            print("Not enough gold to revive, game over")
            game_running = False
    elif choice == "2":
        print("Quitting game.")
        game_running = False
    else:
        print("Invalid choice, please try again")
    pass

def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!")
    print()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""
    
    # Display welcome message
    display_welcome()
    
    # Load game data
    try:
        load_game_data()
        print("Game data loaded successfully!")
    except MissingDataFileError:
        print("Creating default game data...")
        game_data.create_default_data_files()
        load_game_data()
    except InvalidDataFormatError as e:
        print(f"Error loading game data: {e}")
        print("Please check data files for errors.")
        return
    
    # Main menu loop
    while True:
        choice = main_menu()
        
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()

