import time
import random
import json
import os

##########################
#    david malcolm
#    Bens Text-Based-Adventure-game
#    

# Constants
GAME_DATA_FILE = "game_data.json"

# Adjacency mapping for locations
ADJACENCY_MAP = {
    1: [2],
    2: [1, 3],
    3: [2, 4],
    4: [3, 5],
    5: [4, 6],
    6: [5, 7],
    7: [6, 8],
    8: [7, 9],
    9: [8, 10],
    10: [9, 11],
    11: [10, 12],
    12: [11]
}

def load_game_data():
    #Loads game data from an external JSON file. Creates a new one if not found.
    default_data = {
        "places": [
            "Armory", "Library", "Cell Block", "Kitchen", "Storage Room",
            "Alchemy Lab", "Chapel", "Guard Room", "Torture Chamber", "Dungeon Entrance", "Hidden Passage", "Treasure Vault"
        ],
        "enemies": ["Skeleton", "Zombie", "Ghost", "Dark Knight", "Sorcerer"],
        "items": ["Rusty Sword", "Shield", "Health Potion", "Magic Key", "Torch"]
    }
    try:
        with open(GAME_DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Game data file not found. Creating a new one with default data...")
        save_game_data(default_data)
        return default_data

def save_game_data(data):
    #Saves game data to an external JSON file.
    with open(GAME_DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Classes
class Character:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = 10
        self.inventory = []
        self.defense = 0

    def is_alive(self):
        return self.health > 0

    def take_damage(self, damage):
        self.health = max(self.health - (damage - self.defense), 0)

    def add_item(self, item):
        self.inventory.append(item)

class Game:
    def __init__(self):
        self.data = load_game_data()
        self.player = Character("Hero", 100, 10)
        self.current_location = 1  # Start at the first location
        self.final_door_unlocked = False

    def delayed_print(self, text, delay=0.05):
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

    def choose_location(self):
        self.delayed_print("Where would you like to go?")
        current_place_name = self.data["places"][self.current_location - 1]
        self.delayed_print(f"You are currently in the {current_place_name}.\n\n")

        adjacent_locations = ADJACENCY_MAP[self.current_location]
        for loc in adjacent_locations:
            print(f"{loc}. {self.data['places'][loc - 1]}")

        while True:
            try:
                choice = int(input("Choose an adjacent location by number: "))
                if choice in adjacent_locations:
                    self.current_location = choice
                    self.delayed_print(f"You move to the {self.data['places'][self.current_location - 1]}.")
                    break
                else:
                    print("Invalid choice. Choose an adjacent location.\n")
            except ValueError:
                print("Please enter a valid number.")

    def inspect_location(self):
        current_place_name = self.data["places"][self.current_location - 1]
        self.delayed_print(f"You take a closer look around the {current_place_name}.")
        descriptions = {
            "Armory": "there are rusty weapons and broken shields lining the walls.\n",
            "Library": "You see dusty bookshelves filled with ancient books.\n",
            "Cell Block": "all you see are Dark, damp cells with iron bars.\n",
            "Kitchen": "scattered around are Broken pots and old, rotten food.\n",
            "Storage Room": "all there is are Crates and barrels stacked carelessly.\n",
            "Alchemy Lab": "many Strange bottles and ingredients litter the tables.\n",
            "Chapel": "you see some faded tapestries and a broken altar.\n",
            "Guard Room": "so much Rusted armor and a worn table with playing cards... none of it of use.\n",
            "Torture Chamber": "the floor is caked with Chains and ominous tools\n",
            "Dungeon Entrance": "A heavy door blocks the way out. looks like i need a key...\n",
            "Hidden Passage": "Narrow walls with faint torchlight flickering.\n",
            "Treasure Vault": "Piles of gold and jewels, but danger lurks.\n"
        }
        self.delayed_print(descriptions.get(current_place_name, "There's nothing special here.\n"))
        if self.current_location == 12:
            item = "Magic Key"
            self.player.add_item(item)
            self.delayed_print(f"while inspecting, you find the {item}!\n\n")
            self.final_door_unlocked = True
        elif random.random() < 0.5:
            item = random.choice(self.data["items"])
            self.player.add_item(item)
            self.delayed_print(f"While inspecting, you found a {item}!\n\n")
            if item == "Magic Key":
                self.final_door_unlocked = True
                self.delayed_print("This key looks important. It might unlock the final door.")
            elif item == "Rusty Sword":
                self.player.attack = self.player.attack + 10
            elif item == "Shield":
                self.player.defense = 5
        else:
            self.delayed_print("You didn't find anything useful.")

    def encounter_enemy(self):
        if self.current_location == 12:
            enemy_name = "gilgamesh"
            enemy = Character(enemy_name, 75, 10)

            while enemy.is_alive() and self.player.is_alive():
                self.delayed_print(f"Your health: {self.player.health}, {enemy.name}'s health: {enemy.health}")
                action = input("Do you want to (A)ttack or (R)un? ").lower()

                if action == 'a':
                    enemy.take_damage(self.player.attack)
                    self.delayed_print(f"You hit the {enemy.name} for {self.player.attack} damage!")

                    if enemy.is_alive():
                        self.player.take_damage(enemy.attack)
                        self.delayed_print(f"The {enemy.name} strikes you for {enemy.attack} damage!")
                elif action == 'r':
                    chance = random.random(0,1)
                    if chance < 0.70:
                        print("you failed to escape!")
                        continue
                    else:
                        print("you managed to escape!")
                        break
                else:
                    print("Invalid choice. Try again.")

            if not enemy.is_alive():
                self.delayed_print(f"You defeated the {enemy.name}!")
            elif not self.player.is_alive():
                self.delayed_print("You have been defeated. Game over.")
        elif random.random() < 0.7:  # 70% chance to encounter an enemy
            enemy_name = random.choice(self.data["enemies"])
            enemy = Character(enemy_name, random.randint(20, 50), random.randint(5, 10))
            self.delayed_print(f"A {enemy.name} emerges from the shadows!")

            while enemy.is_alive() and self.player.is_alive():
                self.delayed_print(f"Your health: {self.player.health}, {enemy.name}'s health: {enemy.health}")
                action = input("Do you want to (A)ttack or (R)un? ").lower()

                if action == 'a':
                    enemy.take_damage(self.player.attack)
                    self.delayed_print(f"You hit the {enemy.name} for {self.player.attack} damage!")

                    if enemy.is_alive():
                        self.player.take_damage(enemy.attack)
                        self.delayed_print(f"The {enemy.name} strikes you for {enemy.attack} damage!")
                elif action == 'r':
                    chance = random.random(0,1)
                    if chance < 0.70:
                        print("you failed to escape!")
                        continue
                    else:
                        print("you managed to escape!")
                        break
                else:
                    print("Invalid choice. Try again.")

            if not enemy.is_alive():
                self.delayed_print(f"You defeated the {enemy.name}!")
            elif not self.player.is_alive():
                self.delayed_print("You have been defeated. Game over.")

    def check_final_door(self):
        if self.final_door_unlocked:
            self.delayed_print("You use the Magic Key to unlock the final door. You've escaped the dungeon! Congratulations!")
            return True
        else:
            self.delayed_print("The door is locked. You need a key to open it.")

    def play(self):
        self.delayed_print("You wake up in a dark, damp dungeon. The air is thick, and the walls are cold stone.")
        self.delayed_print("Your goal is to find items and unlock the final door to escape.")

        while self.player.is_alive():
            self.choose_location()
            action = input("Do you want to (I)nspect the room or (M)ove to another location? ").lower()
            if self.current_location == 10: #checks to see if player is in entrance / exit
                if action == 'i':
                    self.check_final_door()
                elif action == 'm':
                    continue
                else:
                    print("Invalid choice. Try again.")
            
            else:
                if action == 'i':
                    self.inspect_location()
                elif action == 'm':
                    continue
                else:
                    print("Invalid choice. Try again.")

            self.encounter_enemy()

            
            

        if not self.player.is_alive():
            self.delayed_print("Your journey ends here. The dungeon claims another victim.")

# Main
if __name__ == "__main__":
    os.system('cls')
    game = Game()
    game.play()


