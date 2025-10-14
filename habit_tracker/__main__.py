from . import db_manager
from .cli import cli

def main():
    """The main function to run the application."""
    # Ensure the database and tables are created before running any command
    db_manager.init_db()
    # Start the Click command-line interface
    cli()

if __name__ == '__main__':
    main()
