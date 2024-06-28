import os
import random

# File path for storing quotes
QUOTES_FILE = "quotes.txt"

# Function to ensure the quotes file exists
def ensure_quotes_file():
    if not os.path.exists(QUOTES_FILE):
        with open(QUOTES_FILE, "w") as file:
            file.write("")

# Function to load quotes from file
def load_quotes():
    ensure_quotes_file()
    with open(QUOTES_FILE, "r") as file:
        quotes = [line.strip() for line in file.readlines() if line.strip()]
    return quotes

# Function to add a new quote to the file
def add_quote(quote):
    ensure_quotes_file()
    with open(QUOTES_FILE, "a") as file:
        file.write(quote + "\n")

# Function to generate and print a random quote
def generate_quote():
    quotes = load_quotes()
    if quotes:
        quote = random.choice(quotes)
        print(quote)
    else:
        print("No quotes found. Please add some quotes.")

# Function to allow user to add a new quote
def create_quote():
    new_quote = input("Enter your new quote: ").strip()
    if new_quote:
        add_quote(new_quote)
        print("Quote added successfully!")
    else:
        print("Empty quote. Please enter a valid quote.")

# Function to display menu and handle user input
def display_menu():
    while True:
        print("\nMenu:")
        print("1. Generate Random Quote")
        print("2. Add New Quote")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == "1":
            generate_quote()
        elif choice == "2":
            create_quote()
        elif choice == "3":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid input. Please enter 1, 2, or 3.")

# Main function to run the script
if __name__ == "__main__":
    print("Welcome to the Enhanced Quote Generator!")
    display_menu()
