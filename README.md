Monty: A Monty Python Quote Retrieval Application
Alex He
Inspired by Python's namesake, the legendary comedy troupe Monty Python.

Overview
Monty is a Python application that stores and displays quotes based on keywords, with support for both a command-line interface (CLI) and a graphical user interface (GUI).

Users can input a keyword, and the program will return a relevant Monty Python quote stored in a JSON file.

The CLI supports various modes for adding quotes, viewing available keywords, and displaying all stored quotes.
The GUI, built with Tkinter, also supports similar functionalities.
They are both designed to work seamlessly.

Features
Prevents duplicate quotes – Only unique quotes are stored.
Keyword validation – Rejects invalid keywords.
Automatic backup – Prevents accidental data loss.
Robust error handling - Handles file issues and unexpected inputs.

Dependencies
No additional installations should be necessary, but the program utilizes the following:
- tkinter
- shutil
- random
- os
- sys
- json 
- pytest
- unittest.mock

File Structure
monty/
│── src/
│   ├── cli.py          # CLI entry point
│   ├── gui.py           # GUI entry point
│   ├── json_handler.py  # Handles JSON data storage and modification
│── tests/
│   ├── test_json_handler.py  # Unit tests for JSON handling
│── quotes.json         # Stores Monty Python quotes
│── quotes_backup.json         # Backup to quotes.json
│── README.md  

Have fun quoting Monty Python!
P.S 'castle' is a real hoot.
> "Now go away, or I shall taunt you a second time!"
