# Methods to retrieve API information and parse into Jarvis audio

import requests
import json
import traceback
from math import floor
from pydub import AudioSegment
from pydub.playback import play
import random
import time
import datetime
import os


# Location Data
geolocation_api_token = os.environ.get("GEO_LOCATE_KEY") # https://ipgeolocation.io/
weather_api_token = os.environ.get("WEATHER_KEY")        # https://darksky.net/dev/
weather_lang = 'en'
weather_unit = 'us'         
latitude = None             
longitude = None


# Collect and convert JSON data
with open("audio.json") as f:
    audio_paths = json.load(f)


def get_ip():
    """
    Retrieve IP address from jsonip API
    """
    try:
        ip_url = "http://jsonip.com/"
        req = requests.get(ip_url)
        ip_json = json.loads(req.text)
        return ip_json['ip']
    except Exception as e:
        traceback.print_exc()
        return f"Error: {e}. Cannot get ip."


def get_weather_from_api():
    """
    Retrieve weather data from darksky API
    """
    try:
        if latitude is None and longitude is None:
            # get location
            location_req_url = f"https://api.ipgeolocation.io/ipgeo?apiKey={geolocation_api_token}&ip={get_ip()}"
            r = requests.get(location_req_url)
            location_obj = json.loads(r.text)

            lat = location_obj['latitude']
            lon = location_obj['longitude']

            # get weather
            weather_req_url = f"https://api.darksky.net/forecast/{weather_api_token}/{lat},{lon}?lang={weather_lang}&units={weather_unit}"
        else:
            # get weather
            weather_req_url = f"https://api.darksky.net/forecast/{weather_api_token}/{latitude},{longitude}?lang={weather_lang}&units={weather_unit}"

        r = requests.get(weather_req_url)
        weather_obj = json.loads(r.text)
        return weather_obj

    except Exception as e:
        traceback.print_exc()
        print(f"Error: {e}. Cannot get weather.")


def get_weather_from_jarvis(*args):
    """
    Parse weather information and return as speech
    
    KEYWORD: 'weather'
    """
    
    data = get_weather_from_api()

    # Get temperature audio
    temp = floor(data["currently"]["temperature"])
    if temp <= 60:
        temp_audio = AudioSegment.from_wav(audio_paths["numbers"][str(temp)])
    else:
        temps_ones = temp % 10
        temp_ones_audio = AudioSegment.from_wav(audio_paths["numbers"][str(temp_ones)])
        temp_tens = temp - temp_ones
        temp_tens_audio = AudioSegment.from_wav(audio_paths["numbers"][str(temp_tens)])
        temp_audio = temp_tens_audio + temp_ones_audio

    # Get condition audio
    condition = data["currently"]["icon"]
    condition_response = AudioSegment.from_wav(audio_paths["weather"][condition])

    # Concatenate temp audio and play
    prefix = AudioSegment.from_wav(random.choice(audio_paths["weather"]["current_temp"]))
    degrees = AudioSegment.from_wav(audio_paths["weather"]["degrees"])
    fahrenheit = AudioSegment.from_wav(audio_paths["weather"]["fahrenheit"])
    temp_response = prefix + temp_audio + degrees + fahrenheit
    play(temp_response + condition_response)


def get_date_from_jarvis(*args):
    """
    Parse date information from datetime modules and return as speech.
    
    KEYWORD: 'date'
    """
    
    # TODO: Consider creating individual methods for this as well. Ex: "What year/month/day is it?"

    # Get date in text
    weekday = str(datetime.datetime.today().weekday())
    today = str(datetime.date.today()).split('-')
    month = today[1]
    day = today[2]

    # Convert date to audio
    weekday_audio = AudioSegment.from_wav(audio_paths['dates']['days'][weekday])
    month_audio = AudioSegment.from_wav(audio_paths['dates']['months'][month])
    day_audio = AudioSegment.from_wav(audio_paths['dates']['numbers'][day])
    it_is = AudioSegment.from_wav(audio_paths['dates']['it_is'])

    # Concatenate response and playback
    date_response = it_is + weekday_audio + month_audio + day_audio
    play(date_response)


def get_time_from_jarvis(*args):
    """
    Retrieve time information from datetime modules and return as speech.

    KEYWORD: 'time'
    """

    # Get time in text
    time_list = str(datetime.datetime.now())[11:16].split(':')
    hour = time_list[0]
    minute = time_list[1]

    # Determine if AM or PM
    if int(hour) <= 12:
        meridiem = 'AM'
    else:
        meridiem = 'PM'

    # Revert hour value to 12 hour time scale
    if hour != '12':
        hour = str(int(hour) % 12)

    # Convert time to audio
    it_is_now = AudioSegment.from_wav(audio_paths["times"]["now"])
    hour_audio = AudioSegment.from_wav(audio_paths["numbers"][hour])
    minute_audio = AudioSegment.from_wav(audio_paths["numbers"][minute])
    meridiem_audio = AudioSegment.from_wav(audio_paths["times"]["meridiem"][meridiem])

    # Concatenate response and playback
    time_response = it_is_now + hour_audio + minute_audio + meridiem_audio
    play(time_response)


def get_summary_from_jarvis(*args):
    """
    Call all following commands from Jarvis:
        Weather
        Date
        Time

    KEYWORD: 'summary'
    """
    get_date_from_jarvis()
    get_time_from_jarvis()
    get_weather_from_jarvis()



def main():
    pass


if __name__ == '__main__':
    main()