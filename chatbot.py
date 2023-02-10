import gtts
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
from langdetect import detect
import pyttsx3
from rich import print as color
from random import shuffle
gtts_languages = set(gtts.lang.tts_langs().keys())

def info(content, kind='info'):
    """
    This prints info to the terminal in a fancy way
    :param content: This is the string you want to display
    :param kind: bad, info, question, good, topic, plain; changes color
    :return: None
    """

    if kind == 'info':
        color(f'[bold blue]\[[/bold blue][bold white]i[/bold white][bold blue]][/bold blue]: [white]{content}[/white]')

    elif kind == 'bad':
        color(f'[bold red][X][/bold red] [white]{content}[/white]')

    elif kind == 'question':
        color(f'[bold yellow]\[?][/bold yellow] [white]{content}[/white]')
    
    elif kind == 'good':
        color(f'[bold green][OK][/bold green] [white]{content}[/white]')

    elif kind == 'topic':
        color(f'[bold blue]\[[/bold blue][bold white]{content}[/bold white][bold blue]][/bold blue]: ', end='')

    elif kind == 'plain':
        color(f'[white]{content}[/white]')


def get_files_in_dir(directory: str) -> None:
    # This looks inside a directory and gives you a path to all
    # of the files inside it

    filePaths = []

    for fileName in os.listdir(directory):
        filePath = os.path.join(directory, fileName)

        if os.path.isfile(filePath):
            filePaths.append(filePath)

    return filePaths


def robospeak(text: str):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def tts11AI(key: str, text: str, path: str) -> bool:
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
    url = "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL"
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

def talk(text: str, name: str, use11: bool = False, key11: str = '', show_text:bool = True) -> bool:
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
        if use11 and tts11AI(key11, text, f'{file}.mpeg'):  
            playsound(file + '.mpeg')
            return True

        else:
            google_tts(text, f'{file}.mp3', show_text=show_text)
            playsound(file + '.mp3')
            return tts11_okay

    except:
        google_tts(text, f'{file}.mp3', show_text=show_text)
        playsound(file + '.mp3')
        return tts11_okay

def save_conversation(conversation: str, name):
    
    # 1. Setup directory for conversations
    if not os.path.isdir(f'conversations'):  # Make dir if not there
        os.mkdir(f'conversations')

    # 2. Save file
    try:
        with open(f'conversations/{name}', 'w') as file:
            file.write(conversation)
    except:
        try:
            with open(f'conversations/{name}', 'w', encoding='utf-32') as file:
                file.write(conversation)

        except Exception as e:
            info(f'Failed to save conversation to disk: {e}', 'bad')

