"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: Noble McGregor

AI Usage: AI helped me find out how to create and use directives when saving files and how to use various errors

This module handles character creation, loading, and saving.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)

# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================


def create_character(name, character_class):
    """
    Create a new character with stats based on class
    
    Valid classes: Warrior, Mage, Rogue, Cleric
    
    Returns: Dictionary with character data including:
            - name, class, level, health, max_health, strength, magic
            - experience, gold, inventory, active_quests, completed_quests
    
    Raises: InvalidCharacterClassError if class is not valid
    """
    base_stats = {
        "Warrior": {"health": 150, "strength": 20, "magic": 5},     
        "Mage": {"health": 80, "strength": 5, "magic": 20},
        "Rogue": {"health": 110, "strength": 10, "magic": 7},
        "Cleric": {"health": 90, "strength": 8, "magic": 10}
    }
    classes = ["Warrior", "Mage", "Rogue", "Cleric"]
    
    if character_class not in classes:
        raise InvalidCharacterClassError(f"{character_class} is not a valid class, please choose 'Warrior', 'Mage', 'Rogue', or 'Cleric' ")
   
    stats = base_stats[character_class]
    
    character = {
        "name": name,
        "class": character_class,
        "level": 1,
        "health": stats["health"],
        "max_health": stats["health"],
        "strength": stats["strength"],
        "magic": stats["magic"],
        "experience": 0,
        "gold": 100,
        "inventory": [],
        "active_quests": [],
        "completed_quests": []
    }
    
    return character
    pass

def save_character(character, save_directory="data/save_games"):
    """
    Save character to file
    
    Filename format: {character_name}_save.txt
    
    File format:
    NAME: character_name
    CLASS: class_name
    LEVEL: 1
    HEALTH: 120
    MAX_HEALTH: 120
    STRENGTH: 15
    MAGIC: 5
    EXPERIENCE: 0
    GOLD: 100
    INVENTORY: item1,item2,item3
    ACTIVE_QUESTS: quest1,quest2
    COMPLETED_QUESTS: quest1,quest2
    
    Returns: True if successful
    Raises: PermissionError, IOError (let them propagate or handle)
    """
    if not isinstance(character, dict) or "name" not in character:
        return False
    if not os.path.exists(save_directory):
        os.makedirs(save_directory, exist_ok=True)
    
    file_name = os.path.join(save_directory, f"{character['name']}_save.txt")
    
    try:
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(f"Name: {character['name']}\n")
            file.write(f"Class: {character['class']}\n")
            file.write(f"Level: {character['level']}\n")
            file.write(f"Health: {character['health']}\n")
            file.write(f"Max_Health: {character['max_health']}\n")
            file.write(f"Strength: {character['strength']}\n")
            file.write(f"Magic: {character['magic']}\n")
            file.write(f"Experience: {character['experience']}\n")
            file.write(f"Gold: {character['gold']}\n")
            file.write(f"Inventory: {','.join(character['inventory'])}\n")
            file.write(f"Active_Quests: {','.join(character['active_quests'])}\n")
            file.write(f"Completed_Quests: {','.join(character['completed_quests'])}\n")
        
        return True

    except (PermissionError, IOError):     
        raise
    pass


def load_character(character_name, save_directory="data/save_games"):
    """
    Load character from save file
    
    Args:
        character_name: Name of character to load
        save_directory: Directory containing save files
    
    Returns: Character dictionary
    Raises: 
        CharacterNotFoundError if save file doesn't exist
        SaveFileCorruptedError if file exists but can't be read
        InvalidSaveDataError if data format is wrong
    """

    file_name = os.path.join(save_directory, f"{character_name}_save.txt")
    if not os.path.exists(file_name):
        raise CharacterNotFoundError(f"No save file found for {character_name}")
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except (PermissionError, IOError):
        raise SaveFileCorruptedError(f"Could not read file for {character_name}")

    character = {}
    try:
        for line in lines:
            key, value = line.strip().split(":", 1)
            key = key.strip()
            value = value.strip()
            
            if key in ["Level", "Health", "Max_Health", "Strength", "Magic", "Experience", "Gold"]:
                character[key.lower()] = int(value)
            elif key in ["Inventory", "Active_Quests", "Completed_Quests"]:
                character[key.lower()] = value.split(",") if value else []
            elif key in ["Name", "Class"]:
                character[key.lower()] = value
            else:
                raise InvalidSaveDataError(f"Wrong field {key} in save file.")
        
        fields = [
            "name", "class", "level", "health", "max_health", "strength", "magic", 
            "experience", "gold", "inventory", "active_quests", "completed_quests"
        ]
        for field in fields:
            if field not in character:
                raise InvalidSaveDataError(f"Missing {field} in save file")

    except ValueError:
        raise InvalidSaveDataError("Save file format is invalid")
    
    return character
    pass

