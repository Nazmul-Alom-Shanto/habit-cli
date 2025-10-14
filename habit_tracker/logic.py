from datetime import date, timedelta
from . import db_manager

def calculate_streak(habit_id: int) -> int:
    """
    Calculates the current streak for a given habit.
    A streak is the number of consecutive days a habit has been completed,
    ending either today or yesterday.
    """
    completions_str = db_manager.get_completions(habit_id)
    if not completions_str:
        return 0

    # Convert string dates from DB to date objects
    completions = [date.fromisoformat(d) for d in completions_str]

    today = date.today()
    yesterday = today - timedelta(days=1)
    
    # If the last completion was not today or yesterday, the streak is broken
    if completions[0] not in [today, yesterday]:
        return 0
    
    streak = 0
    # Start checking from the most recent possible day of the streak
    current_day_in_streak = completions[0]
    
    for completion_date in completions:
        if completion_date == current_day_in_streak:
            streak += 1
            current_day_in_streak -= timedelta(days=1)
        else:
            # A gap in the dates means the streak is over
            break
            
    return streak

def get_enriched_habits_data(status: str = 'active'):
    """
    Retrieves habits and enriches them with streak and completion status for today.
    """
    habits = db_manager.get_habits(status=status)
    enriched_data = []
    
    today_str = date.today().isoformat()

    for habit in habits:
        habit_dict = dict(habit)
        completions = db_manager.get_completions(habit['id'])
        
        habit_dict['streak'] = calculate_streak(habit['id'])
        habit_dict['done_today'] = today_str in completions
        
        enriched_data.append(habit_dict)
        
    return enriched_data
