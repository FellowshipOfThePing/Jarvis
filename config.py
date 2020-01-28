# File for configuring interface settings like UI visibility - reference config.json
# TODO: Refactor toggle functions, maybe just a single 'hide' and single 'show', change values based on args?
import json


def toggle_weather_ui():
    # Open config file, load as dictionary
    with open("config.json", "r") as f:
        config = json.load(f)

    # Modify preference
    config["weather_ui_on"] = not config["weather_ui_on"]

    # Dump back to file
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)


def toggle_news_ui():
    # Open config file, load as dictionary
    with open("config.json", "r") as f:
        config = json.load(f)

    # Modify preference
    config["news_ui_on"] = not config["news_ui_on"]

    # Dump back to file
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)


def toggle_time_ui():
    # Open config file, load as dictionary
    with open("config.json", "r") as f:
        config = json.load(f)

    # Modify preference
    config["time_ui_on"] = not config["time_ui_on"]

    # Dump back to file
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)


def toggle_ui():
    # Open config file, load as dictionary
    with open("config.json", "r") as f:
        config = json.load(f)

    # Modify preferences
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
    Shows/hides UI elements based on speech.

    KEYWORD(s): 'show', 'hide'
    """
    # List speech and keywords
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
    jarvis_change_ui("show me the weather")


if __name__ == '__main__':
    main()