def list_saved_characters(save_directory="data/save_games"):
    """
    Get list of all saved character names
    
    Returns: List of character names (without _save.txt extension)
    """
    if not os.path.exists(save_directory):
        return []
    
    try:
        file = os.listdir(save_directory)
    except (PermissionError, IOError):
        raise
    
    save_list = [f for f in file if f.endswith("_save.txt")]
    
    saved_character = [f.replace("_save.txt", "") for f in save_list]
    
    return saved_character
    pass

def delete_character(character_name, save_directory="data/save_games"):
    """
    Delete a character's save file
    
    Returns: True if deleted successfully
    Raises: CharacterNotFoundError if character doesn't exist
    """
    file_name = os.path.join(save_directory, f"{character_name}_save.txt")
    if not os.path.exists(file_name):
        raise CharacterNotFoundError
    
    try:
        os.remove(file_name)
        return True
    except (PermissionError, IOError):
        raise
    pass

# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    """
    Add experience to character and handle level ups
    
    Level up formula: level_up_xp = current_level * 100
    Example when leveling up:
    - Increase level by 1
    - Increase max_health by 10
    - Increase strength by 2
    - Increase magic by 2
    - Restore health to max_health
    
    Raises: CharacterDeadError if character health is 0
    """
    if character["health"] <= 0:
        raise CharacterDeadError(f"{character["name"]} is dead")

    character["experience"] += xp_amount

    while character["experience"] >= character["level"] * 100:
        character["experience"] -= character["level"] * 100
        character["level"] += 1
        character["max_health"] += 10
        character["strength"] += 2
        character["magic"] += 2
        character["health"] = character["max_health"]

    return character
    pass

def add_gold(character, amount):
    """
    Add gold to character's inventory
    
    Args:
        character: Character dictionary
        amount: Amount of gold to add (can be negative for spending)
    
    Returns: New gold total
    Raises: ValueError if result would be negative
    """
    total_gold = character["gold"] + amount

    if total_gold < 0:
        raise ValueError(f"{character["name"]} can not have less than 0 gold")
    character["gold"] = total_gold
    return total_gold
    pass

def heal_character(character, amount):
    """
    Heal character by specified amount
    
    Health cannot exceed max_health
    
    Returns: Actual amount healed
    """
    health = character["max_health"] - character["health"]
    healing = min(amount, health)

    character["health"] += healing
    return healing
    pass

def is_character_dead(character):
    """
    Check if character's health is 0 or below
    
    Returns: True if dead, False if alive
    """
    if character["health"] <= 0:
        return True
    else:
        return False
    pass
    
def revive_character(character):
    """
    Revive a dead character with 50% health
    
    Returns: True if revived
    """
    if character["health"] <= 0:
        character["health"] = character["max_health"] // 2
        return True

    return False
    pass

# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    """
    Validate that character dictionary has all required fields
    
    Required fields: name, class, level, health, max_health, 
                    strength, magic, experience, gold, inventory,
                    active_quests, completed_quests
    
    Returns: True if valid
    Raises: InvalidSaveDataError if missing fields or invalid types
    """
    fields = [
            "name", "class", "level", "health", "max_health", "strength", "magic", 
            "experience", "gold", "inventory", "active_quests", "completed_quests"
        ]
    for field in fields:
        if field not in character:
            raise InvalidSaveDataError(f"Missing {field} in save file")
    
    numeric_values = ["level", "health", "max_health", "strength", "magic", "experience", "gold"]
    for field in numeric_values:
        if not isinstance(character[field], int):
            raise InvalidSaveDataError
        
    list_values = ["inventory", "active_quests", "completed_quests"]
    for field in list_values:
        if not isinstance(character[field], list):
            raise InvalidSaveDataError
    return True
    pass

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")
    
    # Test character creation
    try:
        char = create_character("TestHero", "Warrior")
        print(f"Created: {char['name']} the {char['class']}")
        print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
    except InvalidCharacterClassError as e:
        print(f"Invalid class: {e}")
    
    # Test saving
    try:
       save_character(char)
       print("Character saved successfully")
    except Exception as e:
        print(f"Save error: {e}")
    
    # Test loading
    try:
       loaded = load_character("TestHero")
       print(f"Loaded: {loaded['name']}")
    except CharacterNotFoundError:
       print("Character not found")
    except SaveFileCorruptedError:
       print("Save file corrupted")

