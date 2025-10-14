#!/usr/bin/env bash

# Ensure script is run from project root
PROJECT_DIR="./"

# Create main CLI file
touch "$PROJECT_DIR/habit_tracker.py"

# Create db folder and placeholder DB file
mkdir -p "$PROJECT_DIR/db"
touch "$PROJECT_DIR/db/habits.db"

# Create templates folder and HTML summary template
mkdir -p "$PROJECT_DIR/templates"
cat > "$PROJECT_DIR/templates/summary.html" <<EOL
<!DOCTYPE html>
<html>
<head>
    <title>Habit Summary</title>
</head>
<body>
    <h1>Habit Tracker Summary</h1>
    <!-- Placeholder for Jinja2-rendered content -->
</body>
</html>
EOL

# Create README.md if it doesn't exist
if [ ! -f "$PROJECT_DIR/README.md" ]; then
cat > "$PROJECT_DIR/README.md" <<EOL
# Habit Tracker CLI

A cross-platform CLI tool to track daily habits, maintain history, and generate summary reports.
EOL
fi

# Create LICENSE file if it doesn't exist
if [ ! -f "$PROJECT_DIR/LICENSE" ]; then
cat > "$PROJECT_DIR/LICENSE" <<EOL
MIT License
EOL
fi

echo "Remaining project structure created."
tree "$PROJECT_DIR"
