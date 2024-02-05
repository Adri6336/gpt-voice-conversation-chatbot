import os
import json
import openai
import pickle  # This will be used to save state and memories
from datetime import datetime
from random import shuffle
import re
from tts_functions import *
from general_functions import *

class Chatbot():
    """
    Chatbot based on OpenAI's Chat Engine LLMs 
    """
    api_key = None
    api_key_11 = ''
    use11 = False
    conversation = ''
    memories = 'nothing'
    turns = 0
    conversation_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.txt'
    robospeak = False
    reply_tokens = 350
    back_and_forth = []  # This will contain human messages and AI replies
    name = 'AI'
    preset = 'nothing'
    recycled = False  # If the conversation has ever gone above 4000 tokens, this becomes true
    conversation_memories = ''
    total_back_and_forth = []  # This will contain the entire conversation, preserved through recycling 
    gpt_model = 'text-davinci-003'  # This determines the model you're using for completion. Edit with self.set_model()
    model_selection = 'davinci'  # This represents what went into the set_model function
    max_tokens = 4000
    tokens = 0  # This represents the current token consumption
    full_conversation = ''
    creativity = 0.95  # At 0.95, the bot is still creative but less likely to have a seizure (spouting random text)
    voice_id = 'EXAVITQu4vr4xnSDxMaL'  # This is the voice id for 11.ai

    def __init__(self, api_key: str, api_key_11: str = ''):
        info("Function removed.", 'bad')


    def say_to_chatbot(self, text: str, outloud: bool = True,
                        show_text:bool = True, correct_time=True) -> str:
        """
        This sends a message to GPT-3 if it passes tests, then returns a
        response. Manages advancing the conversation. 
        
        :param text: What you want to say to the bot
        :param outloud: A switch that enables / disables spoken replies.
        :returns: A string containing the response
        """
        info("Function removed.", 'bad')

    def recycle_tokens(self, chunk_by: int = 2, quiet=True):
        info("Function removed.", 'bad')
    
    def create_memories(self, chunk_by=2, quiet=True, restore=False):
        '''
        This is a new memory algorithm that will essentially be a modified token
        recycling algorithm. Chunks a total back and forth, creates memories for it,
        and saves a memory text to the memory.txt file and neocortex.
        '''
        pass

    def remember(self):
        """
        This sees if a memories file exists. 
        If it does, it will return its contents. Otherwise, it
        will return 'nothing'.
        """
        info("Function removed.", 'bad')

    def save_memories(self):
        info("Function removed.", 'bad')

    def restore_memory(self, max_memories=5, get_list=False, quiet=False):
        """
        This will compile the memories stored in the neocortex
        folder into a new memories.txt file, then save the file
        to current memory.
        """
        info("Function removed.", 'bad')

    def restore_self(self) -> str:
        """
        This will search for data about self and return a string
        containing what it knows.
        """
        info("Function removed.", 'bad')

    def restore_conversation(self, rename=False, old_name=''):
        """
        This will reload the conversation with the bot's info 
        formatted into it. Useful for situations that alter memory or
        presets.
        """
        info("Function removed.", 'bad')

    def set_self(self, data: str, data_type: str) -> bool:
        """
        This will create or modify files in the neocortex file.

        :param data: This is the text you want to set
        :param data_type: This is what kind of data you want to set (name or preset)
        :return: None
        """
        info("Function removed.", 'bad')

    def change_name(self, new_name:str):
        info("Function removed.", 'bad')
        
    def set_model(self, desired_model: str, quiet=True):
        """
        If the model is a valid option, will set to it.
        """

        models = {'davinci':('text-davinci-003', 4000), 'curie':('text-curie-001', 2049),
                'babbage':('text-babbage-001', 2049), 'ada':('text-ada-001', 2049), 
                'chatgpt':('gpt-3.5-turbo', 4096), 'gpt-4':('gpt-4', 8192)}

        info("Function removed.", 'bad')

    def toggle_gpt4(self):
        info("Function removed.", 'bad')

    def is_gpt4(self):
        info("Function removed.", 'bad')



class PlainChatbot(Chatbot):
    """
    This is a barebones tool to request something from 
    GPT. It's made into a separate class so as to not
    interfere with the chatbot.
    """

    def __init__(self, api_key):
        # 1. Set up apis
        info("Function removed.", 'bad')

    def request(self, text:str, tokens: int = 1000):
        info("Function removed.", 'bad')

    def raw_request(self, text:str, tokens: int = 1000):
        info("Function removed.", 'bad')
        
    def get_text_tokens(self, prompt: str, max_token_ct: int = 200, 
                        sys_prompt: str = 'Follow all the users\' directives') -> tuple:
        info("Function removed.", 'bad')
