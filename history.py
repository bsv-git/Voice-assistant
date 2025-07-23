# history.py
import json

def save_interaction(user_input, response):
    data = {"user": user_input, "assistant": response}
    with open("history.json", "a") as file:
        file.write(json.dumps(data) + "\n")