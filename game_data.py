"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: Noble McGregor

AI Usage: AI helped me debug and understand how exceptions worked in this case

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file
    
    Expected format per quest (separated by blank lines):
    QUEST_ID: unique_quest_name
    TITLE: Quest Display Title
    DESCRIPTION: Quest description text
    REWARD_XP: 100
    REWARD_GOLD: 50
    REQUIRED_LEVEL: 1
    PREREQUISITE: previous_quest_id (or NONE)
    
    Returns: Dictionary of quests {quest_id: quest_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            file = f.read()
    except FileNotFoundError:
        raise MissingDataFileError(f"Quest file {filename} not found")
    except (PermissionError, OSError):
        raise CorruptedDataError(f"Quest file {filename} is corrupted or unreadable")

    sections = [section.strip() for section in file.split("\n\n") if section.strip()]
    quests = {}
    for section in sections:
        data = {}
        try:
            for line in section.splitlines():
                if ":" not in line:
                    raise InvalidDataFormatError(f"Invalid line format: {line}")
                key, value = line.split(":", 1)
                key = key.strip().upper()
                value = value.strip()

                if key == "QUEST_ID":
                    quest_id = value
                    data["quest_id"] = value
                elif key == "TITLE":
                    data["title"] = value
                elif key == "DESCRIPTION":
                    data["description"] = value
                elif key == "REWARD_XP":
                    data["reward_xp"] = int(value)
                elif key == "REWARD_GOLD":
                    data["reward_gold"] = int(value)
                elif key == "REQUIRED_LEVEL":
                    data["required_level"] = int(value)
                elif key == "PREREQUISITE":
                    data["prerequisite"] = None if value.upper() == "NONE" else value
                else:
                    raise InvalidDataFormatError(f"Not a real field: {key}")
            fields = ["quest_id", "title", "description", "reward_xp", "reward_gold", "required_level", "prerequisite"]
            for field in fields:
                if field not in data:
                    raise InvalidDataFormatError(f"Missing field: {field}")
            quests[quest_id] = data
           
           
        except ValueError:
            raise InvalidDataFormatError("Invalid data format")
        except InvalidDataFormatError:
            raise
        except Exception as e:
            raise CorruptedDataError(f"Corrupted Data error: {e}")
    
    return quests
    pass

def load_items(filename="data/items.txt"):
    """
    Load item data from file
    
    Expected format per item (separated by blank lines):
    ITEM_ID: unique_item_name
    NAME: Item Display Name
    TYPE: weapon|armor|consumable
    EFFECT: stat_name:value (e.g., strength:5 or health:20)
    COST: 100
    DESCRIPTION: Item description
    
    Returns: Dictionary of items {item_id: item_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            file = f.read()
    except FileNotFoundError:
        raise MissingDataFileError(f"Item file {filename} not found")
    except (PermissionError, OSError):
        raise CorruptedDataError(f"Item file {filename} is corrupted or unreadable")

    sections = [section.strip() for section in file.split("\n\n") if section.strip()]
    items = {}
    for section in sections:
        data = {}
        try:
            for line in section.splitlines():
                if ":" not in line:
                    raise InvalidDataFormatError(f"Invalid line format: {line}")
                key, value = line.split(":", 1)
                key = key.strip().upper()
                value = value.strip()

                if key == "ITEM_ID":
                    item_id = value
                    data["item_id"] = value
                elif key == "NAME":
                    data["name"] = value
                elif key == "TYPE":
                    if value.lower() not in ["weapon", "armor", "consumable"]:
                        raise InvalidDataFormatError(f"Invalid item type: {value}")
                    data["type"] = value.lower()
                elif key == "EFFECT":
                    if ":" not in value:
                        raise InvalidDataFormatError(f"Invalid effect format: {value}")
                    stat, amount = value.split(":", 1)
                    data["effect"] = {stat.strip().lower(): int(amount.strip())}
                elif key == "COST":
                    data["cost"] = int(value)
                elif key == "DESCRIPTION":
                    data["description"] = value
                else:
                    raise InvalidDataFormatError(f"Not a real field: {key}")
            fields = ["item_id", "name", "type", "effect", "cost", "description"]
            for field in fields:
                if field not in data:
                    raise InvalidDataFormatError(f"Missing field: {field}")
            
            items[item_id] = data

        except ValueError:
            raise InvalidDataFormatError("Invalid data format")
        except Exception as e:
            raise CorruptedDataError(f"Corrupted Data error: {e}")
    return items
    pass


def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields
    
    Required fields: quest_id, title, description, reward_xp, 
                    reward_gold, required_level, prerequisite
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields
    """
    required_fields = [
        "quest_id", "title", "description",
        "reward_xp", "reward_gold", "required_level", "prerequisite"
    ]
    for field in required_fields:
        if field not in quest_dict:
            raise InvalidDataFormatError(f"Missing field: {field}")

    int_fields = ["reward_xp", "reward_gold", "required_level"]
    for field in int_fields:
        if not isinstance(quest_dict[field], int):
            raise InvalidDataFormatError(f"Field {field} must be an integer")

    if quest_dict["prerequisite"] is not None and not isinstance(quest_dict["prerequisite"], str):
        raise InvalidDataFormatError("Prerequisite must be a string or None")

    return True
    pass

def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields
    
    Required fields: item_id, name, type, effect, cost, description
    Valid types: weapon, armor, consumable
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields or invalid type
    """
    # TODO: Implement validation
    pass

def create_default_data_files():
    """
    Create default data files if they don't exist
    This helps with initial setup and testing
    """
    # TODO: Implement this function
    # Create data/ directory if it doesn't exist
    # Create default quests.txt and items.txt files
    # Handle any file permission errors appropriately
    pass

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary
    
    Args:
        lines: List of strings representing one quest
    
    Returns: Dictionary with quest data
    Raises: InvalidDataFormatError if parsing fails
    """
    # TODO: Implement parsing logic
    # Split each line on ": " to get key-value pairs
    # Convert numeric strings to integers
    # Handle parsing errors gracefully
    pass

def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary
    
    Args:
        lines: List of strings representing one item
    
    Returns: Dictionary with item data
    Raises: InvalidDataFormatError if parsing fails
    """
    # TODO: Implement parsing logic
    pass

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
    # Test creating default files
    # create_default_data_files()
    
    # Test loading quests
    # try:
    #     quests = load_quests()
    #     print(f"Loaded {len(quests)} quests")
    # except MissingDataFileError:
    #     print("Quest file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid quest format: {e}")
    
    # Test loading items
    # try:
    #     items = load_items()
    #     print(f"Loaded {len(items)} items")
    # except MissingDataFileError:
    #     print("Item file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid item format: {e}")

