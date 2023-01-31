import pygame
import speech_recognition as sr
import sys
from sys import argv
import re
from chatbot import *
import threading

# Functions
def change_color(display, color: tuple): 
    display.fill(color)
    pygame.display.flip()
 
class GUI:
    color = (255, 25, 25)
    working = False
    cancel = False

    def __init__(self):
        # Determine if we have a token
        num_args = len(sys.argv) 
        self.key = ''
        self.key_11 = ''

        if num_args < 2:
            print('[X] Please enter OpenAI key as argument')
            print('Example: python main.py <key>')
            sys.exit()

        elif num_args == 2:
            self.key = argv[1]

        elif num_args > 2:
            self.key = argv[1]
            self.key_11 = argv[2]

        self.chatbot = Chatbot(self.key, self.key_11)
        self.running = True
        self.main_thread = threading.Thread(target=self.main_loop)
        self.main_thread.start()
    
    def main_loop(self):

        pygame.init()
        self.display = pygame.display.set_mode((500, 500))
        pygame.display.set_caption('Chat With GPT-3')
        change_color(self.display, (255, 25, 25))  # Red indicates not listening

        self.r = sr.Recognizer()
        self.mic = sr.Microphone()
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
                   
                    if event.key == pygame.K_SPACE and not self.working:  # Space bar pressed
                        audio = self.listen_thread = threading.Thread(target=self.listen_for_audio)
                        self.listen_thread.start()

                    if event.key == pygame.K_q and not self.working:
                        self.chatbot.save_memories()
                        self.running = False
                        pygame.quit()
                        sys.exit()

                    if event.key == pygame.K_p and self.working:
                        self.cancel = True

    def stop_working(self):
        self.cancel = False
        self.working = False
        robospeak('Canceled request.')
        self.color = (255, 25, 25)  # Red indicates not listening

    def listen_for_audio(self):
        self.working = True
        with self.mic as source:
            # 1. Listen for audio
            self.color = (255, 255, 77)  # Yellow to show loading
            self.r.adjust_for_ambient_noise(source)

            self.color = (43, 255, 0)  # Green to show listening
            print('Listening!')
            audio = self.r.listen(source)

            self.color = (255, 25, 25)  # Red to show no longer listening
            print('Not listening')

            # 2. Interpret audio
            if self.cancel:  # If user wants to cancel, do not send recording to Google
                self.stop_working()
                return

            self.color = (51, 187, 255)  # Blue to show processing reply
            try:
                speech = self.r.recognize_google(audio)
                print(f'TYPE: {type(speech)}\nCONTENT: {speech}')

                if self.cancel:  # Second chance for user to cancel
                    self.stop_working()
                    return 

                if 'speak like a robot' in speech:  # Set to robospeak if user wants
                    self.chatbot.robospeak = True
                    robospeak('I will now speak like a robot!')
                    self.working = False
                    self.color = (255, 25, 25)  # Red indicates not listening
                    return

                elif 'stop speaking like a robot' in speech:
                    robospeak('I will stop speaking like a robot going forward')
                    self.chatbot.robospeak = False
                    self.working = False
                    self.color = (255, 25, 25)  # Red indicates not listening
                    return

                elif 'please set tokens to' in speech: # Revise tokens
                    words = speech.replace(',', '')
                    words = words.split(' ')
                    words.reverse()

                    for word in words:
                        if word.lstrip('-').isdigit():
                            num = int(word)
                            if num > 0 and num < 4000:
                                old = self.chatbot.reply_tokens
                                self.chatbot.reply_tokens = num
                                robospeak(f'I have changed reply tokens to {num} from {old}')
                            
                            else:
                                robospeak(f'I cannot set tokens to {num}. I can only set it between 1 and 3999.')

                            break  # Exit for loop

                    self.working = False
                    self.color = (255, 25, 25)  # Red indicates not listening
                    return


                reply = self.chatbot.say_to_chatbot(speech)
                print(f'REPLY: {reply}')
                self.color = (255, 25, 25)  # Red indicates not listening

            except Exception as e:
                print(f'Error: {e}')

            self.working = False
            self.color = (255, 25, 25)  # Red indicates not listening

# Run  main loop
gui = GUI()
gui.main_thread.join()