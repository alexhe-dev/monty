import json
import shutil


def safe_file_operation(func, *args, **kwargs):
    """Safely handles file operation with error catching.

    Args:
        func (callable): The file operation function to be executed
        *args: Positional arguments
        **kwargs: Keyword arguments

    Returns:
        The intended result of file operation function,
        or none if an error occurs.
    """
    try:
        return func(*args, **kwargs)
    except FileNotFoundError:
        print("Error: File not found")
    except PermissionError:
        print("Error: File permission denied")
    except json.JSONDecodeError:
        print("Error: Encoding JSON data")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None


def load_quotes(filename):
    """Loads quotes from a JSON file.

    Args:
        filename (str): Name of the JSON file.

    Returns:
        dict: A dictionary containing quotes that match up to keywords.
        Returns an empty dictionary if the file does not exist or is invalid.
    """
    def read_file():
        with open(filename, "r") as file:
            return json.load(file)
    result = safe_file_operation(read_file)
    return result if result is not None else {}


def is_valid_keyword(keyword):
    """Validates a keyword by making sure it is alphabetical.

    Args:
        keyword (str): Keyword.

    Returns:
        bool: Result.
    """
    return (
        isinstance(keyword, str) and
        keyword.isalpha() and
        keyword.strip() != ""
    )


def save_quotes(filename, quotes):
    """Save the quotes dictionary to a JSON file

    Args:
        filename (str): Name of the JSON file.
        quotes (dict): Dictionary containing quotes.

    Returns:
        bool: Whether quotes were safely saved.
    """
    def write_file():
        with open(filename, "w") as file:
            json.dump(quotes, file, indent=4)
        return True

    # Make sure to catch the case where quotes is empty due to error
    if quotes:
        return safe_file_operation(write_file) is not None
    else:
        print(f"Trying to overwrite contents of {filename} "
              "with an empty dict."
              )
        return False


def add_quotes(filename, keyword, new_quotes):
    """Add quotes with an associated keyword to the JSON file.

    Args:
        filename (str): Name of the JSON file.
        keyword (str): Keyword.
        new_quotes (list): List of the quotes to add.

    Returns:
        list: Quotes that were successsfully added
    """
    added_quotes = []
    # Load existing quotes to a temp dict
    quotes = load_quotes(filename)
    # Add the new quotes
    if keyword not in quotes:
        quotes[keyword] = []
    # Check that the new quotes are not duplicates
    existing_quotes = set(quotes[keyword])
    for quote in new_quotes:
        if quote not in existing_quotes:
            quotes[keyword].append(quote)
            added_quotes.append(quote)
            # Continuously check for duplicates
            existing_quotes.add(quote)
    # Save quotes to the JSON file
    if save_quotes(filename, quotes):
        return added_quotes
    else:
        return []


def backup_json(original_file_path):
    """Creates a backup JSON file for the original file.

    Args:
        original_file_path (str): File path for the original JSON file.

    Returns:
        bool: Whether the backup was safely created.
    """
    # Remove the .json on the original file
    backup_file_path = f"{original_file_path[:-5]}_backup.json"
    # Copy contents to backup
    result = safe_file_operation(
        shutil.copy, original_file_path, backup_file_path
        )
    if result is None:
        print("Error: Backup file was not safely created.")
        return False
    return True
