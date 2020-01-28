from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr
from info import *
import sys
import time
import json
import random
import subprocess



class Jarvis(object):
    """
    Handles the bulk of call/response mechanics.
    
    See imported weather modules for API calls and json parsing.
    """
    def __init__(self, launch_phrase='jarvis', debugger_enabled=False):
        self.launch_phrase = launch_phrase
        self.debugger_enabled = debugger_enabled
        self.actively_listening = False
        with open('audio.json') as f:
            self.audio_paths = json.load(f)
        self.command_dict = {'weather': get_weather_from_jarvis,
                             'date': get_date_from_jarvis,
                             'thank': self.jarvis_stop_listening,
                             'thanks': self.jarvis_stop_listening,
                             'introduce': self.introduction,
                             'off': self.jarvis_off,
                             'recognition_error': self.jarvis_recognition_error,
                             'request_error': self.jarvis_request_error,
                             'terminate': self.shut_down_machine}


    def listen_for_audio(self):
        """
        Initializes recognizer/microphone and listens for audio. 
        
        Returns audio recognizer and audio objects.
        """
        r = sr.Recognizer()
        mic = sr.Microphone()
        with mic as source:
            r.adjust_for_ambient_noise(source)
            print("I'm listening")
            audio = r.listen(source)

        print("Found audio")
        return r, audio


    def recognize_speech(self, recognizer, audio):
        """Retrieves text from Google Speech-to-text API, given voice audio and recognizer"""
        speech = None
        try:
            speech = recognizer.recognize_google(audio)
            print("You said:", speech)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            speech = 'recognition_error'
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            speech = 'request_error'
        finally:
            return speech


    def is_call_to_action(self, speech):
        """
        Verifies if launch phrase was spoken or not.
        
        If so, responds with Jarvis affirmation.
        """
        if speech is not None and self.launch_phrase in speech.lower():
            self.jarvis_response(random.choice(audio_paths['greetings']))
            return True

        return False


    def parse_speech_for_commands(self):
        """
        Initializes listener, translates to text, and parses to determine proper response.
        """

        # Begins actively listening (until told to stop)
        self.actively_listening = True

        while self.actively_listening:

            # Listen
            r, audio = self.listen_for_audio()

            # Translate to text
            speech = self.recognize_speech(r, audio)

            # Build command queue
            command_queue = []

            for word in speech.lower().split():
                if word in self.command_dict:
                    command_queue.append(self.command_dict[word])

            # Execute commands
            for command in command_queue:
                command()

            if not command_queue:
                self.no_keywords_found()

            # Re-prompt "awaiting instructions"
            if self.actively_listening:
                time.sleep(1)
                self.jarvis_response("Audio/Greeting/caged_listening_on_3.wav")


    def jarvis_response(self, audio_path):
        """Plays given audio file"""
        response = AudioSegment.from_wav(audio_path)
        play(response)


    def introduction(self):
        """
        Jarvis introduces himself.

        KEYWORD: 'introduce'
        """
        self.jarvis_response("Audio/Greeting/caged_intro_2.wav")

    
    def jarvis_stop_listening(self):
        """
        Ends active listening.
        
        KEYWORD: 'thank(s)'
        """
        self.jarvis_response("Audio/Other/caged_confirm_10_s.wav")
        self.actively_listening = False


    def jarvis_off(self):
        """
        Switches Jarvis off entirely.
        
        KEYWORD: 'off'
        """
        self.jarvis_response(random.choice(self.audio_paths["other"]["switch_off"]))
        time.sleep(1)
        sys.exit()


    def jarvis_recognition_error(self):
        """Responds with audio error message when google cannot recognize speech"""
        self.jarvis_response("Audio/Other/caged_repeat_3.wav")

    
    def jarvis_request_error(self):
        """Reponds with audio when google cannot be reached"""
        self.jarvis_response("Audio/Other/caged_network_lost_wifi.wav")


    def no_keywords_found(self):
        """Reponds with audio when no keywords are found in speech"""
        self.jarvis_response("Audio/Other/caged_unavailable_0.wav")


    def shut_down_machine(self):
        """
        Shuts off the host machine.
        
        KEYWORD: 'terminate'
        """
        self.jarvis_response(random.choice(self.audio_paths["other"]["switch_off"]))
        time.sleep(1)
        subprocess.call(['osascript', '-e', 'tell app "System Events" to shut down'])


    def start(self):
        """Start Jarvis"""
        while True:
            recognizer, audio = self.listen_for_audio()
            speech = self.recognize_speech(recognizer, audio)
            if self.is_call_to_action(speech):
                self.parse_speech_for_commands()



def main():
    s = Jarvis()
    s.start()


if __name__ == '__main__':
    main()
