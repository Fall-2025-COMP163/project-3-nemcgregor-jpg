"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: Noble McGregor

AI Usage: AI helped me debug and how to set up lists and dictionaries that can be changed

This module handles inventory management, item usage, and equipment.
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

# Maximum inventory size
MAX_INVENTORY_SIZE = 20

# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

def add_item_to_inventory(character, item_id):
    """
    Add an item to character's inventory
    
    Args:
        character: Character dictionary
        item_id: Unique item identifier
    
    Returns: True if added successfully
    Raises: InventoryFullError if inventory is at max capacity
    """
    inventory = character.setdefault("inventory", [])

    if len(inventory) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full")

    inventory.append(item_id)
    return True
    pass

def remove_item_from_inventory(character, item_id):
    """
    Remove an item from character's inventory
    
    Args:
        character: Character dictionary
        item_id: Item to remove
    
    Returns: True if removed successfully
    Raises: ItemNotFoundError if item not in inventory
    """
    inventory = character.get("inventory", [])
    if item_id not in inventory:
        raise ItemNotFoundError(f"Item {item_id} not found in inventory")

    inventory.remove(item_id)
    return True

    pass

def has_item(character, item_id):
    """
    Check if character has a specific item
    
    Returns: True if item in inventory, False otherwise
    """
    return item_id in character.get("inventory", [])
    pass

def count_item(character, item_id):
    """
    Count how many of a specific item the character has
    
    Returns: Integer count of item
    """
    return character.get("inventory", []).count(item_id)
    pass

def get_inventory_space_remaining(character):
    """
    Calculate how many more items can fit in inventory
    
    Returns: Integer representing available slots
    """
    inventory = character.get("inventory", [])
    return MAX_INVENTORY_SIZE - len(inventory)
    pass

def clear_inventory(character):
    """
    Remove all items from inventory
    
    Returns: List of removed items
    """
    inventory = character.get("inventory", [])
    removed_items = list(inventory)
    character["inventory"] = []

    return removed_items
    pass

# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    """
    Use a consumable item from inventory
    
    Args:
        character: Character dictionary
        item_id: Item to use
        item_data: Item information dictionary from game_data
    
    Item types and effects:
    - consumable: Apply effect and remove from inventory
    - weapon/armor: Cannot be "used", only equipped
    
    Returns: String describing what happened
    Raises: 
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'consumable'
    """
    inventory = character.get("inventory", [])
    if item_id not in inventory:
        raise ItemNotFoundError(f"Item {item_id} not found in inventory")

    # item_data is already the dict for this item
    item = item_data
    if item.get("type", "").lower() != "consumable":
        raise InvalidItemTypeError(f"Item {item_id} is not consumable")

    effect_str = item.get("effect")
    if not effect_str or ":" not in effect_str:
        raise InvalidItemTypeError(f"Invalid effect format for item {item_id}")

    stat, value_str = effect_str.split(":", 1)
    stat = stat.strip().lower()
    try:
        value = int(value_str.strip())
    except ValueError:
        raise InvalidItemTypeError(f"Invalid numeric value effect for item {item_id}")

    if stat == "health":
        character["health"] = min(
            character.get("health", 0) + value,
            character.get("max_health", character.get("health", 0))
        )
    else:
        character[stat] = character.get(stat, 0) + value

    inventory.remove(item_id)
    return f'{character.get("name","Unknown")} used {item.get("name", item_id)} and gained {value} {stat}.'

    pass

def equip_weapon(character, item_id, item_data):
    """
    Equip a weapon
    
    Args:
        character: Character dictionary
        item_id: Weapon to equip
        item_data: Item information dictionary
    
    Weapon effect format: "strength:5" (adds 5 to strength)
    
    If character already has weapon equipped:
    - Unequip current weapon (remove bonus)
    - Add old weapon back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'weapon'
    """
    inventory = character.get("inventory", [])
    if item_id not in inventory:
        raise ItemNotFoundError(f"Item {item_id} not found in inventory")

    item = item_data
    if item.get("type", "").lower() != "weapon":
        raise InvalidItemTypeError(f"Item {item_id} is not a weapon")

    if character.get("equipped_weapon"):
        old_weapon_id = character["equipped_weapon"]
        old_effect = character.get("equipped_weapon_effect")
        if old_effect:
            stat, value_str = old_effect.split(":", 1)
            stat = stat.strip().lower()
            character[stat] -= int(value_str.strip())
        inventory.append(old_weapon_id)

    effect_str = item.get("effect")
    if not effect_str or ":" not in effect_str:
        raise InvalidItemTypeError(f"Invalid effect format for weapon {item_id}")

    stat, value_str = effect_str.split(":", 1)
    stat = stat.strip().lower()
    try:
        value = int(value_str.strip())
    except ValueError:
        raise InvalidItemTypeError(f"Invalid value effect for weapon {item_id}")

    character[stat] = character.get(stat, 0) + value
    character["equipped_weapon"] = item_id
    character["equipped_weapon_effect"] = effect_str

    inventory.remove(item_id)
    return f'{character.get("name","Unknown")} equipped {item.get("name", item_id)} (+{value} {stat}).'

    pass

def equip_armor(character, item_id, item_data):
    """
    Equip armor
    
    Args:
        character: Character dictionary
        item_id: Armor to equip
        item_data: Item information dictionary
    
    Armor effect format: "max_health:10" (adds 10 to max_health)
    
    If character already has armor equipped:
    - Unequip current armor (remove bonus)
    - Add old armor back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'armor'
    """
    inventory = character.get("inventory", [])

    if item_id not in inventory:
        raise ItemNotFoundError(f"{item_id} not found in inventory")

    if item_id not in item_data:
        raise ItemNotFoundError(f"{item_id} not found in game data")
    item = item_data[item_id]

    if item["type"].lower() != "armor":
        raise InvalidItemTypeError(f"{item_id} is not armor")

    if "equipped_armor" in character and character["equipped_armor"]:
        old_armor_id = character["equipped_armor"]
        old_armor = item_data.get(old_armor_id)

        if old_armor and "effect" in old_armor:
            stat, value = old_armor["effect"].split(":")
            character[stat] -= int(value)

        inventory.append(old_armor_id)

    effect_str = item.get("effect")
    if not effect_str or ":" not in effect_str:
        raise InvalidItemTypeError(f"Invalid item type for armor {item_id}")

    stat, value = effect_str.split(":", 1)
    stat = stat.strip().lower()
    try:
        value = int(value.strip())
    except ValueError:
        raise InvalidItemTypeError(f"Invalid value in effect for armor {item_id}")
    if stat in character:
        character[stat] += value
    else:
        character[stat] = value

    character["equipped_armor"] = item_id

    inventory.remove(item_id)

    return f"{character["name"]} equipped {item["name"]} (+{value} {stat})."

    pass

def unequip_weapon(character):
    """
    Remove equipped weapon and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no weapon equipped
    Raises: InventoryFullError if inventory is full
    """
    inventory = character.get("inventory", [])
    equipped = character.get("equipped_weapon")

    if not equipped:
        return None 
    if len(inventory) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full")

    if "equipped_weapon_effect" in character:
        stat, value = character["equipped_weapon_effect"].split(":")
        character[stat] -= int(value)

    inventory.append(equipped)

    character["equipped_weapon"] = None
    character.pop("equipped_weapon_effect", None)

    return equipped
    pass

def unequip_armor(character):
    """
    Remove equipped armor and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no armor equipped
    Raises: InventoryFullError if inventory is full
    """
    inventory = character.get("inventory", [])
    equipped = character.get("equipped_armor")

    if not equipped:
        return None  

    if len(inventory) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full")

    if "equipped_armor_effect" in character:
        stat, value = character["equipped_armor_effect"].split(":")
        character[stat] -= int(value)

    inventory.append(equipped)

    character["equipped_armor"] = None
    character.pop("equipped_armor_effect", None)

    return equipped
    pass

# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    """
    Purchase an item from a shop
    
    Args:
        character: Character dictionary
        item_id: Item to purchase
        item_data: Item information with 'cost' field
    
    Returns: True if purchased successfully
    Raises:
        InsufficientResourcesError if not enough gold
        InventoryFullError if inventory is full
    """
    if "inventory" not in character:
        character["inventory"] = []
    inventory = character["inventory"]

    cost = item_data.get("cost", 0)

    if character.get("gold", 0) < cost:
        raise InsufficientResourcesError(
            f"Not enough gold to purchase {item_data.get('name', item_id)}"
        )

    if len(inventory) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full")

    character["gold"] -= cost
    inventory.append(item_id)

    return True
    pass

def sell_item(character, item_id, item_data):
    """
    Sell an item for half its purchase cost
    
    Args:
        character: Character dictionary
        item_id: Item to sell
        item_data: Item information with 'cost' field
    
    Returns: Amount of gold received
    Raises: ItemNotFoundError if item not in inventory
    """
    if "inventory" not in character:
        character["inventory"] = []
    inventory = character["inventory"]

    if item_id not in inventory:
        raise ItemNotFoundError(f"Item {item_id} not in inventory")

    inventory.remove(item_id)

    sell_value = item_data.get("cost", 0) // 2
    character["gold"] = character.get("gold", 0) + sell_value
    return sell_value
    pass

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    """
    Parse item effect string into stat name and value
    
    Args:
        effect_string: String in format "stat_name:value"
    
    Returns: Tuple of (stat_name, value)
    Example: "health:20" → ("health", 20)
    """
    stat_name, value_str = effect_string.split(":", 1)
    value = int(value_str.strip())
    return stat_name.strip().lower(), value
    pass

def apply_stat_effect(character, stat_name, value):
    """
    Apply a stat modification to character
    
    Valid stats: health, max_health, strength, magic
    
    Note: health cannot exceed max_health
    """
    if stat_name not in ["health", "max_health", "strength", "magic"]:
        raise ValueError(f"Invalid stat: {stat_name}")

    if stat_name == "health":
        character["health"] = min(
            character.get("health", 0) + value,
            character.get("max_health", character.get("health", 0))
        )
    else:
        character[stat_name] = character.get(stat_name, 0) + value
    pass

def display_inventory(character, item_data_dict):
    """
    Display character's inventory in formatted way
    
    Args:
        character: Character dictionary
        item_data_dict: Dictionary of all item data
    
    Shows item names, types, and quantities
    """
    inventory = character.get("inventory", [])
    if not inventory:
        print(f"{character.get('name', 'Unknown')} has an empty inventory.")
        return

    item_counts = {}
    for item_id in inventory:
        if item_id in item_counts:
            item_counts[item_id] += 1
        else:
            item_counts[item_id] = 1


    print(f"\n{character.get('name', 'Unknown')}s Inventory:")
    print("-" * 40)

    for item_id, count in item_counts.items():
        item_info = item_data_dict.get(item_id, {})
        item_name = item_info.get("name", item_id)
        item_type = item_info.get("type", "Unknown")
        print(f"{item_name} ({item_type}) x{count}")

    print("-" * 40)
    pass

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM TEST ===")
    
    # Test adding items
    test_char = {'inventory': [], 'gold': 100, 'health': 80, 'max_health': 80}
    # 
    try:
       add_item_to_inventory(test_char, "health_potion")
       print(f"Inventory: {test_char['inventory']}")
    except InventoryFullError:
       print("Inventory is full!")
    
    # Test using items
    test_item = {
       'item_id': 'health_potion',
       'type': 'consumable',
       'effect': 'health:20'
    }
    # 
    try:
       result = use_item(test_char, "health_potion", test_item)
       print(result)
    except ItemNotFoundError:
        print("Item not found")

