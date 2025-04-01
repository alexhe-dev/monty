import tkinter as tk
import json_handler as jh
import os
import random


def create_gui():

    def file_path():
        # Returns file path of the current directory appended with
        # quotes.json
        current_directory = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_directory, "..", "quotes.json")

    def get_quote():
        # GUI function to get quote
        # Handling file path to ensure correct file location
        filename = file_path()
        # Load quotes from a JSON file
        quotes = jh.load_quotes(filename)
        keyword = entry_s.get()
        keyword = keyword.lower()
        if keyword in quotes:
            random.shuffle(quotes[keyword])
            label_result.config(state=tk.NORMAL)
            label_result.delete(1.0, tk.END)
            label_result.insert(tk.END, quotes[keyword][0])
            label_result.config(state=tk.DISABLED)
        else:
            label_result.config(state=tk.NORMAL)
            label_result.delete(1.0, tk.END)
            label_result.insert(tk.END, "Sorry, no quotes were found.")
            label_result.config(state=tk.DISABLED)

    def process_quotes(quotes):
        # Strip and split quotes
        quotes_list = [quote.strip() for quote in quotes.split("/")]
        return quotes_list

    def add_quote_gui():
        # GUI function for adding a quote
        keyword = entry_a_k.get()
        if jh.is_valid_keyword(keyword):
            keyword = keyword.lower()
            # get the new quotes
            processed_quotes = process_quotes(entry_a_q.get())
            # Handling file path to ensure correct file location
            current_directory = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(current_directory, "..", "quotes.json")
            # add quotes
            added_quotes = jh.add_quotes(filename, keyword, processed_quotes)
            if added_quotes:
                label_confirm.config(text="Quotes successfully saved")
                update_side()
            else:
                label_confirm.config(
                    text="Duplicate quotes or Error. NO FREE LUNCH."
                )
        else:
            label_confirm.config(text="Not a valid keyword")

    def update_side():
        filename = file_path()
        quotes = jh.load_quotes(filename)

        # Clear frame
        for widget in frame.winfo_children():
            widget.destroy()

        # Add the new content
        top_padding = tk.Label(frame, text="", height=2, bg="white")
        top_padding.pack(fill=tk.X)

        for key, values in quotes.items():
            keyword_label = tk.Label(
                frame, text=f"{key}:", font=("TkDefaultFont", 10)
            )
            keyword_label.pack(anchor="w", padx=10)
            for value in values:
                quote_label = tk.Label(
                    frame, text=f"{value}", font=("TkDefaultFont", 10)
                )
                quote_label.pack(anchor="w", padx=20)
            keyword_padding = tk.Label(frame, text="", height=1, bg="white")
            keyword_padding.pack(fill=tk.X)

        bottom_padding = tk.Label(frame, text="", height=2, bg="white")
        bottom_padding.pack(fill=tk.X)

        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def exit_qui():
        # Create backup and exit
        filename = file_path()
        if jh.backup_json(filename):
            print("\nBackup created.")
        print("Exiting program...\n")
        root.quit()

    # -------- Main Window --------------------
    root = tk.Tk(screenName=None, baseName=None, className="Tk", useTk=1)
    root.config(bg="white")
    root.title("Monty Python Quotes")
    root.geometry("500x600")
    label = tk.Label(
        root, text="Welcome to Monty Python Quotes!",
        font=("TkDefaultFont", 12)
    )
    label.pack(pady=20)

    # Set up close event handling
    root.protocol("WM_DELETE_WINDOW", exit_qui)

    # Prompt to search keyword
    label_prompt = tk.Label(root, text="Enter a keyword:")
    label_prompt.pack(pady=10)

    # Entry field for the keyword
    entry_s = tk.Entry(root)
    entry_s.pack(pady=5)

    # Submit button
    submit_button = tk.Button(root, text="Submit", command=get_quote)
    submit_button.pack(pady=10)

    # Display quote
    label_result = tk.Text(root, wrap=tk.WORD, height=4, width=50)
    label_result.config(state=tk.DISABLED)
    label_result.pack(pady=10)

    # Prompt to add keyword
    label_prompt_add = tk.Label(
        root, text="Enter existing keyword/ a keyword you'd like to add:"
    )
    label_prompt_add.pack(pady=10)

    # Entry for the keyword
    entry_a_k = tk.Entry(root)
    entry_a_k.pack(pady=5)

    # Prompt for corresponding quotes
    label_prompt_add = tk.Label(
        root, text="Enter quotes associated with the keyword,"
        " seperated by /:"
    )
    label_prompt_add.pack(pady=10)

    # Entry for the quotes
    entry_a_q = tk.Entry(root)
    entry_a_q.pack(pady=5)

    # Add button
    add_button = tk.Button(root, text="Add", command=add_quote_gui)
    add_button.pack(pady=10)

    # Confirmation
    label_confirm = tk.Label(root, text="")
    label_confirm.pack(pady=10)

    # Exit
    exit_button = tk.Button(root, text="Exit", command=exit_qui)
    exit_button.pack(pady=10)

    # -------- Side Window --------------------
    # To display all keywords and quotes
    side = tk.Toplevel(root)
    side.config(bg="white")
    side.title("Monty Python Quotes")
    side.geometry("500x600")
    label = tk.Label(
        side, text="All Keywords and Quotes", font=("TkDefaultFont", 12)
    )
    label.pack(pady=20)

    # Exit button for side window
    exit_button_side = tk.Button(side, text="Exit", command=exit_qui)
    exit_button_side.pack(pady=10)

    # Position the side window to the right of the main window
    side.geometry("+{}+{}".format(root.winfo_x() + 500, root.winfo_y()))

    # Fetch content
    filename = file_path()
    quotes = jh.load_quotes(filename)

    # Create a canvas
    canvas = tk.Canvas(side)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=0, pady=0)

    # Create and configure a scrollbar for the canvas
    scrollbar = tk.Scrollbar(side, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.config(yscrollcommand=scrollbar.set)

    # Frame to hold the widgets
    frame = tk.Frame(canvas, bg="white")
    canvas.create_window((0, 0), window=frame, anchor="nw")

    # Label at the top
    label = tk.Label(
        frame, text="All Keywords and Quotes", font=("TkDefaultFont", 12)
    )
    label.pack(pady=20)

    # Keywords and quotes
    for widget in frame.winfo_children():
        widget.destroy()

    top_padding = tk.Label(frame, text="", height=2, bg="white")
    top_padding.pack(fill=tk.X)

    for key, values in quotes.items():
        keyword_label = tk.Label(frame, text=f"{key}:",
                                 font=("TkDefaultFont", 10))
        keyword_label.pack(anchor="w", padx=10)
        for value in values:
            quote_label = tk.Label(
                frame, text=f"{value}", font=("TkDefaultFont", 10)
            )
            quote_label.pack(anchor="w", padx=20)
        keyword_padding = tk.Label(frame, text="", height=1, bg="white")
        keyword_padding.pack(fill=tk.X)

    # Extra padding at the end
    bottom_padding = tk.Label(frame, text="", height=2, bg="white")
    bottom_padding.pack(fill=tk.X)

    # Update the canvas scroll region to match the frame
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    root.mainloop()


def main():
    print("\nRunning in GUI mode...")
    create_gui()


if __name__ == "__main__":
    main()
