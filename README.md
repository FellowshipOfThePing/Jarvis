# Jarvis #

Jarvis is a homemade virtual assistant, built using audio of Paul Bettany’s ‘Jarvis’ voice and Google's speech recognition API. In this repository he is paired with a voice-interactive Tkinter UI, but could easily be used on his own.

For copyright reasons, I will not be distributing the audio files used to create this program, but they are relatively easy to find using Google, and you can see Jarvis in action [here](https://youtu.be/CrxmwC2pocQ)


## How does he work? ##

Jarvis' primary functionality is based on the Jarvis.py file, which is run in parallel with the smartmirror.py file by running the Start.sh script.

Once initialized, Jarvis listens for his name. Until he hears his name, he will not speak, but will always be listening.

When activated using his name, you can ask him anything. At this point in production, there's a good chance he'll respond to most things with the default 'I can't do that right now', but the way he's built leaves room for a lot of new actions.

He listens for keywords (listed below), and depending on the combination and sequence of keywords, will respond in various ways.

If given multiple keywords in a single command, he will compile a list of commands, and execute them in the same sequence they were given.


## Voice Keywords/Commands ##

| Keyword(s)    | Response  (Audio)                                |
| ------------- |:------------------------------------------------:|
| Introduce     | Plays pre-recorded introduction response         |
| Weather       | Current conditions from weather API              |
| Date          | Current date from datetime module                |
| Time          | Current time from datetime module                |
| Summary       | Calls weather, date, and time commands           |
| Show/Hide     | Toggles given UI features (UI keywords below)    |
| Thank(s)      | Returns to inactive listening (waiting for name) |
| Off           | Ends Program                                     |
| Terminate     | Shuts down host computer (intended for RPI)      |



## UI Keywords/Commands ##

These commands will toggle the status of the corresponding UI elements in the config.json file, ultimately changing their visibility on the screen.

You must first say 'hide' or 'show', and Jarvis will interpret everything after that as a UI command.

| Keyword(s)    | Action                  |
| ------------- |:-----------------------:|
| Weather       | Toggle Weather UI       |
| Date/Time     | Toggle Date & Time UI   |
| News/Headlines| Toggle News UI          |



## Todo List ##

- [ ] Raspberry Pi Integration
- [x] Convert .caf files to .mp3 & .wav
- [x] Fix absolute files paths in audio.json
- [ ] Local Calendar/Reminder Integration
- [ ] Synchronize UI changes (refresh rate)
- [ ] Replace Google Speech API with local DNN
- [ ] Embed demonstration video

