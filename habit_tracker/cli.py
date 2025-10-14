import click
from datetime import date
from rich.console import Console
from rich.table import Table
from pathlib import Path
from . import db_manager, logic
from jinja2 import Environment, FileSystemLoader
import webbrowser

console = Console()

def _get_active_habits_with_display_ids():
    """Helper to get active habits and a map from display ID to db ID."""
    active_habits = logic.get_enriched_habits_data(status='active')
    id_map = {i + 1: habit['id'] for i, habit in enumerate(active_habits)}
    return active_habits, id_map

def _get_archived_habits_with_display_ids():
    """Helper to get archived habits and a map from display ID to db ID."""
    archived_habits = logic.get_enriched_habits_data(status='archived')
    id_map = {i + 1: habit['id'] for i, habit in enumerate(archived_habits)}
    return archived_habits, id_map

@click.group()
def cli():
    """A CLI tool to track your daily habits."""
    pass

@cli.command(name="list")
@click.option('--archived', is_flag=True, help="List archived habits instead of active ones.")
def list_habits(archived):
    """Lists all active or archived habits."""
    status = 'archived' if archived else 'active'
    habits_data, _ = logic.get_enriched_habits_data(status=status), None
    
    if not habits_data:
        console.print(f"No {status} habits found. Use 'habit add' to create one!", style="yellow")
        return

    table = Table(title=f"{status.capitalize()} Habits", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=4)
    table.add_column("Habit Name", min_width=20)
    table.add_column("Streak", justify="right")
    table.add_column("Completed Today?", justify="center")

    for idx, habit in enumerate(habits_data):
        status_emoji = "✅" if habit['done_today'] else "❌"
        streak_color = "green" if habit['streak'] > 0 else "default"
        table.add_row(
            str(idx + 1),
            habit['name'],
            f"[{streak_color}]{habit['streak']}[/{streak_color}]",
            status_emoji
        )
    console.print(table)


@cli.command()
@click.argument('name')
@click.option('-d', '--description', default="", help="A short description of the habit.")
def add(name, description):
    """Adds a new habit."""
    db_manager.add_habit(name, description)
    console.print(f"Habit '[bold cyan]{name}[/bold cyan]' added successfully!", style="green")
    list_habits.callback(archived=False)


@cli.command()
@click.argument('display_id', type=int)
def done(display_id):
    """Marks a habit as done for today."""
    _, id_map = _get_active_habits_with_display_ids()
    if display_id not in id_map:
        console.print("Error: Invalid ID.", style="bold red")
        return
    
    db_id = id_map[display_id]
    db_manager.add_completion(db_id, date.today())
    console.print("Great job! Habit marked as done for today.", style="green")
    list_habits.callback(archived=False)


@cli.command()
@click.argument('display_id', type=int)
def archive(display_id):
    """Archives an active habit."""
    _, id_map = _get_active_habits_with_display_ids()
    if display_id not in id_map:
        console.print("Error: Invalid ID.", style="bold red")
        return
    
    db_id = id_map[display_id]
    db_manager.update_habit_status(db_id, 'archived')
    console.print("Habit archived.", style="yellow")
    list_habits.callback(archived=False)


@cli.command()
@click.argument('display_id', type=int)
def unarchive(display_id):
    """Restores an archived habit to active."""
    _, id_map = _get_archived_habits_with_display_ids()
    if display_id not in id_map:
        console.print("Error: Invalid ID.", style="bold red")
        return
    
    db_id = id_map[display_id]
    db_manager.update_habit_status(db_id, 'active')
    console.print("Habit restored to active.", style="green")
    list_habits.callback(archived=True)


