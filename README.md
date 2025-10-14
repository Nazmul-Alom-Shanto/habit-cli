# 🌱 Habit Tracker CLI
 🌱 Habit Tracker CLI

[![GitHub release](https://img.shields.io/github/v/release/nazmul-alom-shanto/habit-cli?color=brightgreen&style=for-the-badge)](https://github.com/nazmul-alom-shanto/habit-cli/releases)
[![License](https://img.shields.io/github/license/nazmul-alom-shanto/habit-cli?style=for-the-badge)](./LICENSE)
![Python Version](https://img.shields.io/badge/python-3.10+-blue?style=for-the-badge)
![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-lightgrey?style=for-the-badge)
[![Downloads](https://img.shields.io/github/downloads/nazmul-alom-shanto/habit-cli/total?color=blue&style=for-the-badge)](https://github.com/nazmul-alom-shanto/habit-cli/releases)
[![Built with PyInstaller](https://img.shields.io/badge/built%20with-PyInstaller-orange?style=for-the-badge)](https://pyinstaller.org)

---

A **minimalist, cross-platform Command Line Interface (CLI)** tool built to help you **track and build better habits—directly from your terminal.**

Stop context-switching. Stay productive.  
Powered by **Python**, **Habit Tracker CLI** focuses on **speed, simplicity, and privacy**, giving you instant feedback via beautiful terminal summaries and detailed HTML reports.

---

## ✨ Key Features

- ⚡ **Blazingly Fast** – Track habits with a single, quick command:  
  `habit done <id>`
- 💾 **Local & Private** – All data is stored securely in a local SQLite database — **your data stays yours**.
- 🖥️ **Cross-Platform Binary** – Distributed as standalone executables for **Linux**, **macOS**, and **Windows** — no Python installation required!
- 📊 **Rich Terminal Summaries** – Instantly view streaks, completion rates, and progress right in your console.
- 🖼️ **Visual HTML Reports** – Generate beautiful historical reports with graphs and trends.
- 🗄️ **Full Lifecycle Management** – Add, edit, delete, archive, or unarchive habits anytime.

---

## 🚀 Installation

### 1️⃣ Download Binary

Go to the [**Releases Page**](https://github.com/nazmul-alom-shanto/habit-cli/releases) and download the file for your operating system:

| OS | File Name |
|----|------------|
| Linux | `habit-linux` |
| macOS | `habit-macos` |
| Windows | `habit-windows.exe` |

### 2️⃣ Make It a Global Command

To use `habit` globally from any terminal:

| System | Example Directory |
|---------|------------------|
| **Linux/macOS** | Move to `/usr/local/bin/` or `~/.local/bin/` |
| **Windows** | Move the `.exe` file to a folder (e.g., `C:\Tools\HabitTracker`) and add that folder to your **System PATH** |

Then, open a new terminal and run:

```bash
habit --help
```
🧑‍💻 Installation from Source (Developers)
If you prefer running from source or want to contribute:

```bash
# 1. Clone the repository
git clone https://github.com/nazmul-alom-shanto/habit-cli.git
cd habit-cli

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the module using Python
python -m habit_tracker summary
```
🏗️ Build Binary from Source (Optional)
If you want to rebuild the executable from source using PyInstaller:

```bash
# 1️⃣ Install PyInstaller if not already installed
pip install pyinstaller

# 2️⃣ Build the standalone executable
pyinstaller --name habit --onefile \
    --collect-all habit_tracker \
    --add-data "templates:templates" \
    habit_tracker/__main__.py
```
💡 Tip: On Linux/macOS, you may need to make it executable:

```bash
chmod +x dist/habit
```
📖 Usage Guide
Habit Tracker CLI uses a clean, intuitive command structure:

```bash
habit <action> [options]
```

🔹 Daily Tracking & Reporting
Command	Description	Example
```bash 
habit done <id>	#Mark a habit as completed today.	habit done 3
```
```bash
habit summary	#View a concise summary of all active habits (streaks, % completion).

habit summary-html	#Generate a detailed HTML report and open it in your browser. |	habit summary-html
```
🔹 Habit Management
Command	Description	Example
```bash
habit add "<name>" # Create a new habit. |	habit add "Read 20 pages"
habit edit <id> "<new name>"	# Edit the name of an existing habit. |	habit edit 1 "Read 30 minutes"
habit list	# Show all active habits with IDs |	habit list
habit list --archived	# Show archived habits |	habit list --archived
habit history <id>	# View the completion history of a habit |	habit history 1
```
🔹 Lifecycle Commands
Command	Description	Example
```bash
habit archive <id>  # Archive a habit (keep its history) |	habit archive 2
habit unarchive <id>    # Reactivate an archived habit |	habit unarchive 2
habit delete <id>	# Permanently remove a habit and its data | habit delete 4
```
## 🏗️ Technical Stack

| Component | Library |
|------------|----------|
| CLI Framework | `click` |
| Terminal Output | `rich` |
| Database | `SQLite` |
| HTML Templates | `Jinja2` |
| Packaging | `PyInstaller` |

---

## 📊 Example Output


### ✅ Terminal Summary


| ID | Habit Name | Streak | Progress |
|----|-------------------|---------|----------|
| 1 | Read 20 pages | 🔥 5d | 83% |
| 2 | Morning Exercise | 💪 12d | 100% |


### 🖼️ HTML Report

- Visual graphs of habit consistency  
- Daily/weekly/monthly insights  
- Exportable & shareable format  

---

## 🤝 Contributing

Contributions, bug reports, and feature ideas are warmly welcome 💡

```bash
# Fork the repository
# Create your branch
git checkout -b feature/new-streak-algo

# Commit your changes
git commit -m "feat: Implement improved streak logic"

# Open a Pull Request

```
## 📜 License
This project is licensed under the MIT License — see the LICENSE file for details.

## 🧠 Built for productivity by Nazmul Alom Shanto
"Build habits. Shape your life — one command at a time." 🌿