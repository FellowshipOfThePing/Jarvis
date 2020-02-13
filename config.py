# Config functions for toggling ui status values in config.json
# TODO: Consider refactoring toggle functions into individual on/off functions

import json


def toggle_weather_ui():
    """Change boolean value for 'weather_ui_on' in config.json"""

    # Open config file, load as dictionary
    with open("config.json", "r") as f:
        config = json.load(f)

    # Modify boolean value
    config["weather_ui_on"] = not config["weather_ui_on"]

    # Dump back to file
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)


def toggle_news_ui():
    """Change boolean value for 'news_ui_on' in config.json"""

    # Open config file, load as dictionary
    with open("config.json", "r") as f:
        config = json.load(f)

    # Modify boolean value
    config["news_ui_on"] = not config["news_ui_on"]

    # Dump back to file
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)


def toggle_time_ui():
    """Change boolean value for 'time_ui_on' in config.json"""
    # Open config file, load as dictionary
    with open("config.json", "r") as f:
        config = json.load(f)

    # Modify boolean value
    config["time_ui_on"] = not config["time_ui_on"]

    # Dump back to file
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)


def toggle_ui():
    """Change boolean value for 'ui_on' in config.json"""
    # Open config file, load as dictionary
    with open("config.json", "r") as f:
        config = json.load(f)

    # Modify all boolean values
    if config["ui_on"]:
        config["weather_ui_on"] = False
        config["news_ui_on"] = False
        config["time_ui_on"] = False
        config["ui_on"] = False
    else:
        config["weather_ui_on"] = True
        config["news_ui_on"] = True
        config["time_ui_on"] = True
        config["ui_on"] = True

    # Dump back to file
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)


def jarvis_change_ui(*args):
    """
    Show/hide UI elements based on speech input.

    KEYWORD(s): 'show', 'hide'
    """

    # List speech and keywords/functions
    speech = args[0].split()
    keywords = {
        'weather': toggle_weather_ui,
        'time': toggle_time_ui,
        'date': toggle_time_ui,
        'news': toggle_news_ui,
        'headlines': toggle_news_ui
    }

    # Create command queue and execute
    command_queue = []
    for word in speech:
        if word.lower() in keywords:
            command_queue.append(keywords[word])

    for command in command_queue:
        command()

    # Return True break value to break out of main command loop in Jarvis.py
    return True


def main():
    pass


if __name__ == '__main__':
    main()