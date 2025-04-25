door_a = {"name": "door a", "type": "door"}
door_b = {"name": "door b", "type": "door"}
door_c = {"name": "door c", "type": "door"}
door_d = {"name": "door d", "type": "door"}

key_a = {"name": "key for door a", "type": "key", "target": door_a}
key_b = {"name": "key for door b", "type": "key", "target": door_b}
key_c = {"name": "key for door c", "type": "key", "target": door_c}
key_d = {"name": "key for door d", "type": "key", "target": door_d}

couch = {"name": "couch", "type": "furniture"}
piano = {"name": "piano", "type": "furniture"}
queen_bed = {"name": "queen bed", "type": "furniture"}
double_bed = {"name": "double bed", "type": "furniture"}
dresser = {"name": "dresser", "type": "furniture"}
dining_table = {"name": "dining table", "type": "furniture"}

bread_and_wine = {"name": "bread and wine", "type": "item"}
radiation_gloves = {"name": "radiation gloves", "type": "item"}
royal_crown = {"name": "royal crown", "type": "item"}
banana = {"name": "banana", "type": "item"}

game_room = {"name": "game room", "type": "room"}
bedroom_1 = {"name": "bedroom 1", "type": "room"}
bedroom_2 = {"name": "bedroom 2", "type": "room"}
living_room = {"name": "living room", "type": "room"}
outside = {"name": "outside"}


all_rooms = [game_room, outside, living_room, bedroom_1, bedroom_2]

all_doors = [door_a, door_b, door_c, door_d]

all_furniture = [couch, piano, queen_bed, double_bed, dresser, dining_table]

object_relations = {
    "game room": [couch, piano, door_a],
    "bedroom 1": [queen_bed, door_a, door_b, door_c],
    "bedroom 2": [dresser, double_bed, door_b],
    "living room": [dining_table, door_d, door_c],
    "outside": [door_d],
    "couch": [radiation_gloves],
    "dining table": [bread_and_wine],


    "piano": [key_a],
    "queen bed": [key_b, royal_crown],
    "dresser": [key_d],
    "double bed": [key_c],

    "door a": [game_room, bedroom_1],
    "door b": [bedroom_1, bedroom_2],
    "door c": [bedroom_1, living_room],
    "door d": [outside, living_room]
}

INIT_GAME_STATE = {
    "current_room": game_room,
    "keys_collected": [],
    "items_collected": [banana],
    "target_room": outside
}

import random
import sys


player_moves = 0

def linebreak():
    """
    Print a line break
    """
    print("\n\n")

def start_game():
    """
    Start the game
    """
    global player_moves
    player_moves = 0
    print("You wake up on a couch and find yourself in a strange house"
          "with no windows which you have never been to before.\n"
          "You feel some unknown danger is approaching\n"
          "and you must get out of the house, NOW!")
    play_room(game_state["current_room"])

def play_room(room):
    global player_moves
    """
    Play a room. First check if the room being played is the target room.
    If it is, the game will end with success. Otherwise, let player either
    explore (list all items in this room) or examine an item found here.
    """
    if player_moves >= 20:
        print("💀 Game Over: You've used too many moves. You died from radiation.")
        sys.exit()

    game_state["current_room"] = room
    if(game_state["current_room"] == game_state["target_room"]):
        print("Congrats! You escaped the room!")
        result(player_moves)
        sys.exit()
    else:
        print("You are now in " + room["name"])
        intended_action = input(
            "What would you like to do? Type 'explore', "
            "'examine' or 'inventory'? "
        ).strip()
        if intended_action == "explore":
            explore_room(room)
            player_moves += 1
            play_room(room)
        elif intended_action == "examine":
            examine_item(input("What would you like to examine?").strip())
            player_moves += 1
        elif intended_action == "inventory":
            show_inventory()
            play_room(room)
        else:
            print("Not sure what you mean. Type 'explore' or 'examine'.")
            play_room(room)
        linebreak()

def explore_room(room):
    items = [i["name"] for i in object_relations[room["name"]]]
    print(
         "You explore the room."
         "This is " + room["name"] + ". You find " + ", ".join(items))

def get_next_room_of_door(door, current_room):
    connected_rooms = object_relations[door["name"]]
    for room in connected_rooms:
        if(not current_room == room):
            return room

def examine_item(item_name):
    """
    Examine an item which can be a door or furniture.
    First make sure the intended item belongs to the current room.
    Then check if the item is a door. Tell player if key hasn't been
    collected yet. Otherwise ask player if they want to go to the next
    room. If the item is not a door, then check if it contains keys.
    Collect the key if found and update the game state. At the end,
    play either the current or the next room depending on the game state
    to keep playing.
    """

    current_room = game_state["current_room"]
    next_room = ""
    output = None

    for item in object_relations[current_room["name"]]:
        if(item["name"] == item_name):
            output = "You examine " + item_name + ". "
            if(item["type"] == "door"):
                have_key = False
                for key in game_state["keys_collected"]:
                    if(key["target"] == item):
                        have_key = True
                if(have_key):
                    output += "You unlock it with a key you have."
                    next_room = get_next_room_of_door(item, current_room)
                else:
                    output += "It is locked but you don't have the key."
            else:
                if item["name"] in object_relations and \
                   len(object_relations[item["name"]]) > 0:
                    item_found = object_relations[item["name"]].pop()
                    if item_found["type"] == "key":
                        game_state["keys_collected"].append(item_found)
                        output += "You found a key: " + item_found["name"] + "."
                    else:
                        game_state["items_collected"].append(item_found)
                        output += "You found an item: " + item_found["name"] + "."
                else:
                    output += "There isn't anything interesting about it."

            print(output)
            break

    if(output is None):
        print("The item you requested is not found in the current room.")

    if(next_room and input(
        "Do you want to go to the next room?"
        "Enter 'yes' or 'no'").strip() == 'yes'):
        fun_fact()
        play_room(next_room)

    else:
        play_room(current_room)

def fun_fact():
    facts = [
        "Fun fact! The piano of this house was played by Beethoven",
        "Fun fact! In this house Marie Curie died by radiation",
        "Fun fact! The dresser was the one from Narnia",
        "Fun fact! The dining table was the one of the Last Supper",
        "Fun fact! It was the queen bed of Isabel II",
        "Fun fact! It was the sofa of the series Friends"
    ]
    print(random.choice(facts))

def show_inventory():
    print("You have collected:")
    for key in game_state["keys_collected"]:
        print(" 🔑 " + key["name"])
    for item in game_state["items_collected"]:
        print(" 🎒 " + item["name"])

def result(player_moves):
    if player_moves < 12:
        print("¡¡You are a cheater!!")
    elif 12 < player_moves < 16:
        print("You are a bit tryhard")
    elif 16 < player_moves < 19:
        print("Well done")
    else:
        print("You found the exit, but too late — you died from radiation.")

if __name__ == "__main__":
    game_state = INIT_GAME_STATE.copy()
    start_game()