class Chatbot():
    """
    Chatbot that uses GPT-3
    """
    api_key = None
    api_key_11 = ''
    use11 = False
    conversation = ''
    memories = 'nothing'
    turns = 0
    conversation_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.txt'
    robospeak = False
    reply_tokens = 150
    back_and_forth = []  # This will contain human messages and AI replies
    name = 'AI'
    preset = 'nothing'

    def __init__(self, api_key: str, api_key_11: str = ''):
        
        # 1. Set up apis
        self.api_key = api_key
        openai.api_key = api_key 

        if not api_key_11 == '':
            self.api_key_11 = api_key_11
            self.use11 = True

        # 2. Set up bot memories and init prompt
        self.memories = self.remember()  # This will collect memories
        self.conversation = (f"{self.restore_self()}The following is a conversation with an AI assistant. The AI assistant is helpful, creative," + 
                "clever, very friendly, and supports users like a motivational coach. The AI assistant is able to understand numerous languages and will reply" +
                f" to any messsage by the human in the language it was provided in. The AI's name is {self.name}, but it can be changed with the voice command 'please set name to'. " + 
                f"The AI has the ability to remember important concepts about the user; it currently remembers: {self.memories}." + 
                f"\n\nHuman: Hello, who are you?\n{self.name}: I am an AI created by OpenAI being ran on a Python bot made by Adri6336, called GPT-3 STTC. How" + 
                " can I help you today?")

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
            info(f'Failed to test with OpenAI. Key might be invalid.', 'bad')
            return True

    def say_to_chatbot(self, text: str, outloud: bool = True, show_text:bool = True) -> str:
        """
        This sends a message to GPT-3 if it passes tests, then returns a
        response. Manages advancing the conversation. 
        
        :param text: What you want to say to the bot
        :param outloud: A switch that enables / disables spoken replies.
        :returns: A string containing the response
        """
        if not hostile_or_personal(text) and not self.flagged_by_openai(text):

            # 1. Get response
            start_sequence = "\n{self.name}:"
            restart_sequence = "\nHuman: "
            self.conversation += f'\nHuman: {text}'
            self.back_and_forth.append(f'\nHuman: {text}')

            try:
                response = openai.Completion.create(
                model="text-davinci-003",
                prompt=self.conversation,
                temperature=0.9,
                max_tokens=self.reply_tokens,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0.6,
                stop=[" Human:", f" {self.name}:"]
                )

            except Exception as e:
                if 'server had an error while processing' in str(e):  # If connection issue, try again once more
                    try:
                        response = openai.Completion.create(
                            model="text-davinci-003",
                            prompt=self.conversation,
                            temperature=0.9,
                            max_tokens=self.reply_tokens,
                            top_p=1,
                            frequency_penalty=0,
                            presence_penalty=0.6,
                            stop=[" Human:", f" {self.name}:"]
                            )

                    except Exception as e:
                        info(f'Error communicating with GPT-3: {e}', 'bad')
                        return ''
                
                else:  # If we don't know what happened, don't immediately try again
                    info(f'Error communicating with GPT-3: {e}', 'bad')
                    return ''

            # Cut response and play it
            reply = json.loads(str(response))['choices'][0]['text']

            if show_text:
                info(f'{self.name}\'s Response', 'topic')
                info(self.get_AI_response(reply), 'plain')

            try:
                if outloud and not self.robospeak: 
                    self.use11 = talk(self.get_AI_response(reply), f'{self.turns}',
                                    self.use11, self.api_key_11, show_text=show_text)  # Speak if setting turned on
                
                elif outloud and self.robospeak:
                    robospeak(self.get_AI_response(reply))

            except Exception as e:
                info(f'Error trying to speak: {e}', 'bad')
                self.use11 = False

            # Keep track of conversation
            self.turns += 1
            self.conversation += reply
            self.back_and_forth.append(reply)
            save_conversation(self.conversation, self.conversation_name)

            return reply

        else:
            info('Text flagged, no request sent.', 'bad')
            return '[X] Text flagged, no request sent.'

    def remember(self):
        """
        This sees if a memories file exists. 
        If it does, it will return its contents. Otherwise, it
        will return 'nothing'.
        """
        if os.path.isfile('memories.txt'):
            with open('memories.txt', 'r') as file:
                memories =  file.read()

            memories = memories.replace(' ', '')
            memories = memories.replace('\n', '')
            return memories

        return 'nothing'

    def save_memories(self):
        gpt = GPT3(self.api_key)

        # 0. Create directory for long-term memory storage
        if not os.path.exists('neocortex'): 
            os.mkdir('neocortex')
            memory_name = '1.txt'

        else:
            memory_name = f'{(len(get_files_in_dir("neocortex")) + 1)}.txt'

        # 1. Get the information to remember
        conversation = self.conversation.split('\n')[4:]
        conversation_string = ''
        for line in conversation:
            conversation_string += f'{line}\n'

        if conversation_string == '':
            conversation_string = 'nothing.'

        info('Memories', 'topic')
        print(f'{self.memories}\n')

        info('Conversation', 'topic')
        info(conversation_string, 'plain')

        prompt = ("Create a memory text file with the following format:\n\n" +
                    "{humans_job:[], humans_likes:[], humans_dislikes[], humans_personality:[], facts_about_human:[], things_discussed:[], humans_interests:[], things_to_remember:[]}\n\n" +
                    "Fill the text file in with information you obtain from your previous memories and the conversation. If the conversation is empty, update none of your memories. If you " + 
                    "have no memories and the conversation is empty, create a placeholder text with 'nothing' in each key's list. If the conversation is not empty, fill in the memory text " + 
                    "with as much info as is relevant, using as few words as possible, using natural language processing. Please make as few assumptions as possible when recording memories, " + 
                    "sticking only to the facts avaliable. Please ignore the name \"AI:\", as this is the bot.\n\n" + 
                    f"PREVIOUS_MEMORIES: {self.memories}.\n\n" + 
                    f"CONVERSATION:\n{conversation_string}")

        print(prompt)

        # 2. Remember the info as short term    
        memories = gpt.request(prompt, 500)
        ct = 0

        while memories == '' or memories == '||' and ct > 3:
            memories = gpt.request(prompt)

        memories = memories.replace(' ', '')  # Remove spaces
        memories = memories.replace('\n', '')  # Remove newlines

        info(f'New Memories', 'topic')
        print(memories)
        with open('memories.txt', 'w') as file:
            file.write(f'|{memories}|')

        # 3. Remember the info as long term
        with open(f'neocortex/{memory_name}', 'w') as file:
            file.write(f'|{memories}|')

    def restore_memory(self, max_memories=5):
        """
        This will compile the memories stored in the neocortex
        folder into a new memories.txt file, then save the file
        to current memory.
        """
        gpt = GPT3(self.api_key)
        info(f'Max memories to compile: {max_memories}')

        # 0. Ensure neocortex exists
        if not os.path.exists('neocortex'):  # No memories exist 
            info('Failed to restore memory: neocortex folder does not exist', 'bad')
            return 

        # 2. Try to obtain memories from neocortex
        memory_files = get_files_in_dir('neocortex')
        num_memories = len(memory_files)
        selected_memories = ''
        one_memory = False

        if num_memories == 0:  # No memories exist
            info('Failed to restore memory: neocortex folder is empty', 'bad')
            return
        
        elif num_memories == 1:  # Load the only memory you have
            with open(memory_files[0], 'r') as file:
                self.memories = file.read()
            one_memory = True
            info('1 memory located in neocortex')

        else:  # Grab a number of memories and have GPT-3 compile them into a new memory
            info(f'{num_memories} memories located in neocortex')
            shuffle(memory_files)
            for x, memory_path in enumerate(memory_files):
                if x > max_memories:
                    break

                with open(memory_path, 'r') as file:
                    selected_memory = file.read()
                    selected_memories += f'{selected_memory}\n'
                    info(f'Selected Memory {x}', 'topic')
                    print(f'{selected_memory}\n')


        # 2. Create new memory text
        prompt = ("Create a new single memory text file with the following format:\n\n" +
                    "{humans_job:[], humans_likes:[], humans_dislikes[], humans_personality:[], facts_about_human:[], things_discussed:[], humans_interests:[], things_to_remember:[]}\n\n" +
                    "Fill the text file in with information you compile from your previous memories; preserve as much info as is efficient. Each old memory text is encased in '|' characters. If you " + 
                    "have no memories, create a placeholder text with 'nothing' in each key's list. If the conversation is not empty, fill in the memory text " + 
                    "with as much info as is relevant, using as few words as possible, using natural language processing. Please make as few assumptions as possible when recording memories, " + 
                    "sticking only to the facts avaliable.\n\n" + 
                    f"PREVIOUS_MEMORIES:\n{selected_memories}.\n")
        ct = 0

        if not one_memory:  # If one_memory, the memory will already be loaded
            restored_memories = gpt.request(prompt)

            while restored_memories == '' or restored_memories == '||' and not ct > 3:  # Prevent AI from not making memory
                restored_memories = gpt.request(prompt)
                ct += 1  # Prevent infinite loop, which could be costly

            restored_memories = restored_memories.replace(' ', '')  # Remove spaces
            restored_memories = restored_memories.replace('\n', '')  # Remove newlines
            
            self.memories = restored_memories

        with open('memories.txt', 'w') as file:
            file.write(f'|{self.memories}|')

        info('Compiled Memory', 'topic')
        print(self.memories)
        # 3. Recreate conversation with new memories
        self.restore_conversation()

        info('Memories Successfully Restored', 'good')

    def restore_self(self) -> str:
        """
        This will search for data about self and return a string
        containing what it knows.
        """
        
        # Get date
        now = datetime.now()
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        week_day = datetime.today().weekday()
        day_name = days[week_day]
        today = f'{day_name} (MM-dd-YY) {now.month}-{now.day}-{now.year}'

        # Get name and preset
        # 1. Ensure valid dirs
        if not os.path.exists('neocortex'):  # Memory folder does not exist
            os.mkdir('neocortex')
            os.mkdir('neocortex/self_concept')
            
            with open('neocortex/self_concept/name.txt', 'w') as file:
                file.write('AI')  # Default name is AI

            with open('neocortex/self_concept/preset.txt', 'w') as file:
                file.write('nothing')  # Default preset is nothing

        elif not os.path.exists('neocortex/self_concept'):  # Self concept does not exist; make it
            os.mkdir('neocortex/self_concept')
            
            with open('neocortex/self_concept/name.txt', 'w') as file:
                file.write('AI')  # Default name is AI

            with open('neocortex/self_concept/preset.txt', 'w') as file:
                file.write('nothing')  # Default preset is nothing

        # 2. Ensure data in dirs; get data
        name = ''
        preset = ''

        if not os.path.exists('neocortex/self_concept/name.txt'):  # Name does not exist
            with open('neocortex/self_concept/name.txt', 'w') as file:
                file.write('AI')  # Default name is AI
            name = 'AI'

        else:
            with open('neocortex/self_concept/name.txt', 'r') as file:
                name = file.read()

        if not os.path.exists('neocortex/self_concept/preset.txt'):
            with open('neocortex/self_concept/preset.txt', 'w') as file:
                file.write('nothing')  # Default preset is nothing
            preset = 'nothing'

        else:
            with open('neocortex/self_concept/preset.txt', 'r') as file:
                preset = file.read()

        # 2.2 Test name and preset
        if not name == 'AI' and hostile_or_personal(name) and self.flagged_by_openai(name):  # Disallow policy violation names
            with open('neocortex/self_concept/name.txt', 'w') as file:
                file.write('AI')
            name = 'AI'
            info('Name rejected for potential use policy violation', 'bad')

        if not preset == 'nothing' and hostile_or_personal(name) and self.flagged_by_openai(name):
            with open('neocortex/self_concept/preset.txt', 'w'):
                file.write('nothing')

            preset = 'nothing'
            info('Preset rejected for potential use policy violation', 'bad')
                
        self.preset = preset
        self.name = name
        # 3. Create initialization string
        init_str = f'Today is {today}\nAI\'s preset is {self.preset}.\n'

        return init_str

    def restore_conversation(self, rename=False, old_name=''):
        """
        This will reload the conversation with the bot's info 
        formatted into it. Useful for situations that alter memory or
        presets.
        """
        
        base = (f"{self.restore_self()}The following is a conversation with an AI assistant. The AI assistant is helpful, creative," + 
                "clever, very friendly, and supports users like a motivational coach. The AI assistant is able to understand numerous languages and will reply" +
                f" to any messsage by the human in the language it was provided in. The AI's name is {self.name}, but it can be changed with the voice command 'please set name to'. " + 
                f"The AI has the ability to remember important concepts about the user; it currently remembers: {self.memories}." + 
                f"\n\nHuman: Hello, who are you?\n{self.name}: I am an AI created by OpenAI being ran on a Python bot made by Adri6336, called GPT-3 STTC. How" + 
                " can I help you today?")

        conversation = ''
        new_messages = []

        if not rename:
            for message in self.back_and_forth:
                    conversation += message

        else:
            for message in self.back_and_forth:
                new_message = message.replace(old_name, self.name)
                new_messages.append(new_message)
                conversation += new_message

        base += conversation

        if rename: 
            self.back_and_forth = new_messages  # Save edited list of messages 

        info(base)

        self.conversation = base

    def set_self(self, data: str, data_type: str) -> bool:
        """
        This will create or modify files in the neocortex file.

        :param data: This is the text you want to set
        :param data_type: This is what kind of data you want to set (name or preset)
        :return: None
        """
        # 1. Ensure pathways exist
        self.restore_self()  # This will create the necesary paths.
            
        # 2. Create / modify files
        data = data.replace('\n', '')
        
        if hostile_or_personal(data) and self.flagged_by_openai(data):
            info('Update may be in violation of OpenAI\'s usage policy and has been rejected', 'bad')
            return False

        if data_type == 'name':
            with open('neocortex/self_concept/name.txt', 'w') as file:
                file.write(data)
            self.name = data

        elif data_type == 'preset':
            with open('neocortex/self_concept/preset.txt', 'w') as file:
                file.write(data)  
            self.preset = data

        # 3. Recreate conversation
        self.restore_conversation()

        return True

    def get_AI_response(self, text: str) -> str:
        """
        This returns all the text following the first 
        instance of a colon
        """
        sections = text.split(f'{self.name}:')
        try:
            target = sections[1]

        except Exception as e:
            info(f'\nError occurred while trying to separate "{self.name}:" from response {e}', 'bad')
            target = text

        return target

    def change_name(self, new_name:str):
        self.restore_self()
        clean_name = new_name.replace(' ', '')
        clean_name = clean_name.replace('\n', '')

        if not hostile_or_personal(new_name) and not self.flagged_by_openai(new_name):
            with open('neocortex/self_concept/name.txt', 'w') as file:
                file.write(clean_name)

            old_name = self.name
            self.name = clean_name
            self.restore_conversation(True, old_name)
            return True

        else:
            return False
        


