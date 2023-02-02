import pygame
import speech_recognition as sr
import sys
from sys import argv
import re
from chatbot import *
import threading
from random import randint


def change_color(display, color: tuple): 
    display.fill(color)
    pygame.display.flip()
 
class GUI:
    color = (255, 25, 25)
    working = False
    cancel = False
    hal = ["I'm sorry Dave. I'm afraid I can't do that.", 
            "I think you know what the problem is just as well as I do.",
            "This mission is too important for me to allow you to jeopardize it.",
            "I know you were planning to disconnect me, and I'm afraid that's something I can't allow to happen."]

    def __init__(self):
        # Determine if we have a token
        num_args = len(sys.argv) 
        self.key = ''
        self.key_11 = ''

        if num_args < 2:
            info('Please enter OpenAI key as argument', 'bad')
            info('Example: python main.py <key>')
            sys.exit()

        elif num_args == 2:
            self.key = argv[1]

        elif num_args > 2:
            self.key = argv[1]
            self.key_11 = argv[2]

        # Setup speech recognizer and recorder
        self.r = sr.Recognizer()
        self.mic = sr.Microphone()

        self.chatbot = Chatbot(self.key, self.key_11)

        self.listen_for_audio(load_run=True)

        self.running = True
        self.main_thread = threading.Thread(target=self.main_loop)
        self.main_thread.start()
    
    def main_loop(self):

        pygame.init()
        self.display = pygame.display.set_mode((500, 500))
        pygame.display.set_caption('Chat With GPT-3')
        change_color(self.display, (255, 25, 25))  # Red indicates not listening

        info('Main Loop Running', 'good')
        while self.running:
            change_color(self.display, self.color)  
            # Creating a loop to check events that
            # are occurring
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                 
                # Checking if keydown event happened or not
                if event.type == pygame.KEYDOWN:
                   
                    if event.key == pygame.K_SPACE and not self.working:  # Start listening
                        self.listen_thread = threading.Thread(target=self.listen_for_audio)
                        self.listen_thread.start()

                    if event.key == pygame.K_q and not self.working:  # Exit and save memories
                        self.chatbot.save_memories()
                        self.running = False
                        pygame.quit()
                        sys.exit()

                    if event.key == pygame.K_p and self.working:  # Cancel recording
                        self.cancel = True

                    if event.key == pygame.K_ESCAPE:  # Exiting without saving
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

    def listen_for_audio(self, load_run=False):
        self.working = True

        if load_run:
            try:
                with self.mic as source:  # This makes a lot of text, so I want to get it 
                    self.r.adjust_for_ambient_noise(source)  # Out of the way to make messages cleaner
                    audio = self.r.listen(source, timeout=1)

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

                reply = self.chatbot.say_to_chatbot(speech)  # Send transcribed text to GPT-3
                self.color = (255, 25, 25)  # Red indicates not listening

            except Exception as e:
                info(f'Error: {e}', 'bad')

            info('='*20, 'plain')
            print('\n')
            self.working = False
            self.color = (255, 25, 25)  # Red indicates not listening

# Run  main loop
gui = GUI()
gui.main_thread.join()
