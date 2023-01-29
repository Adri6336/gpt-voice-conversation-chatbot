# gpt3-speech-to-text-chatbot (GPT-3 STTC)

This is a bot that allows you to have a spoken conversation with GPT-3 using your microphone. The tool uses GPT-3's chat preset and handles keeping track of the conversation. You can tell GPT-3 something and it will remember what you said for the session. In order to use this tool, you need a valid OpenAI API key.

The bot requires OpenAI's moderation and GPT-3 apis to be working properly without too much latency. You can find the status here: https://status.openai.com/

# Using GPT-3 STTC

To use this STTC, you'll need to clone the repository, install the requirements, then navigate to the repository's folder using a terminal or powershell.
Be sure to have a working mic connected. Once in the repository's folder, use the following command (replacing \<key\> with your api key):

    python main.py <key>
    
A Pygame gui will pop up; its colors represent the state of the bot. The color red indicates that the bot is not listening. To make the bot listen to you,
press space. The color will then turn to yellow when its loading, then green when it's listening. Speak freely when the color is green, your speech will
be recorded, converted to text, then fed to GPT-3 if it is in compliance with OpenAI's policies. When GPT-3 is ready to reply, the screen will turn blue.

Press 'q' to exit.

If you would like to use [ElevenLabs TTS](https://beta.elevenlabs.io/speech-synthesis), you must enter your personal ElevenLabs api key following your OpenAI api key as follows:

        python main.py <OpenAI key> <ElevenLabs TTS key>

If you don't want to use the fancy TTS, this bot will use Google's TTS.

# Content Moderation

The moderation uses both OpenAI's moderation tool and NLTK. Combined, they hope to prevent the use of GPT-3 that is outside of OpenAI's useage policy.
This is not an infaliable method though, so please exercise caution with what you give GPT-3.

Please not that outages or latency problems with the moderation api will prevent you from using this chatbot. If you must talk with the bot while
OpenAI is having issues, please edit the chatbot.py file to exclude the "not self.flagged_by_openai(text)" condition. I do not recommend this though.


# Planned Features

- Make a setting where the bot can remember speaking with you between sessions, recalling only important bits of info.

- Make interface run more smoothly
