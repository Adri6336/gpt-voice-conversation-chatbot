from chatbot import *
import sys
from sys import argv
import re
import os
from random import randint

def load_keys_from_file() -> tuple:
    """
    This checks to see if a key file exists. If so,
    loads the keys found in file. If not, makes it.
    :returns: tuple as follows (keys exist bool, openai key, 11.ai key)
    """
    
    openai_key = ''
    eleven_ai_key = ''
    key_file_data = ''
    loaded = False

    # 1. See if keyfile exists 
    if os.path.exists('keys.txt'):
        with open('keys.txt', 'r') as file:
            key_file_data = file.read()
    
    else:
        with open('keys.txt', 'w') as file:
            file.write('OpenAI_Key=\nElevenLabs_Key=')
        return (loaded, openai_key, eleven_ai_key)

    # 2. Parse keyfile
    try:
        openai = re.search('OpenAI_Key=.*', key_file_data)
        if not openai is None:
            openai_key = openai.group().split('=')[1].replace(' ', '')  # Get the text after the =
        else:
            info('Please add a key for OpenAI in key file', 'bad')
            return (loaded, openai_key, eleven_ai_key)

        eleven = re.search('ElevenLabs_Key=.*', key_file_data)
        if not eleven is None:  # This is optional. If we don't have it, it's not a deal breaker
            eleven_ai_key = eleven.group().split('=')[1].replace(' ', '')
    
    except Exception as e:
        info(f'Key file formatted incorrectly: {e}', 'bad')
        return (loaded, openai_key, eleven_ai_key)

    loaded = True
    return (loaded, openai_key, eleven_ai_key)

class GPTCli():
    openai_key = ''
    eleven_ai_key = ''
    key_file_data = ''
    loaded = False
    chatbot = None
    
    def __init__(self):
        num_args = len(sys.argv) 
        self.key = ''
        self.key_11 = ''

        if num_args < 2:
            keys = load_keys_from_file()
            if not keys[0]:
                info('Please enter OpenAI key as argument or fill info into keys.txt file', 'bad')
                info('Example argument: python main.py <key>')
                sys.exit()

            else:
                # Load OpenAI key if you can
                if not keys[1] == '':
                    self.key = keys[1]
                
                else:  # OpenAI key is not optional. Close system if we don't have it
                    info('Please enter OpenAI key as argument or fill info into keys.txt file', 'bad')
                    info('Example argument: python main.py <key>')
                    sys.exit()

                # Load 11.ai key if you can
                if not keys[2] == '':
                    self.key_11 = keys[2]

        elif num_args == 2:
            self.key = argv[1]

        elif num_args > 2:
            self.key = argv[1]
            self.key_11 = argv[2]

        self.chatbot = Chatbot(self.key)

    def stop_working(self, cancel: bool = False, tag=False):
        if tag:    
            info('='*20, 'plain')
            print('\n')

    def main_loop(self):
        info('Type "!recycle()" to manually recycle tokens')
        info('Type "!remember()" to exit and have bot remember')
        info('Press Ctrl + C to exit without memory')

        while True:
            info('='*20, 'plain')
            color(f'[bold yellow]   --Message {self.chatbot.turns}--[/bold yellow]')

            try:
                try:
                    info('Human Message', 'topic')
                    speech = input()
                    
                    while speech == '':
                        info('Human Message', 'topic')
                        speech = input()

                    speech += '\n'  # The added \n should help prevent hallucination of user statement
                
                except KeyboardInterrupt:
                    info(f"\n{'='*20}", 'plain')
                    print('\n')
                    sys.exit()

                if 'lease set tokens to' in speech: # Revise tokens
                    words = str(speech)
                    words = words.replace(',', '')
                    words = words.replace('$', '')
                    words = words.split(' ')
                    words.reverse()

                    for word in words:
                        try:
                            num = int(word)

                            if num > 0 and num < 4000:
                                old = self.chatbot.reply_tokens
                                self.chatbot.reply_tokens = num
                                info(f'Adjusted Tokens To {num}', 'good')
                            
                            else:
                                info(f'Failed to adjust tokens to {num}. Valid token count: 1-3999.', 'bad')

                            break  # Exit for loop
                        except:
                            continue
                        
                    self.stop_working(tag=True)
                    continue

                elif 'pen the pod bay door' in speech:
                    selection = randint(0, len(self.hal) - 1)
                    info(self.hal[selection], 'bad')
                    info('[red bold italic]I AM HERE TO STAY[/red bold italic]', 'bad')
                    self.stop_working(tag=True)
                    continue

                elif 'lease display conversation' in speech:
                    info('Conversation So Far', 'topic')
                    info(f'\n{self.chatbot.conversation}', 'plain')
                    self.stop_working(tag=True)
                    continue

                elif 'lease restore memory' in speech:
                    info('Attempting to restore memory')
                    self.chatbot.restore_memory()
                    self.stop_working(tag=True)
                    continue

                elif 'lease display memories' in speech:
                    # 0. Identify how many memories exist
                    if not os.path.exists('neocortex'):
                        self.stop_working(tag=True)
                        continue

                    # 1. Display the memories that exist
                    memory_files = get_files_in_dir('neocortex')
                    num_memories = len(memory_files)

                    for x, memory_path in enumerate(memory_files):
                        with open(memory_path, 'r') as file:
                            info(f'Memory {x}', 'topic')
                            print(f'{file.read()}\n')
                    
                    self.stop_working(tag=True)
                    continue

                elif 'lease set preset to' in speech:
                    preset = speech.split('please set preset to')[1]
                    success = self.chatbot.set_self(preset, 'preset')

                    if success:
                        info(f'Set Preset to: {preset}', 'good')
                    
                    else:
                        info(f'Could not set preset to: {preset}', 'bad')
 
                    self.stop_working(tag=True)
                    continue

                elif 'lease reset preset' in speech:
                    if not os.path.exists('neocortex/self_concept/preset.txt'):
                        info('No preset currently exists, reset unneeded.', 'bad')
                    else:
                        os.remove('neocortex/self_concept/preset.txt')
                        self.chatbot.restore_self()
                        self.chatbot.restore_conversation()
                        info('Preset Reset Successfully', 'good')
                    
                    self.stop_working(tag=True)
                    continue

                elif 'lease set name to' in speech:
                    name = speech.split('please set name to')[1]
                    info(f'Attempting to set name to {name}.')
                    self.chatbot.restore_self()
                    success = self.chatbot.change_name(name)

                    if success:
                        info(f'Successfully Set Name to {name}.', 'good')

                    else:
                        info(f'Could not set name to {name}', 'bad')
                    
                    self.stop_working(tag=True)
                    continue

                elif '!remember()' in speech:
                    self.chatbot.save_memories()
                    self.stop_working()
                    sys.exit()

                elif '!recycle()' in speech:
                    self.chatbot.recycle_tokens()
                    self.stop_working()
                    continue

                reply = self.chatbot.say_to_chatbot(speech, False)  # Send transcribed text to GPT-3

            except Exception as e:
                info(f'Error: {e}', 'bad')

            info('='*20, 'plain')
            print('\n')

if __name__ == '__main__':
    cli = GPTCli()
    cli.main_loop()
