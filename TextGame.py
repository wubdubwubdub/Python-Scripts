import random

# Define rooms and their descriptions
rooms = {
    "hall": "You are in a dark hall.",
    "kitchen": "You are in a warm kitchen.",
    "bedroom": "You are in a cozy bedroom.",
    "library": "You are in a dusty old library.",
    "attic": "You are in a cobweb-filled attic.",
    "basement": "You are in a cold, dimly lit basement.",
    "garden": "You are in a serene garden with blooming flowers.",
    "dining_room": "You are in an elegant dining room.",
    "study": "You are in a quiet study with bookshelves lining the walls.",
    "secret_room": "You stumbled upon a hidden room!",
    "laboratory": "You entered a mysterious laboratory."
}

# Define actions and their consequences
actions = {
    "hall": {
        "explore": "You found a secret passage!",
        "run": "You escaped back to the main hall."
    },
    "kitchen": {
        "cook": "You made a delicious meal.",
        "eat": "You feel energized after a good meal.",
        "hide": "You hid behind the counter just in time."
    },
    "bedroom": {
        "sleep": "You dreamt of amazing adventures.",
        "read": "You found an interesting book.",
        "search": "You found a hidden compartment."
    },
    "library": {
        "read": "You found an ancient scroll.",
        "study": "You learned about ancient legends.",
        "hide": "You found a secret passage behind the bookshelf!"
    },
    "attic": {
        "explore": "You found an old chest.",
        "climb": "You found a way out through the attic window.",
        "hide": "You hid among the dusty boxes."
    },
    "basement": {
        "explore": "You found an old map.",
        "investigate": "You discovered an old journal.",
        "hide": "You concealed yourself behind some barrels."
    },
    "garden": {
        "explore": "You found a hidden pathway.",
        "relax": "You feel refreshed after sitting on the bench.",
        "hide": "You disguised yourself among the bushes."
    },
    "dining_room": {
        "eat": "You enjoyed a sumptuous meal.",
        "drink": "You found a hidden stash of fine wine.",
        "hide": "You ducked behind the curtains."
    },
    "study": {
        "read": "You found a rare manuscript.",
        "research": "You discovered clues about the haunted house.",
        "hide": "You concealed yourself in a secret alcove."
    },
    "secret_room": {
        "explore": "You found a treasure chest!",
        "examine": "You found a mysterious artifact.",
        "hide": "You found a hidden exit!"
    },
    "laboratory": {
        "experiment": "You concocted a strange potion.",
        "explore": "You found a hidden passage to the basement.",
        "hide": "You hid among the shelves of bizarre specimens."
    }
}

# Function to simulate the game
def play_game():
    current_room = "hall"
    print("Welcome to the Haunted Mansion Adventure!\n")
    print("You are being chased by a ghost. Survive by making the right choices!\n")

    while True:
        print(rooms[current_room])
        print("Available actions:", list(actions[current_room].keys()))

        action = input("What would you like to do? ").lower().strip()

        if action == "quit":
            print("Exiting the game. Goodbye!")
            break

        if action in actions[current_room]:
            print
