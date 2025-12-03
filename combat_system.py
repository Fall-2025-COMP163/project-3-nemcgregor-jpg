"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: Noble McGregor

AI Usage: AI helped me debug and use more with functions

Handles combat mechanics
"""

from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)
import random
# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

def create_enemy(enemy_type):
    """
    Create an enemy based on type
    
    Example enemy types and stats:
    - goblin: health=50, strength=8, magic=2, xp_reward=25, gold_reward=10
    - orc: health=80, strength=12, magic=5, xp_reward=50, gold_reward=25
    - dragon: health=200, strength=25, magic=15, xp_reward=200, gold_reward=100
    
    Returns: Enemy dictionary
    Raises: InvalidTargetError if enemy_type not recognized
    """
    enemy_stats = {
        "goblin": {"health": 50, "strength": 8, "magic": 2, "xp_reward": 25, "gold_reward": 10},
        "orc": {"health": 80, "strength": 12, "magic": 5, "xp_reward": 50, "gold_reward": 25},
        "dragon": {"health": 200, "strength": 25, "magic": 15, "xp_reward": 200, "gold_reward": 100}
    }
    enemy_types = enemy_type.lower()

    if enemy_type not in enemy_stats:
        raise InvalidTargetError(f"{enemy_type} is not a valid enemy, check for capitalization")
    stats = enemy_stats[enemy_type]
    enemy = {
        "name": enemy_type.capitalize(),
        "health": stats["health"],
        "max_health": stats["health"],
        "strength": stats["strength"],
        "magic": stats["magic"],
        "xp_reward": stats["xp_reward"],
        "gold_reward": stats["gold_reward"]
    }
    return enemy
    pass

def get_random_enemy_for_level(character_level):
    """
    Get an appropriate enemy for character's level
    
    Level 1-2: Goblins
    Level 3-5: Orcs
    Level 6+: Dragons
    
    Returns: Enemy dictionary
    """
    if character_level <= 2:
        enemy_type = "goblin"
    elif 3 <= character_level <= 5:
        enemy_type = "orc"
    else:
        enemy_type = "dragon"
    
    try:
        return create_enemy(enemy_type)
    except InvalidTargetError as e:
        raise InvalidTargetError(f"No enemy for character level {character_level}: {e}")
    pass

# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    Simple turn-based combat system
    
    Manages combat between character and enemy
    """
    
    def __init__(self, character, enemy):
        """Initialize battle with character and enemy"""
        self.character = character
        self.enemy = enemy
        self.combat_active = True
        self.turn_counter = 1
        pass
    
    def start_battle(self):
        """
        Start the combat loop
        
        Returns: Dictionary with battle results:
                {'winner': 'player'|'enemy', 'xp_gained': int, 'gold_gained': int}
        
        Raises: CharacterDeadError if character is already dead
        """
        if self.character["health"] <= 0:
            raise CharacterDeadError(f"{self.character["name"]} is dead")

        while self.combat_active:
            self.enemy["health"] -= self.character["strength"]
            if self.enemy["health"] <= 0:
                self.combat_active = False
                return {
                    f"{self.character["name"]} has won the battle\n"
                    f"You gained: {self.enemy["xp_reward"]} xp\n"
                    f"You gained: {self.enemy["gold_reward"]} gold"
                }
            
            self.character["health"] -= self.enemy["strength"]
            if self.character["health"] <= 0:
                self.combat_active = False
                return {
                    f"{self.character["name"]} has lost the battle"
                    "You gained: 0 xp"
                    "You gained: 0 gold"
                }
            
            self.turn_counter += 1
        pass
    
    def player_turn(self):
        """
        Handle player's turn
        
        Displays options:
        1. Basic Attack
        2. Special Ability (if available)
        3. Try to Run
        Raises: CombatNotActiveError if called outside of battle
        """
        if not self.combat_active:
            raise CombatNotActiveError("Cannot take action, combat is not active")
        print("Player's Turn")
        print("1. Basic Attack")
        print("2. Special Ability")
        print("3. Try to Run")

        player_choice = input("Choose an action between 1, 2, and 3")
        if player_choice == "1":
            damage = self.character["strength"]
            self.enemy["health"] -= damage
            print(f"{self.character["name"]} dealt {damage} damage to {self.enemy["name"]}")

        elif player_choice == "2":
            if self.character.get("ability_cooldown", False):
                raise AbilityOnCooldownError(f"{self.character["name"]}s ability is on cooldown")
            else:
                damage = self.character["magic"] + self.character["strength"] * 2
                self.enemy["health"] -= damage
                self.character["ability_cooldown"] = True
                print(f"{self.character["name"]} used their special ability and dealt {damage} damage to {self.enemy["name"]}")

        elif player_choice == "3":
            if random.random <= 0.5:
                print(f"{self.character["name"]} succesfully escaped")
                self.combat_active = False
                return {f"Nobody won, xp gained: 0, gold gained: 0"}
            else:
                print(f"{self.character["name"]} failed to escape")
        else:
            print("please select an option between 1, 2, and 3")
        pass
    
    def enemy_turn(self):
        """
        Handle enemy's turn - simple AI
        
        Enemy always attacks
        
        Raises: CombatNotActiveError if called outside of battle
        """
        if not self.combat_active:
            raise CombatNotActiveError("Cannot take action, combat is not active")
        print("Enemy's Turn")
        damage = self.enemy["strength"]
        self.character["health"] -= damage
        print(f"{self.enemy['name']} dealth {damage} to {self.character['name']}")
        if self.character["health"] <= 0:
            self.combat_active = False
            print(f"{self.character['name']} has been defeated!")
            return {
                f"{self.character["name"]} has lost the battle"
                "You gained: 0 xp"
                "You gained: 0 gold"
            }
        self.turn_counter += 1
        pass
    

    def calculate_damage(self, attacker, defender):
        """
        Calculate damage from attack
        
        Damage formula: attacker['strength'] - (defender['strength'] // 4)
        Minimum damage: 1
        
        Returns: Integer damage amount
        """
        damage = attacker["strength"] - (defender["strength"] // 4)
        return max(damage, 1)
        
        pass
    
    def apply_damage(self, target, damage):
        """
        Apply damage to a character or enemy
        
        Reduces health, prevents negative health
        """
        target["health"] -= damage
        if target["health"] < 0:
            target["health"] = 0
        return target["health"]
        
        pass
    
    def check_battle_end(self):
        """
        Check if battle is over
        
        Returns: 'player' if enemy dead, 'enemy' if character dead, None if ongoing
        """
        if self.enemy["health"] <= 0:
            return "player"
        elif self.player['health'] <= 0:
            return "enemy"
        else:
            return None
            
        pass
    
    def attempt_escape(self):
        """
        Try to escape from battle
        
        50% success chance
        
        Returns: True if escaped, False if failed
        """
        escape = random.random() < 0.5

        if escape:
            self.combat_active = False
            return True
        else:
            return False
        pass

# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    """
    Use character's class-specific special ability
    
    Example abilities by class:
    - Warrior: Power Strike (2x strength damage)
    - Mage: Fireball (2x magic damage)
    - Rogue: Critical Strike (3x strength damage, 50% chance)
    - Cleric: Heal (restore 30 health)
    
    Returns: String describing what happened
    Raises: AbilityOnCooldownError if ability was used recently
    """
    if character.get("ability_cooldown", False):
                raise AbilityOnCooldownError("Ability is on cooldown")
    character_class = character.get("class")
    
    result = ""

    if character_class == "Warrior":
        damage = character["strength"] * 2
        enemy["health"] -= damage
        result = f"{character["name"]} used power strike and dealt {damage} damage to {enemy["name"]}"
    
    elif character_class == "Mage":
        damage = character["magic"] * 2
        enemy["health"] -= damage
        result = f"{character["name"]} casts fireball and dealt {damage} damage to {enemy["name"]}"

    elif character_class == "Rogue":
        if random.random() < 0.5:  
            damage = character["strength"] * 3
            enemy["health"] -= damage
            result = f"{character["name"]} used critical strike and dealth {damage} damage to {enemy["name"]}"
        else:
            result = f"{character["name"]} missed their critical strike"

    elif character_class == "Cleric":
        healing = 30
        character["health"] += healing
        result = f"{character["name"]} used heal, {healing} health was restored"

    else:
        result = f"{character["name"]} does not have a special ability"
    character["ability_cooldown"] = True
    return result
   
    pass

def warrior_power_strike(character, enemy):
    """Warrior special ability"""
    damage = character["strength"] * 2
    enemy["health"] -= damage
    result = f"{character["name"]} used power strike and dealt {damage} damage to {enemy["name"]}"
    pass

def mage_fireball(character, enemy):
    """Mage special ability"""
    damage = character["magic"] * 2
    enemy["health"] -= damage
    result = f"{character["name"]} casts fireball and dealt {damage} damage to {enemy["name"]}"
    pass

def rogue_critical_strike(character, enemy):
    """Rogue special ability"""
    if random.random() < 0.5:  
            damage = character["strength"] * 3
            enemy["health"] -= damage
            result = f"{character["name"]} used critical strike and dealth {damage} damage to {enemy["name"]}"
    else:
        result = f"{character["name"]} missed their critical strike"
    pass

def cleric_heal(character):
    """Cleric special ability"""
    healing = 30
    health = min(character["health"] + healing, character["max_health"])
    restored_health = health - character["health"]
    character["health"] = health
    return f"{character["name"]} used heal, {healing} health was restored."
    pass

# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    """
    Check if character is in condition to fight
    
    Returns: True if health > 0 and not in battle
    """
    if character.get("health", 0) <= 0:
        return False
    
    if character.get("combat_active", False):
        return False
    
    return True
    pass

def get_victory_rewards(enemy):
    """
    Calculate rewards for defeating enemy
    
    Returns: Dictionary with 'xp' and 'gold'
    """
    return {
        "xp": enemy.get("xp_reward", 0),
        "gold": enemy.get("gold_reward", 0)
    }

    pass

def display_combat_stats(character, enemy):
    """
    Display current combat status
    
    Shows both character and enemy health/stats
    """
    print("IN COMBAT")
    print(f"{character["name"]} (Character)")
    print(f"HP: {character["health"]}/{character["max_health"]}")
    print(f"Strength: {character.get("strength")}")
    print(f"Magic: {character.get("magic")}")

    print("vs")
    
    print(f"{enemy["name"]} (Enemy)")
    print(f"HP: {enemy["health"]}/{enemy["max_health"]}")
    print(f"Strength: {enemy.get("strength")}")
    print(f"Magic: {enemy.get("magic")}")



    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")
    pass

def display_battle_log(message):
    """
    Display a formatted battle message
    """
    print("BATTLE LOG")
    print(f">>> {message}")
    pass

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    
    # Test enemy creation
    try:
        goblin = create_enemy("goblin")
        print(f"Created {goblin['name']}")
    except InvalidTargetError as e:
        print(f"Invalid enemy: {e}")
    
    # Test battle
    test_char = {
        'name': 'Hero',
        'class': 'Warrior',
        'health': 120,
        'max_health': 120,
        'strength': 15,
        'magic': 5
     }
    
    battle = SimpleBattle(test_char, goblin)
    try:
        result = battle.start_battle()
        print(f"Battle result: {result}")
    except CharacterDeadError:
        print("Character is dead!")