@cli.command()
@click.argument('display_id', type=int)
def delete(display_id):
    """Deletes a habit permanently."""
    active_habits, active_id_map = _get_active_habits_with_display_ids()
    archived_habits, archived_id_map = _get_archived_habits_with_display_ids()
    
    db_id = None
    habit_name = ""
    if display_id in active_id_map:
        db_id = active_id_map[display_id]
        habit_name = active_habits[display_id - 1]['name']
    elif display_id in archived_id_map:
        db_id = archived_id_map[display_id]
        habit_name = archived_habits[display_id - 1]['name']

    if not db_id:
        console.print("Error: Invalid ID. Check `list` or `list --archived`.", style="bold red")
        return
    
    if click.confirm(f"Are you sure you want to permanently delete '[bold red]{habit_name}[/bold red]'?"):
        db_manager.delete_habit(db_id)
        console.print(f"Habit '[bold red]{habit_name}[/bold red]' deleted.", style="yellow")


@cli.command()
@click.argument('display_id', type=int)
def history(display_id):
    """Shows the completion history for a habit."""
    active_habits, active_id_map = _get_active_habits_with_display_ids()
    db_id = active_id_map.get(display_id)

    if not db_id:
        console.print("Error: Invalid ID.", style="bold red")
        return

    habit_name = active_habits[display_id - 1]['name']
    completions = db_manager.get_completions(db_id)
    
    if not completions:
        console.print(f"No history found for '[bold cyan]{habit_name}[/bold cyan]'.", style="yellow")
        return
        
    table = Table(title=f"Completion History for '{habit_name}'")
    table.add_column("Date", style="cyan")
    
    for comp_date in completions:
        table.add_row(comp_date)
        
    console.print(table)



@cli.command(name="summary-html")
def summary_html():
    """Generates an HTML summary report of your habits."""
    console.print("Generating HTML summary...", style="cyan")

    # 1. Prepare data using the NEW master function
    context = logic.get_summary_data() # This now returns the full context dictionary
    
    # 2. Set up Jinja2 (no changes here)
    template_dir = Path(__file__).resolve().parent.parent / "templates"
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("summary.html")
    
    # 3. Render the template by unpacking the context dictionary
    html_output = template.render(**context)
    
    # 4 & 5. Save and open the file (no changes here)
    output_path = Path.cwd() / "habit_summary.html"
    with open(output_path, "w") as f:
        f.write(html_output)
        
    console.print(f"✅ Summary saved to: [bold green]{output_path}[/bold green]")
    
    if click.confirm("Do you want to open the report now?"):
        webbrowser.open(output_path.as_uri())



@cli.command(name="summary")
def summary_terminal():
    """Prints a summarized report of your habits directly to the terminal."""
    console.print("Fetching habit summary...", style="cyan")

    # 1. Prepare data using the master function
    context = logic.get_summary_data()

    # The 'context' dictionary should contain a key for your habit data, 
    # for example, 'habits' which is a list of habit objects/dictionaries.
    habits_data = context.get('habits', []) 

    if not habits_data:
        console.print("[bold yellow]No active habits found to summarize.[/bold yellow]")
        return

    # 2. Create the Rich Table
    table = Table(
        title="Habit Tracker Summary", 
        show_header=True, 
        header_style="bold magenta", 
        show_lines=True
    )
    
    # Define columns based on the data you want to display
    table.add_column("Habit Name", style="bold green", min_width=20)
    table.add_column("Period", justify="center")
    table.add_column("Current Streak", justify="right", style="cyan")
    table.add_column("Longest Streak", justify="right", style="blue")
    table.add_column("Completion %", justify="right", style="yellow")

    # 3. Populate the Table with data
    for habit in habits_data:
        # Assuming your habit data structure looks something like this:
        name = habit.get("name", "N/A")
        period = habit.get("period", "N/A").title() # e.g., 'daily' -> 'Daily'
        current_streak = str(habit.get("current_streak", 0))
        longest_streak = str(habit.get("longest_streak", 0))
        # Calculate a simple completion percentage for display
        total_checks = habit.get("total_checks", 0)
        total_possible = habit.get("total_possible", 1) # Avoid ZeroDivisionError
        completion_percent = f"{(total_checks / total_possible) * 100:.1f}%"
        
        table.add_row(
            name,
            period,
            current_streak,
            longest_streak,
            completion_percent
        )

    # 4. Print the table to the console
    console.print(table)
    console.print("\n[bold green]Summary complete.[/bold green]")