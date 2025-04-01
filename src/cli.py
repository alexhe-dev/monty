import random
from json_handler import load_quotes, add_quotes, is_valid_keyword, backup_json
import os


quit_program = False


def exit_program(original_file_path):
    # Create backup and exit
    print()
    backup_json(original_file_path)
    print("Backup created.")
    print("Exiting program...")
    print()


def get_input(line, triggers):
    # Checks if the input matches any triggers
    global quit_program
    user_input = input(line).strip()
    for trigger in triggers:
        if user_input.lower() == trigger.lower():
            quit_program = True
    return user_input


def get_quote(keyword, quotes):
    # Function used to print out a random quote associated with keyword
    keyword = keyword.lower()
    if not is_valid_keyword(keyword):
        print("Sorry, invalid keyword.")
    elif keyword in quotes:
        random.shuffle(quotes[keyword])
        print(quotes[keyword][0])
    else:
        print("Sorry, no quotes were found for that keyword.")


def add_mode(filename):
    # Mode where the user can continously add keyword + quote pairs
    global quit_program
    while True:
        keyword_to_add = get_input(
            "Enter existing keyword/ a keyword you would like to add: ",
            ["quit", "exit"]
            ).lower()
        if quit_program:
            quit_program = False
            break
        if is_valid_keyword(keyword_to_add):
            quotes_to_add = get_input(
                "Enter the quotes you would like to add "
                "(use / to seperate multiple quotes): \n", ["quit", "exit"]
                )
            if quit_program:
                quit_program = False
                break
            quotes_list = [
                quote.strip() for quote in quotes_to_add.split("/")
                ]
            added_quotes = add_quotes(
                filename, keyword_to_add, quotes_list
                )
            if added_quotes:
                print(
                    "Quotes successfully added "
                    f"to the '{keyword_to_add}' keyword."
                )
            else:
                print(
                    "Quotes were not added "
                    f"to the '{keyword_to_add}' keyword."
                    )


def run_cli():
    print("\nRunning in CLI mode...")
    # Handling file path to ensure correct file location
    current_directory = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(current_directory, "..", "quotes.json")
    # Load quotes from a JSON file
    quotes = load_quotes(filename)
    # Main
    print("\nIf you would like to add a quote, please input 'add'.")
    print("If you would like to use add mode, enter 'add_mode'.")
    print("If you would like to view the list of keywords, "
          "enter 'view_keywords'.")
    print("If you would like to view the entire dictionary, "
          "enter 'view_all'.")
    print(
        "If you would like to exit the program at any time, "
        "please input 'quit'.\n"
        )
    while not quit_program:
        user_input = get_input("Enter a keyword: ", ["quit", "exit"])
        if quit_program:
            exit_program(filename)
            break
        if user_input.lower() == "add":
            keyword_to_add = get_input(
                "Enter existing keyword/ "
                "a keyword you would like to add: ", ["quit", "exit"]
                ).lower()
            if quit_program:
                exit_program(filename)
                break
            if is_valid_keyword(keyword_to_add):
                quotes_to_add = get_input(
                    "Enter the quotes you would like to add"
                    "(use / to seperate multiple quotes): \n", ["quit", "exit"]
                    )
                if quit_program:
                    exit_program(filename)
                    break
                quotes_list = [
                    quote.strip() for quote in quotes_to_add.split("/")
                    ]
                added_quotes = add_quotes(
                    filename, keyword_to_add, quotes_list
                    )
                if added_quotes:
                    print(
                        "Quotes successfully added "
                        f"to the '{keyword_to_add}' keyword."
                    )
                else:
                    print(
                        "No quotes were added. Duplicate quotes or Error."
                        )
                    print("NO FREE LUNCH\n")
                quotes = load_quotes(filename)
            else:
                print(f"The keyword '{keyword_to_add}' is invalid.")
        elif user_input.lower() == "add_mode":
            print("\nYou are now entering add_mode.\n"
                  "Enter 'quit' to exit add_mode.")
            add_mode(filename)
            quotes = load_quotes(filename)
            print("You are now exiting add_mode.\n")
        elif user_input.lower() == "view_keywords":
            print()
            for key in quotes:
                print(key)
            print()
        elif user_input.lower() == "view_all":
            print()
            for key, values in quotes.items():
                print(f"{key}:")
                for value in values:
                    print(f"- {value}")
                print()
            print()
        else:
            get_quote(user_input, quotes)


def main():
    run_cli()


if __name__ == "__main__":
    main()
