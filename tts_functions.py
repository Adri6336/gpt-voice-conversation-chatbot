import pyttsx3
import requests
import gtts
from gtts import gTTS
import os
from playsound import playsound
from datetime import datetime
from langdetect import detect
from general_functions import *
import json
from elevenlabs import generate, play, save
gtts_languages = set(gtts.lang.tts_langs().keys())


def robospeak(text: str):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def tts11Multi(key: str, text: str, path: str, voice_id: str = 'EXAVITQu4vr4xnSDxMaL'):
    audio = generate(
    text=text,
    voice=voice_id,
    model='eleven_multilingual_v1',
    api_key=key
)
    save(audio, filename=path)

def tts11AI(key: str, text: str, path: str, voice_id: str = 'EXAVITQu4vr4xnSDxMaL') -> bool:
    """
    This uses ElevenLab's AI to generate text to speech.

    :param key: This is your 11.ai key
    :param text: What you want spoken
    :param path: Where you want your file saved
    """

    # create a session object 
    s = requests.Session()

    # set the headers
    headers = {
        "accept": "audio/mpeg",
        "xi-api-key": key,
        "Content-Type": "application/json",
    }

    # set the payload
    payload = {
        "text": text
    }

    # make the post request
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    try:
        r = s.post(url, data=json.dumps(payload), headers=headers, timeout=60)
        if r.status_code != 200:
            return False

        # save the response content
        with open(path, 'wb') as f:
            f.write(r.content)
    except requests.exceptions.Timeout:
        return False

    except Exception as e:
        info(f'Unexpected error: {e}', 'bad')
        return False
    
    return True

def google_tts(text: str, path: str, show_text:bool = True):

    language = detect(text)
    if show_text: info(f'DETECTED LANGUAGE: {language}')
    
    if language in gtts_languages:  # Pronounce correctly if possible
        tts = gTTS(text, lang=language)
        tts.save(path)

    elif language == 'zh-cn':
        tts = gTTS(text, lang='zh-CN')
        tts.save(path)

    elif language == 'zh-tw':
        tts = gTTS(text, lang='zh-TW')
        tts.save(path)

    else:  # Otherwise just use English pronounciation
        tts = gTTS(text)
        tts.save(path)

def talk(text: str, name: str, use11: bool = False, key11: str = '', 
         show_text:bool = True, eleven_voice_id: str = 'EXAVITQu4vr4xnSDxMaL') -> bool:
    """
    This will provide a sound file for what ever you enter, then 
    play it using playsound. Saves an mp3 file.

    :param text: This is what you want to be converted to speech
    :param name: This is what you want the mp3 file to be called 
    """

    tts11_okay = False

    # 1. Set up name
    now = datetime.now()
    today = f'{now.month}-{now.day}-{now.year}'
    file = f'./messages/{today}/{name}'

    if not os.path.isdir(f'messages'):  # Make primary dir if not there
        os.mkdir(f'messages')

    if not os.path.isdir(f'./messages/{today}'):
        os.mkdir(f'./messages/{today}')

    if os.path.isfile(file + '.mpeg'):  # Delete file if it's already there
        os.remove(file + '.mpeg')
    
    elif os.path.isfile(file + '.mp3'):
        os.remove(file + '.mp3')

    # 2. Have gtts create file
    try:
        if use11:  
            tts11Multi(text=text, key=key11, voice_id=eleven_voice_id, path=f'{file}.mpeg')
            playsound(f'{file}.mpeg')
            return True

        else:
            google_tts(text, f'{file}.mp3', show_text=show_text)
            playsound(file + '.mp3')
            return tts11_okay

    except Exception as e:
        google_tts(text, f'{file}.mp3', show_text=show_text)
        playsound(file + '.mp3')
        return tts11_okay