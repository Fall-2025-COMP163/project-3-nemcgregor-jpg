"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: Noble McGregor

AI Usage: [Document any AI assistance used]

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
    required_fields = ["item_id", "name", "type", "effect", "cost", "description"]
    for field in required_fields:
        if field not in item_dict:
            raise InvalidDataFormatError(f"Missing field: {field}")

    valid_items = ["weapon", "armor", "consumable"]
    if item_dict["type"].lower() not in valid_items:
        raise InvalidDataFormatError(f"Invalid item type: {item_dict['type']}")

    if not isinstance(item_dict["cost"], int):
        raise InvalidDataFormatError("Cost has to be an integer")

    if not isinstance(item_dict["effect"], str):
        raise InvalidDataFormatError("Effect must be a string in 'stat:value' format")
    if ":" not in item_dict["effect"]:
        raise InvalidDataFormatError("Effect must be in 'stat:value' format")

    stat, value_str = item_dict["effect"].split(":", 1)
    try:
        int(value_str.strip())
    except ValueError:
        raise InvalidDataFormatError("Effect value must be an integer")

    return True

    pass

def create_default_data_files():
    """
    Create default data files if they don't exist
    This helps with initial setup and testing
    """
    try:
        if not os.path.exists("data"):
            os.makedirs("data")
            quests_file = "data/quests.txt"
            if not os.path.exists(quests_file):
                with open(quests_file, "w", encoding="utf-8") as f:
                    f.write(
                        "QUEST_ID: goblin_hunt"
                        "TITLE: Hunt the Goblins"
                        "DESCRIPTION: Defeat 5 goblins near the village"
                        "REWARD_XP: 100"
                        "REWARD_GOLD: 50"
                        "REQUIRED_LEVEL: 1"
                        "PREREQUISITE: NONE"
                        "QUEST_ID: dragon_slayer"
                        "TITLE: Slay the Dragon"
                        "DESCRIPTION: Defeat the mighty dragon"
                        "REWARD_XP: 500"
                        "REWARD_GOLD: 200"
                        "REQUIRED_LEVEL: 5"
                        "PREREQUISITE: goblin_hunt"
                    )

        items_file = "data/items.txt"
        if not os.path.exists(items_file):
            with open(items_file, "w", encoding="utf-8") as f:
                f.write(
                    "ITEM_ID: sword_iron"
                    "NAME: Iron Sword"
                    "TYPE: weapon"
                    "EFFECT: strength:5"
                    "COST: 100"
                    "DESCRIPTION: An iron sword."
                    "ITEM_ID: potion_small"
                    "NAME: Small Health Potion"
                    "TYPE: consumable"
                    "EFFECT: health:20"
                    "COST: 50"
                    "DESCRIPTION: Restores a small amount of health."
                )

    except (PermissionError, OSError) as e:
        raise CorruptedDataError(f"Error creating default data file: {e}")

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
    quest = {}
    try:
        for line in lines:
            if ":" not in line:
                raise InvalidDataFormatError(f"Invalid line format: {line}")
            key, value = line.split(":", 1)
            key = key.strip().upper()
            value = value.strip()

            if key == "QUEST_ID":
                quest["quest_id"] = value
            elif key == "TITLE":
                quest["title"] = value
            elif key == "DESCRIPTION":
                quest["description"] = value
            elif key == "REWARD_XP":
                quest["reward_xp"] = int(value)
            elif key == "REWARD_GOLD":
                quest["reward_gold"] = int(value)
            elif key == "REQUIRED_LEVEL":
                quest["required_level"] = int(value)
            elif key == "PREREQUISITE":
                quest["prerequisite"] = None if value.upper() == "NONE" else value
            else:
                raise InvalidDataFormatError(f"Unexpected field: {key}")

        fields = ["quest_id", "title", "description", "reward_xp",
                    "reward_gold", "required_level", "prerequisite"]
        for field in fields:
            if field not in quest:
                raise InvalidDataFormatError(f"Missing field: {field}")

        return quest

    except ValueError:
        raise InvalidDataFormatError("Can not parse field")
    except Exception as e:
        raise InvalidDataFormatError(f"Error parsing quest block: {e}")
    pass

def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary
    
    Args:
        lines: List of strings representing one item
    
    Returns: Dictionary with item data
    Raises: InvalidDataFormatError if parsing fails
    """
    item = {}
    try:
        for line in lines:
            if ":" not in line:
                raise InvalidDataFormatError(f"Invalid line format: {line}")
            key, value = line.split(":", 1)
            key = key.strip().upper()
            value = value.strip()

            if key == "ITEM_ID":
                item["item_id"] = value
            elif key == "NAME":
                item["name"] = value
            elif key == "TYPE":
                if value.lower() not in ["weapon", "armor", "consumable"]:
                    raise InvalidDataFormatError(f"Invalid item type: {value}")
                item["type"] = value.lower()
            elif key == "EFFECT":
                if ":" not in value:
                    raise InvalidDataFormatError(f"Invalid effect format: {value}")
                stat, amount = value.split(":", 1)
                item["effect"] = {stat.strip().lower(): int(amount.strip())}
            elif key == "COST":
                item["cost"] = int(value)
            elif key == "DESCRIPTION":
                item["description"] = value
            else:
                raise InvalidDataFormatError(f"Unexpected field: {key}")

        fields = ["item_id", "name", "type", "effect", "cost", "description"]
        for field in fields:
            if field not in item:
                raise InvalidDataFormatError(f"Missing field: {field}")

        return item

    except ValueError:
        raise InvalidDataFormatError("Can not parse field")
    except Exception as e:
        raise InvalidDataFormatError(f"Error parsing item block: {e}")
    pass

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
    # Test creating default files
    create_default_data_files()
    
    # Test loading quests
    try:
        quests = load_quests()
        print(f"Loaded {len(quests)} quests")
    except MissingDataFileError:
        print("Quest file not found")
    except InvalidDataFormatError as e:
        print(f"Invalid quest format: {e}")
    
    # Test loading items
    try:
        items = load_items()
        print(f"Loaded {len(items)} items")
    except MissingDataFileError:
        print("Item file not found")
    except InvalidDataFormatError as e:
        print(f"Invalid item format: {e}")

