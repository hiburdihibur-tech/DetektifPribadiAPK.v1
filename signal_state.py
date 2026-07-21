import json
import os

FILE = "signal_state.json"


def load_state():

    if not os.path.exists(FILE):
        return {}

    with open(FILE, "r") as f:
        return json.load(f)


def save_state(data):

    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


def already_sent(symbol):

    data = load_state()

    return data.get(symbol, False)


def mark_sent(symbol):

    data = load_state()

    data[symbol] = True

    save_state(data)


def reset_symbol(symbol):

    data = load_state()

    data[symbol] = False

    save_state(data)