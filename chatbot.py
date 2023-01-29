from gtts import gTTS
from playsound import playsound
import os
import json
import openai
import requests
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk import ne_chunk, pos_tag
from nltk.tokenize import word_tokenize
from datetime import datetime


def get_AI_response(text: str) -> str:
    """
    This returns all the text following the first 
    instance of a colon
    """
    sections = text.split('AI:')
    return sections[1]

def hostile_or_personal(text: str) -> bool:
    """
    This tests the text to see if it is hostile
    or references a person. This test is done by
    your computer and should be done before
    testing with OpenAI.
    :param text: This is the text you want to test.
    :return: bool regarding status. If true, reject text
    """

    # Sentiment Analysis
    sid = SentimentIntensityAnalyzer()
    scores = sid.polarity_scores(text)
    negative_score = scores['neg']

    # Named Entity
    named_entities = []
    chunked = ne_chunk(pos_tag(word_tokenize(text)))
    for chunk in chunked:
        if hasattr(chunk, 'label'):
            named_entities.append(chunk.label())

    # Check for manipulation
    if (negative_score > 0.5) or ('PERSON' in named_entities and negative_score > 0.3):
        return True
    else:
        return False

def talk(text: str, name: str):
    """
    This will provide a sound file for what ever you enter, then 
    play it using playsound. Saves an mp3 file.

    :param text: This is what you want to be converted to speech
    :param name: This is what you want the mp3 file to be called 
    """

    # 1. Set up name
    now = datetime.now()
    today = f'{now.month}-{now.day}-{now.year}'
    file = f'./messages {today}/{name}.mp3'

    if not os.path.isdir(f'messages {today}'):  # Make dir if not there
        os.mkdir(f'messages {today}')

    if os.path.isfile(file):  # Delete file if it's already there
        os.remove(file)

    # 2. Have gtts create file
    tts = gTTS(text)
    tts.save(file)

    # 3. Have playsound play file
    playsound(file)


class Chatbot():
    """
    Chatbot that uses GPT-3
    """
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('maxent_ne_chunker')
    nltk.download('words')
    api_key = None
    conversation = ("The following is a conversation with an AI assistant. The assistant is helpful, creative," + 
                "clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How" + 
                " can I help you today?")
    turns = 0

    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = api_key

    def flagged_by_openai(self, text: str) -> bool:
        """
        Tests text using OpenAI api. If it fails or is flagged, return false.
        :param text:
        :return: bool representing if the material is flagged or something else.
        A return of False means the text is good to go
        """
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            data = {"input": text}
            response = requests.post("https://api.openai.com/v1/moderations", headers=headers, json=data)
            return json.loads(response.text)['results'][0]['flagged']  # This is a bool

        except Exception as e:
            print(f'[X] Failed to test with OpenAI. Key might be invalid.')
            return True

    def say_to_chatbot(self, text) -> str:
        """
        This translates text into Latin
        :param text: Whatever text you want translated into Latin
        :return: Latin text if accepted or an error message
        """
        if not hostile_or_personal(text) and not self.flagged_by_openai(text):

            # 1. Get response
            start_sequence = "\nAI:"
            restart_sequence = "\nHuman: "
            self.conversation += f'\nHuman: {text}'

            response = openai.Completion.create(
            model="text-davinci-003",
            prompt=self.conversation,
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=[" Human:", " AI:"]
            )

            # Cut response and play it
            reply = json.loads(str(response))['choices'][0]['text']
            talk(get_AI_response(reply), f'{self.turns}')
            self.turns += 1
            self.conversation += reply
            return reply

        else:
            print('[X] Text flagged, no request sent.')
            return '[X] Text flagged, no request sent.'