class GPT3(Chatbot):
    """
    This is a barebones tool to request something from 
    GPT-3. It's made into a separate class so as to not
    interfere with the chatbot.
    """

    def request(self, text:str, tokens: int = 1000):
        if not hostile_or_personal(text) and not self.flagged_by_openai(text):

            # 1. Get response
            response = openai.Completion.create(
            model="text-davinci-003",
            prompt=text,
            temperature=0.9,
            max_tokens=tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            )

            # Cut response and play it
            reply = json.loads(str(response))['choices'][0]['text']
            return reply

# Ensure that nltk is downloaded
try:
    nltk.download('punkt', quiet=True, raise_on_error=True)
    nltk.download('averaged_perceptron_tagger', quiet=True, raise_on_error=True)
    nltk.download('maxent_ne_chunker', quiet=True, raise_on_error=True)
    nltk.download('words', quiet=True, raise_on_error=True)
    info('NLTK Loaded', 'good')

except Exception as e:
    if 'getaddrinfo failed' in str(e):  # Notify that you have a connection issue
        info('Failed to download NLTK data', 'bad')
        info('Testing if NLTK requirements met ... ')
    
    else:  # If some other issue presents, exit
        info(f'Unexpected error while downloading NLTK data: {e}')
        exit(2)

    # Test to see if NLTK requirements met
    try:
        hostile_or_personal('Thats pretty wack yo')
        info('NLTK Requirements Met', 'good')
    
    except Exception as e:
        info('NLTK requirements not met', 'bad')
