# Habit Tracker CLI Project Plan

## Overview
This project is a **cross-platform CLI habit tracker** built in Python. Users can add, edit, delete, archive, and mark habits as done each day. It maintains a **local database** to track history and streaks, and optionally generates an HTML summary of progress.

The goal is to create a **binary executable** for Linux, Windows, and macOS, so users do not need Python installed.

---

## Features

### Core CLI Features
- `habit add "Habit Name"` - Add a new habit.
- `habit edit <id> "New Habit Name"` - Edit an existing habit.
- `habit delete <id>` - Delete a habit.
- `habit archive <id>` - Archive a habit.
- `habit done <id>` - Mark habit as done today.
- `habit history <id>` - Show daily history for a habit.
- `habit summary` - Show CLI summary: streaks, completion rates.
- `habit summary-html` - Generate a local HTML summary using templates.

### Optional Features
- Reminders or notifications for daily habits.
- Graphs or charts in HTML summary (using matplotlib or plotly).
- Export/import habits in JSON or CSV.
- Backup database to cloud (GitHub Gist / Google Drive).

---

## Tech Stack

| Layer | Tool / Library |
|-------|----------------|
| CLI | Click or argparse |
| Terminal UI | Rich (tables, progress bars, streaks) |
| Local DB | SQLite (built-in Python) |
| HTML Summary | Jinja2 (templates) |
| Binary Packaging | PyInstaller (`--onefile`) |

Optional:
- Pandas for statistics calculations
- Matplotlib / Plotly for charts in HTML summary

---

## Project Structure

```
habit-tracker/
├─ habit_tracker.py       # main CLI entrypoint
├─ db/
│   └─ habits.db          # SQLite database (created automatically)
├─ templates/
│   └─ summary.html       # Jinja2 template for HTML report
├─ README.md
├─ requirements.txt      # Python dependencies
├─ LICENSE
└─ plan.md               # project plan (this file)
```

---

## Development Plan

### Phase 1: CLI MVP
1. Set up Python project and virtual environment.
2. Implement core CLI commands (`add`, `edit`, `delete`, `done`, `history`, `summary`).
3. Connect SQLite database and implement habit history tracking.
4. Use `Rich` for terminal output (tables, colors, streaks).

### Phase 2: Binary Packaging
1. Test PyInstaller build on Linux.
2. Build Windows `.exe` and macOS binary.
3. Ensure cross-platform consistency.

### Phase 3: HTML Summary
1. Create `summary.html` template with placeholders.
2. Implement Jinja2 rendering using habit history.
3. Optionally add graphs or charts.

### Phase 4: Optional Enhancements
- Daily notifications/reminders.
- Export/import habits.
- Backup and sync.
- Streak achievements, gamification.

---

## Notes
- Keep CLI commands intuitive and short.
- Use modular Python structure for maintainability.
- Ensure database schema can easily track habit history and archived habits.
- Make HTML summary visually clear and optional.

---

## Requirements File (`requirements.txt`)
```
click
rich
jinja2
sqlite3
# optional for graphs or stats:
matplotlib
pandas
```

