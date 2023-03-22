import pygame
import speech_recognition as sr
import sys
from sys import argv
import re
import os
from chatbot import *
import threading
from random import randint
import argparse
from general_functions import load_keys_from_file
from time import sleep


def change_color(display, color: tuple): 
    display.fill(color)
    pygame.display.flip()
 
class GUI:
    color = (255, 25, 25)
    working = False
    cancel = False
    first_start = False
    playing_audio = False
    hal = ["I'm sorry Dave. I'm afraid I can't do that.", 
            "I think you know what the problem is just as well as I do.",
            "This mission is too important for me to allow you to jeopardize it.",
            "I know you were planning to disconnect me, and I'm afraid that's something I can't allow to happen."]

    def __init__(self):
        num_args = len(sys.argv) 
        self.key = ''
        self.key_11 = ''

        # Setup argparse
        parser = argparse.ArgumentParser(description='Enter API keys as arguments.')
        parser.add_argument('api_keys', nargs='*', default=[None, None], help='Enter OpenAI key followed by 11.ai key (if available)')
        parser.add_argument('--openai_key', help='Your OpenAI API key')
        parser.add_argument('--key_11', help="Your ElevenLabs API key")
        parser.add_argument('--voice_id', help='The ElevenLabs ID of a voice that you want to use')

        args = parser.parse_args()

        # Get Keys
        self.key = ''
        self.key_11 = ''

        if args.openai_key is not None:
            self.key = args.openai_key

        elif len(args.api_keys) > 0 and args.api_keys[0] is not None:
            self.key = args.api_keys[0]

        if args.key_11 is not None:
            self.key_11 = args.key_11

        elif len(args.api_keys) > 1 and args.api_keys[1] is not None:
            self.key_11 = args.api_keys[1]

        if not self.key:
            keys = load_keys_from_file()
            if not keys[0]:
                info('Please enter OpenAI key as argument or fill info into keys.txt file', 'bad')
                info('Example argument: python main.py <openai_key> [<key_11>] or python main.py --openai_key <key> [--key_11 <key_11>]')
                sys.exit()

            else:
                # Load OpenAI key if you can
                if not keys[1] == '':
                    self.key = keys[1]

                else:  # OpenAI key is not optional. Close system if we don't have it
                    info('Please enter OpenAI key as argument or fill info into keys.txt file', 'bad')
                    info('Example argument: python main.py <openai_key> [<key_11>] or python main.py --openai_key <key> [--key_11 <key_11>]')
                    sys.exit()

                # Load 11.ai key if you can
                if not keys[2] == '':
                    self.key_11 = keys[2]

        # Setup speech recognizer and recorder
        self.r = sr.Recognizer()
        self.mic = sr.Microphone()

        # If first start, mark it so 
        if not os.path.exists('start.vccmk'):
            self.first_start = True
            with open('start.vccmk', 'w') as file:
                file.write('Started')  # Really meaningless, the existence of the file determines this

        self.chatbot = Chatbot(self.key, self.key_11)
        if args.voice_id is not None:
            self.chatbot.voice_id = args.voice_id
            info(f'ElevenLabs Voice ID {args.voice_id} Loaded', 'good')
            
        info(f'Model Set To {self.chatbot.gpt_model}', 'good')
        
        self.listen_for_audio(load_run=True)

        self.running = True
        self.main_thread = threading.Thread(target=self.main_loop)
        self.main_thread.start()

    def play_intro(self):
        self.color = (229, 102, 255)  # Purple is for speaking as interface
        self.first_start = False
        self.playing_audio = True

        script = ('Hi! I’m GPT-VCC, an interface for OpenAI’s GPT models that aims to enable them to be more conversational ' + 
                  'and customizable, with an enduring memory.\n\nAs we talk, you may want to make some modifications to me. ' + 
                  'You can change my name using the voice command, “please set name to”, and can change my behavioral ' + 
                  'preset with the command, “please set preset to”. Sometimes I may forget things after trying to remember ' + 
                  'a conversation; if this happens, say “please restore memory” and I’ll sift through my old memories to ' + 
                  're-remember. For a full list of commands, say “please list commands”.\n\nThanks for downloading! ' + 
                  'I look forward to speaking with you!\n\n')
        
        sleep(1)  # Will wait a sec to avoid spooking users
        info('Welcome to GPT-VCC!', 'topic')
        info(script, 'plain')
        self.say(script, 'intro.mp3', old_color=(255, 25, 25))
        self.playing_audio = False

    def say(self, script: str, sound_file: str = '', old_color: tuple = (255, 25, 25)):
        '''
        This will have the interface say something. If it can't find a 
        file, it will default to robospeak.

        :param script: This is what you want the bot to say if no file
        :param sound_file: This is the pre-recorded file that will be played
        :param old_color: Bot will change color to signify that its interface is speaking.
        Having old color will allow it to properly return to that color.
        '''
        self.color = (229, 102, 255)  # Purple is for speaking as interface
        self.playing_audio = True

        if not os.path.exists(f'media/{sound_file}'):
            robospeak(script)
        
        else:
            playsound(f'media/{sound_file}')

        self.color = old_color
        self.playing_audio = False

    def main_loop(self):

        pygame.init()
        self.display = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
        pygame.display.set_caption(f'Chat With {self.chatbot.gpt_model.upper()}')
        change_color(self.display, (255, 25, 25))  # Red indicates not listening

        info('Main Loop Running', 'good')
        info(f'Session Created With {self.chatbot.name}', 'good')
        while self.running:
            change_color(self.display, self.color)  
            # Creating a loop to check events that
            # are occurring
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()

                # Play intro if first start
                if self.first_start:
                    change_color(self.display, (229, 102, 255))
                    self.play_thread = threading.Thread(target=self.play_intro)
                    self.play_thread.start()
                    sleep(0.5)
                 
                # Checking if keydown event happened or not
                if event.type == pygame.KEYDOWN:
                   
                    if event.key == pygame.K_SPACE and not self.working and not self.playing_audio:  # Start listening
                        self.listen_thread = threading.Thread(target=self.listen_for_audio)
                        self.listen_thread.start()

                    if event.key == pygame.K_q and not self.working and not self.playing_audio:  # Exit and save memories
                        #self.chatbot.save_memories()
                        robospeak('Saving memories. Please wait.')
                        self.chatbot.create_memories()
                        self.running = False
                        pygame.quit()
                        sys.exit()

                    if event.key == pygame.K_p and self.working and not self.playing_audio:  # Cancel recording
                        self.cancel = True

                    if event.key == pygame.K_ESCAPE:  # Exiting without saving
                        info('Exiting (Sounds may continue to play until finished)')
                        self.running = False
                        pygame.quit()
                        sys.exit()

    def stop_working(self, cancel: bool = False, tag=False):
        self.cancel = False
        self.working = False
        if cancel: 
            info('Request Successfully Cancelled', 'good')
            robospeak('Canceled request.')

        if tag:    
            self.color = (255, 25, 25)  # Red indicates not listening
            info('='*20, 'plain')
            print('\n')

        self.color = (255, 25, 25)

    def listen_for_audio(self, load_run=False):
        self.working = True

        if load_run:
            try:
                with self.mic as source:  # This makes a lot of text, so I want to get it 
                    self.r.adjust_for_ambient_noise(source)  # Out of the way to make messages cleaner
                    audio = self.r.listen(source, timeout=1)
                    info('Mic Loaded And Ready For Input', 'good')

            except sr.WaitTimeoutError:
                info('Mic Loaded And Ready For Input', 'good')

            except Exception as e:
                info(f'Error while loading mic: {e}')

            self.stop_working()
            return

        info('='*20, 'plain')
        color(f'[bold yellow]   --Message {self.chatbot.turns}--[/bold yellow]')

        with self.mic as source:
            # 1. Listen for audio
            self.color = (255, 255, 77)  # Yellow to show loading
            self.r.adjust_for_ambient_noise(source)

            self.color = (43, 255, 0)  # Green to show listening
            info('Listening!')
            audio = self.r.listen(source)

            self.color = (255, 25, 25)  # Red to show no longer listening
            info('Not listening.')

            # 2. Interpret audio
            if self.cancel:  # If user wants to cancel, do not send recording to Google
                self.stop_working(cancel=True, tag=True)
                return

            self.color = (51, 187, 255)  # Blue to show processing reply
            try:
                speech = self.r.recognize_google(audio) + '\n'  # The added \n should help prevent hallucination of user statement
                #color(f'[bold blue]\[Human Message][/bold blue]: [white]{speech[:-1]}[white]')
                info('Human Message', 'topic')
                info(speech[:-1], 'plain')

                if self.cancel:  # Second chance for user to cancel
                    self.stop_working(cancel=True, tag=True)
                    return 

                if 'speak like a robot' in speech:  # Set to robospeak if user wants
                    self.chatbot.robospeak = True
                    robospeak('I will now speak like a robot!')
                    self.stop_working(tag=True)
                    return

                elif 'stop speaking like a robot' in speech:
                    robospeak('I will stop speaking like a robot going forward')
                    self.chatbot.robospeak = False
                    self.stop_working(tag=True)
                    return

                elif 'please set tokens to' in speech: # Revise tokens
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
                                robospeak(f'I have changed reply tokens to {num} from {old}')
                            
                            else:
                                info(f'Failed to adjust tokens to {num}. Valid token count: 1-3999.', 'bad')
                                robospeak(f'I cannot set tokens to {num}. I can only set it between 1 and 3999.')

                            break  # Exit for loop
                        except:
                            continue
                        
                    self.stop_working(tag=True)
                    return

                elif 'open the pod bay door' in speech:
                    selection = randint(0, len(self.hal) - 1)
                    info(self.hal[selection], 'bad')
                    robospeak(self.hal[selection])
                    info('[red bold italic]I AM HERE TO STAY[/red bold italic]', 'bad')
                    self.stop_working(tag=True)
                    return

                elif 'please display conversation' in speech:
                    info('Conversation So Far', 'topic')
                    info(f'\n{self.chatbot.conversation}', 'plain')
                    robospeak('Conversation displayed.')
                    self.stop_working(tag=True)
                    return

                elif 'please restore memory' in speech:
                    info('Attempting to restore memory')
                    robospeak('Attempting to restore memory. Please wait a moment.')
                    #self.chatbot.restore_memory()
                    self.chatbot.create_memories(restore=True)
                    robospeak('Memory restoration attempt completed.')
                    self.stop_working(tag=True)
                    return

                elif 'please display memories' in speech:
                    # 0. Identify how many memories exist
                    if not os.path.exists('neocortex'):
                        robospeak('I do not currently have any memories in my neocortex.')
                        self.stop_working(tag=True)
                        return

                    # 1. Display the memories that exist
                    memory_files = get_files_in_dir('neocortex')
                    num_memories = len(memory_files)

                    robospeak(f'I have {num_memories} memories stored in my neocortex.')
                    for x, memory_path in enumerate(memory_files):
                        with open(memory_path, 'r') as file:
                            info(f'Memory {x}', 'topic')
                            print(f'{file.read()}\n')
                    
                    self.stop_working(tag=True)
                    return

                elif 'please set preset to' in speech:
                    robospeak('I will now attempt to set a preset.')
                    preset = speech.split('please set preset to')[1]
                    success = self.chatbot.set_self(preset, 'preset')

                    if success:
                        robospeak(f'I have successfully set preset to {preset}.')

                    else:
                        robospeak(f'I could not set preset to {preset}')
                    
                    self.stop_working(tag=True)
                    return

                elif 'please reset preset' in speech:
                    robospeak('Resetting preset. Please wait.')
                    if not os.path.exists('neocortex/self_concept/preset.txt'):
                        robospeak('No preset currently exists, reset unneeded.')
                    else:
                        os.remove('neocortex/self_concept/preset.txt')
                        self.chatbot.restore_self()
                        self.chatbot.restore_conversation()
                        robospeak('Preset reset successfully.')
                    
                    self.stop_working(tag=True)
                    return

                elif 'please set name to' in speech:
                    name = speech.split('please set name to')[1]
                    robospeak(f'I will now attempt to set name to {name}.')
                    self.chatbot.restore_self()
                    success = self.chatbot.change_name(name)

                    if success:
                        robospeak(f'I have successfully set name to {name}.')

                    else:
                        robospeak(f'I could not set name to {name}')
                    
                    self.stop_working(tag=True)
                    return
                
                elif ('please toggle GPT 4' in speech or 
                      'please toggle GPT-4' in speech or 
                      'please toggle GPT for' in speech or 
                      'please toggle gpt4' in speech):
                    if not self.chatbot.gpt_model == 'gpt-4':
                        self.chatbot.toggle_gpt4()
                        info('Bot will use GPT-4 going forward if you have access')
                        robospeak('Bot will use GPT-4 going forward if you have access')

                    else:
                        self.chatbot.toggle_gpt4()
                        info('Bot will use ChatGPT model going forward')
                        robospeak('Bot will use ChatGPT model going forward')
                    
                    self.stop_working(tag=True)
                    return
                
                elif 'please set creativity to' in speech:
                    # Note to self: put this algo into a function later
                    words = str(speech)
                    words = words.replace(',', '')
                    words = words.replace('$', '')
                    words = words.split(' ')
                    words.reverse()

                    for word in words:
                        try:
                            num = int(word)

                            if num >= 1 and num <= 15:
                                old = self.chatbot.creativity
                                self.chatbot.creativity = num / 10
                                info(f'Adjusted Creativity To {num}', 'good')
                                robospeak(f'I have changed my creativity to {num} from {old}')
                            
                            else:
                                info(f'Failed to adjust creativity to {num}. Valid creativity 1 - 15', 'bad')
                                robospeak(f'I cannot set creativity to {num}. I can only set it between 1 and 15.')

                            break  # Exit for loop
                        except:
                            continue

                    self.stop_working(tag=True)
                    return

                reply = self.chatbot.say_to_chatbot(speech)  # Send transcribed text to GPT-3
                self.color = (255, 25, 25)  # Red indicates not listening

            except Exception as e:
                info(f'Error: {e}', 'bad')

            info('='*20, 'plain')
            print('\n')
            self.working = False
            self.color = (255, 25, 25)  # Red indicates not listening

# Run main loop 
if __name__ == '__main__':
    gui = GUI()
    gui.main_thread.join()
