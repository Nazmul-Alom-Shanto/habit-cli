from datetime import date, timedelta
from . import db_manager
import calendar
from datetime import datetime, date, timedelta


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





def get_missed_dates(habit: dict, completions: list[date]) -> list[date]:
    """Calculates the list of dates a habit was missed."""
    created_at_str = habit['created_at'].split(" ")[0] # Get 'YYYY-MM-DD' part
    created_date = date.fromisoformat(created_at_str)
    today = date.today()
    
    # Create a set of completion dates for fast lookups
    completion_set = set(completions)
    
    missed_dates = []
    # Iterate through each day from creation until today
    current_day = created_date
    while current_day < today:
        if current_day not in completion_set:
            missed_dates.append(current_day)
        current_day += timedelta(days=1)
        
    return missed_dates

def generate_calendar_view(habit: dict, completions: list[date], year: int, month: int) -> list[list[dict]]:
    """
    Generates a calendar grid for a given month and habit.
    Each day is a dict with its number and status.
    """
    cal = calendar.monthcalendar(year, month)
    today = date.today()
    created_at_str = habit['created_at'].split(" ")[0]
    created_date = date.fromisoformat(created_at_str)
    completion_set = set(completions)
    
    calendar_grid = []
    for week in cal:
        week_data = []
        for day_num in week:
            if day_num == 0:
                # This is a placeholder for a day not in the current month
                week_data.append({'day': None, 'status': 'empty'})
                continue

            current_date = date(year, month, day_num)
            status = ''
            if current_date > today:
                status = 'future'
            elif current_date < created_date:
                status = 'before_creation'
            elif current_date in completion_set:
                status = 'completed'
            else:
                status = 'missed'
            
            week_data.append({'day': day_num, 'status': status})
        calendar_grid.append(week_data)
        
    return calendar_grid


# This will be our NEW master data function, replacing the old one
# This will be our FINAL master data function
def get_summary_data():
    """
    Retrieves and enriches all data needed for the HTML summary,
    including stats, missed dates, and calendar views.
    """
    habits = db_manager.get_habits(status='active')
    summary_data = []
    
    # Generate calendar for the current month
    today = date.today()
    current_year, current_month = today.year, today.month

    for habit in habits:
        habit_dict = dict(habit)
        
        # Fetch completions and convert to date objects
        completions_str = db_manager.get_completions(habit['id'])
        completions_dates = [date.fromisoformat(d) for d in completions_str]
        
        # Add all the stats needed for the template
        habit_dict['current_streak'] = calculate_streak(habit['id'])
        habit_dict['longest_streak'] = calculate_longest_streak(habit['id'])
        habit_dict['completion_rate'] = calculate_completion_rate(habit_dict)
        habit_dict['total_completions'] = len(completions_dates)
        
        # Add missed dates and calendar view
        habit_dict['missed_dates'] = get_missed_dates(habit_dict, completions_dates)
        habit_dict['calendar'] = generate_calendar_view(habit_dict, completions_dates, current_year, current_month)
        
        summary_data.append(habit_dict)
        
    # We pass month/year names to the template for the title
    overall_context = {
        'habits': summary_data,
        'generation_date': today.strftime("%B %d, %Y"),
        'calendar_month': today.strftime("%B"),
        'calendar_year': today.year
    }
    return overall_context

def calculate_longest_streak(habit_id: int) -> int:
    """
    Calculates the longest streak of consecutive completion days for a habit.
    """
    completions_str = db_manager.get_completions(habit_id)
    if not completions_str:
        return 0

    completions = sorted([date.fromisoformat(d) for d in completions_str]) # Sort oldest to newest

    if not completions:
        return 0

    longest_streak = 1
    current_streak = 1
    
    # Iterate from the second completion to the end
    for i in range(1, len(completions)):
        # Check if the current completion is exactly one day after the previous one
        if completions[i] == completions[i-1] + timedelta(days=1):
            current_streak += 1
        else:
            # If the streak is broken, reset the counter
            current_streak = 1
        
        # Update the longest streak found so far
        if current_streak > longest_streak:
            longest_streak = current_streak
            
    return longest_streak

def calculate_completion_rate(habit: dict) -> float:
    """
    Calculates the percentage of days a habit was completed since its creation.
    """
    created_at_str = habit['created_at'].split(" ")[0]
    created_date = date.fromisoformat(created_at_str)
    today = date.today()
    
    # Calculate the number of days the habit has existed
    days_since_creation = (today - created_date).days + 1
    if days_since_creation <= 0:
        return 100.0 # Habit created today is 100% complete if done, 0% otherwise

    total_completions = len(db_manager.get_completions(habit['id']))

    return (total_completions / days_since_creation) * 100.0