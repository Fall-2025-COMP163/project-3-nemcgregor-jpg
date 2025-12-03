"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Starter Code

Name: Noble McGregor

AI Usage: AI helped me debug and with how to use empty lists and dictionaries

This module handles quest management, dependencies, and completion.
"""

from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)
import character_manager
# ============================================================================
# QUEST MANAGEMENT
# ============================================================================

def accept_quest(character, quest_id, quest_data_dict):
    """
    Accept a new quest
    
    Args:
        character: Character dictionary
        quest_id: Quest to accept
        quest_data_dict: Dictionary of all quest data
    
    Requirements to accept quest:
    - Character level >= quest required_level
    - Prerequisite quest completed (if any)
    - Quest not already completed
    - Quest not already active
    
    Returns: True if quest accepted
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        InsufficientLevelError if character level too low
        QuestRequirementsNotMetError if prerequisite not completed
        QuestAlreadyCompletedError if quest already done
    """
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest {quest_id} not found")

    quest = quest_data_dict[quest_id]

    if character["level"] < quest["required_level"]:
        raise InsufficientLevelError(
        f'{character.get("name","Unknown")} is level {character["level"]} but needs level {quest["required_level"]}'
    )


    prereq = quest.get("prerequisite")
    if prereq and prereq != "NONE":
        if prereq not in character.get("completed_quests", []):
            raise QuestRequirementsNotMetError(
                f"Prerequisite quest {prereq} not completed"
            )

    if quest_id in character.get("completed_quests", []):
        raise QuestAlreadyCompletedError(f"Quest {quest_id} already completed")

    if quest_id in character.get("active_quests", []):
        raise QuestRequirementsNotMetError(f"Quest {quest_id} is already active")

    character.setdefault("active_quests", []).append(quest_id)

    return True
    
    pass

def complete_quest(character, quest_id, quest_data_dict):
    """
    Complete an active quest and grant rewards
    
    Args:
        character: Character dictionary
        quest_id: Quest to complete
        quest_data_dict: Dictionary of all quest data
    
    Rewards:
    - Experience points (reward_xp)
    - Gold (reward_gold)
    
    Returns: Dictionary with reward information
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        QuestNotActiveError if quest not in active_quests
    """
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest {quest_id} not found")

    quest = quest_data_dict[quest_id]

    if quest_id not in character.get("active_quests", []):
        raise QuestNotActiveError(f"Quest {quest_id} is not active")

    character["active_quests"].remove(quest_id)

    character.setdefault("completed_quests", []).append(quest_id)

    xp_reward = quest["reward_xp"]
    gold_reward = quest["reward_gold"]

    character_manager.gain_experience(character, xp_reward)
    character_manager.add_gold(character, gold_reward)
    pass

def abandon_quest(character, quest_id):
    """
    Remove a quest from active quests without completing it
    
    Returns: True if abandoned
    Raises: QuestNotActiveError if quest not active
    """
    if quest_id not in character.get("active_quests", []):
        raise QuestNotActiveError(f"Quest {quest_id} is not active")
    character["active_quests"].remove(quest_id)
    return True
    pass

def get_active_quests(character, quest_data_dict):
    """
    Get full data for all active quests
    
    Returns: List of quest dictionaries for active quests
    """
    active_quests = []
    for quest_id in character.get("active_quests", []):
        if quest_id not in quest_data_dict:
            raise QuestNotFoundError(f"Quest {quest_id} not found in quest data")
        active_quests.append(quest_data_dict[quest_id])
    return active_quests
    pass

def get_completed_quests(character, quest_data_dict):
    """
    Get full data for all completed quests
    
    Returns: List of quest dictionaries for completed quests
    """
    completed = []
    for quest_id in character.get("completed_quests", []):
        if quest_id not in quest_data_dict:
            raise QuestNotFoundError(f"Quest {quest_id} not found in quest data")
        completed.append(quest_data_dict[quest_id])
    return completed
    pass

def get_available_quests(character, quest_data_dict):
    """
    Get quests that character can currently accept
    
    Available = meets level req + prerequisite done + not completed + not active
    
    Returns: List of quest dictionaries
    """
    available = []
    for quest_id, quest in quest_data_dict.items():
        if quest_id in character.get("completed_quests", []):
            continue
        if quest_id in character.get("active_quests", []):
            continue
        if character["level"] < quest["required_level"]:
            continue
        prereq = quest.get("prerequisite")
        if prereq and prereq != "NONE":
            if prereq not in character.get("completed_quests", []):
                continue

        available.append(quest)

    return available
    pass

# ============================================================================
# QUEST TRACKING
# ============================================================================

def is_quest_completed(character, quest_id):
    """
    Check if a specific quest has been completed
    
    Returns: True if completed, False otherwise
    """
    return quest_id in character.get("completed_quests", [])
    pass

def is_quest_active(character, quest_id):
    """
    Check if a specific quest is currently active
    
    Returns: True if active, False otherwise
    """
    return quest_id in character.get("active_quests", [])
    pass

def can_accept_quest(character, quest_id, quest_data_dict):
    """
    Check if character meets all requirements to accept quest
    
    Returns: True if can accept, False otherwise
    Does NOT raise exceptions - just returns boolean
    """
    if quest_id not in quest_data_dict:
        return False

    quest = quest_data_dict[quest_id]

    if character["level"] < quest["required_level"]:
        return False
    prereq = quest.get("prerequisite")
    if prereq and prereq != "NONE":
        if prereq not in character.get("completed_quests", []):
            return False
    if quest_id in character.get("completed_quests", []):
        return False
    if quest_id in character.get("active_quests", []):
        return False

    return True
    pass

def get_quest_prerequisite_chain(quest_id, quest_data_dict):
    """
    Get the full chain of prerequisites for a quest
    
    Returns: List of quest IDs in order [earliest_prereq, ..., quest_id]
    Example: If Quest C requires Quest B, which requires Quest A:
             Returns ["quest_a", "quest_b", "quest_c"]
    
    Raises: QuestNotFoundError if quest doesn't exist
    """
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest {quest_id} not found")

    chain = []
    current_id = quest_id

    while current_id and current_id != "NONE":
        if current_id not in quest_data_dict:
            raise QuestNotFoundError(f"Quest {current_id} not found in quest data")
        
        chain.insert(0, current_id)  
        prereq = quest_data_dict[current_id].get("prerequisite")
        current_id = prereq if prereq and prereq != "NONE" else None

    return chain
    pass

# ============================================================================
# QUEST STATISTICS
# ============================================================================

def get_quest_completion_percentage(character, quest_data_dict):
    """
    Calculate what percentage of all quests have been completed
    
    Returns: Float between 0 and 100
    """
    total_quests = len(quest_data_dict)
    if total_quests == 0:
        return 0.0

    completed_quests = len(character.get("completed_quests", []))
    percentage = (completed_quests / total_quests) * 100
    return float(percentage)
    pass

def get_total_quest_rewards_earned(character, quest_data_dict):
    """
    Calculate total XP and gold earned from completed quests
    
    Returns: Dictionary with 'total_xp' and 'total_gold'
    """
    total_xp = 0
    total_gold = 0

    for quest_id in character.get("completed_quests", []):
        if quest_id in quest_data_dict:
            quest = quest_data_dict[quest_id]
            total_xp += quest.get("reward_xp", 0)
            total_gold += quest.get("reward_gold", 0)

    return {"total_xp": total_xp, "total_gold": total_gold}
    pass

def get_quests_by_level(quest_data_dict, min_level, max_level):
    """
    Get all quests within a level range
    
    Returns: List of quest dictionaries
    """
    if min_level > max_level:
        min_level, max_level = max_level, min_level

    quests_in_range = []
    for quest_id, quest in quest_data_dict.items():
        required_level = quest.get("required_level")
        if required_level is not None and min_level <= required_level <= max_level:
            quests_in_range.append(quest)

    return quests_in_range
    pass

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_quest_info(quest_data):
    """
    Display formatted quest information
    
    Shows: Title, Description, Rewards, Requirements
    """
    print(f"=== {quest_data['title']} ===")
    print(f"Description: {quest_data['description']}")
    print(f"Rewards: {quest_data['reward_xp']} XP, {quest_data['reward_gold']} Gold")
    print(f"Required Level: {quest_data['required_level']}")
    prereq = quest_data.get("prerequisite")
    if prereq and prereq != "NONE":
        print(f"Prerequisite: {prereq}")
    else:
        print("Prerequisite: None")
    pass

def display_quest_list(quest_list):
    """
    Display a list of quests in summary format
    
    Shows: Title, Required Level, Rewards
    """
    print("QUEST LIST")
    for quest in quest_list:
        print(f"- {quest['title']} (Level {quest['required_level']}) "
              f"=> {quest['reward_xp']} XP, {quest['reward_gold']} Gold")
    pass

def display_character_quest_progress(character, quest_data_dict):
    """
    Display character's quest statistics and progress
    
    Shows:
    - Active quests count
    - Completed quests count
    - Completion percentage
    - Total rewards earned
    """
    active_count = len(character.get("active_quests", []))
    completed_count = len(character.get("completed_quests", []))
    total_percentage = get_quest_completion_percentage(character, quest_data_dict)
    rewards = get_total_quest_rewards_earned(character, quest_data_dict)

    print("QUEST PROGRESS")
    print(f"Active Quests: {active_count}")
    print(f"Completed Quests: {completed_count}")
    print(f"Completion Percentage: {total_percentage:.2f}%")
    print(f"Total Rewards Earned: {rewards['total_xp']} XP, {rewards['total_gold']} Gold")
    pass

# ============================================================================
# VALIDATION
# ============================================================================

def validate_quest_prerequisites(quest_data_dict):
    """
    Validate that all quest prerequisites exist
    
    Checks that every prerequisite (that's not "NONE") refers to a real quest
    
    Returns: True if all valid
    Raises: QuestNotFoundError if invalid prerequisite found
    """
    for quest_id, quest in quest_data_dict.items():
        prereq = quest.get("prerequisite")
        if prereq and prereq != "NONE":
            if prereq not in quest_data_dict:
                raise QuestNotFoundError(
                    f"Quest {quest_id} has invalid prerequisite: {prereq}"
                )
    return True
    pass

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== QUEST HANDLER TEST ===")
    
    # Test data
    test_char = {
         'level': 1,
         'active_quests': [],
         'completed_quests': [],
         'experience': 0,
         'gold': 100
    }
    #
    test_quests = {
         'first_quest': {
             'quest_id': 'first_quest',
             'title': 'First Steps',
             'description': 'Complete your first quest',
             'reward_xp': 50,
             'reward_gold': 25,
             'required_level': 1,
             'prerequisite': 'NONE'
        }
    }
    #
    try:
        accept_quest(test_char, 'first_quest', test_quests)
        print("Quest accepted!")
    except QuestRequirementsNotMetError as e:
        print(f"Cannot accept: {e}")

