# gpt-voice-conversation-chatbot (GPT-VCC) (formerly GPT3-STTC)

(Used to be called gpt3-speech-to-text-chatbot, but was changed due to plans to add ability to swap model if desired)

This is a bot that allows you to have an engaging and safely emotive spoken conversation with ChatGPT using your microphone. If you'd prefer to type rather than speak, you can also converse with the bot via the terminal.

The tool uses a modified GPT chat preset, handles keeping track of the conversation, and uses ChatGPT's API by default. You can tell GPT something and it will remember what you said for the session and you can also have the bot develop a memory of you over time if you'd like. Despite limitations based on GPT's max token count, GPT-VCC should still be able to converse with you for as long as you'd like without losing awareness about what you've talked about. In order to use this tool, you will need a valid OpenAI API key.

The bot requires OpenAI's moderation and GPT APIs to be working properly without too much latency. You can find the status here: https://status.openai.com/

The releases are stable, as far as previous testing goes, but will not have all of the newest features. If you would like to have all the features as listed here, clone the repository and run 'git pull' every now and then. This will get you the newest features and bug fixes as they come, but it could be unstable. 

![_image_](https://github.com/Adri6336/gpt3-speech-to-text-chatbot/blob/main/bot.jpeg)

<sup>(Note: wiseTech is the name my bot instance chose for itself)</sup>

# Installing

First off, you'll need an OpenAI API key. You can create an account to get an API key here: https://openai.com/api/ .

### Windows

1. Download Python at https://www.python.org/

2. Download this repo either via the releases like [v0.9.9.1](https://github.com/Adri6336/gpt3-speech-to-text-chatbot/archive/refs/tags/v0.9.9.1.zip), git cloning the repo, or pressing the code button towards the upper right and pressing "Download ZIP".

3. Extract contents, then move into folder with the files.

4. If you have Windows Terminal installed, right click the empty part of the folder and select 'Open in Terminal'. Otherwise, use Win + R and enter powershell. Once you're in a terminal window and at the proper directory, use "pip install -r requirements.txt". If this is done successfully, you should be ready to go as soon as you get yourself an OpenAI API key.

5. Follow the steps listed in Using GPT-VCC


### Linux (Debian / Ubuntu based)

1. Install pip3

        sudo apt install python3-pip
        
2. Download this repo either via the releases like [v0.9.9.1](https://github.com/Adri6336/gpt3-speech-to-text-chatbot/archive/refs/tags/v0.9.9.1.zip), git cloning the repo, or pressing the code button towards the upper right and pressing "Download ZIP".

3. Extract files, move into directory, open requirements.txt, and delete pyaudio==0.2.13 from file. Make it look like it was never there, preserving the original formatting.

4. Download pyaudio with apt as follows:

        sudo apt install python3-pyaudio
        
5. Download espeak with apt as follows (needed for interface communication):

        sudo apt install espeak
        
6. Download other requirements with pip as follows:

        pip3 install -r requirements.txt
        
7. Follow the steps listed in Using GPT-VCC


# Using GPT-VCC

To use this chatbot, enter the following command once you've navigated to the bot's folder (replacing \<key\> with your api key):

    python main.py <key>
    
For convenience, you can also just enter the key into the keys.txt file. When you run the script, the bot will automatically read this file and load the key.

A Pygame gui will pop up; its colors represent the state of the bot. The color red indicates that the bot is not listening. To make the bot listen to you, press space. The color will then turn to yellow when its loading, then green when it's listening. Speak freely when the color is green, your speech will be recorded, converted to text, then fed to GPT if it is in compliance with OpenAI's policies. When GPT is ready to reply, the screen will turn blue.

If you would like to use the terminal, run gptcli.py instead using the same syntax (having keyfile also works):

    python gptcli.py <key>

If you would like to use [ElevenLabs TTS](https://beta.elevenlabs.io/speech-synthesis), you must enter your personal ElevenLabs api key following your OpenAI api key as follows or fill in the key in the key file:

        python main.py <OpenAI key> <ElevenLabs TTS key>

If you don't want to use the fancy TTS, this bot will automatically use Google's TTS.

# Content Moderation

The moderation uses both OpenAI's moderation tool and NLTK. Combined, they hope to prevent the use of GPT that is outside of OpenAI's useage policy. This is not an infaliable method though, so please exercise caution with what you give GPT.

Please note that outages or latency problems with the moderation api will prevent you from using this chatbot. If you must talk with the bot while OpenAI is having issues, please edit the chatbot.py file to exclude the "not self.flagged_by_openai(text)" condition. I do not recommend this though.


# Controls

#### Keyboard

- **SPACEBAR**: This starts a recording. Whatever you say will be then transcribed and sent to GPT (if it passes filters).

- **ESCAPE**: This exits without memorizing.

- **Q**: This quits and has bot remember details about you and your conversations (data is saved in the text file called memories.txt)

- **P**: This attempts to cancel a request to GPT. It will either prevent transcribing of message or will avoid sending it to GPT.

#### Voice Commands (All work with CLI version too except for the robot-speaking commands)

- **Say 'please set tokens to #'**: When the bot recognizes this phrase, it will try to set the max_tokens of the reply to the value you specified.

- **Say 'speak like a robot'**: This will set all responses from GPT to be spoken with a robotic TTS program that works offline.

- **Say 'stop speaking like a robot'**: This will revert bot's TTS to whatever you had before (either Google or ElevenLabs TTS).

- **Say 'please display conversation'**: This will output your entire conversation to the terminal window.

- **Say 'please display memories'**: This will provide an output of all memories saved into long term storage.

- **Say 'please restore memory'**: This will attempt to repair the working memory of the bot by consolidating a certain number of memories from the long term storage .

- **Say 'please set preset to'**: This will set the preset (a text string given to AI at start of every conversation) for the bot. For example, the preset 'speak like a pirate' makes AI speak like a pirate.

- **Say 'please reset preset'**: This will delete the preset you made.

- **Say 'please set name to'**: This will set the name of the bot to whatever you specify, so long as it is in accordance with OpenAI's usage policies. After setting name, the bot will refer to itself by the name you set.


# Features

- Have a personalized conversation with ChatGPT

- Hear GPT talk to you with Google's TTS tool (will pronounce accents accurately if it can), in ElevenLab's life-like TTS (if you have a valid api key), or as a robot (say "speak like a robot" to activate)

- Speak with GPT outloud using Google's speech recognition tech  

- Bot will remember things about you if you close with the 'Q' key

- See GPT's replies as text in the terminal window. Most UTF-32 characters (like Chinese and Arabic text) will also be printed

- Automatically save conversations to a file on your disk to help you keep track of what you've talked about 

- Save a custom preset to have an experience better suited for you and your needs

- Customize the bot's name

- Chat with GPT via the terminal (Windows and Linux)

# Example Use Cases

- Converse with bot recreationally

- Use bot via terminal to practice a language by a setting preset to talk to you in that language like a teacher, and entering '!speak()' with google TTS to pronounce the bot's reponses in that language properly

- Have bot help you practice programming by asking you questions and giving feedback on your code

- Ask bot questions over various things that pop up

- Ask bot to help you with writing cover letters and descriptions
