# importing pygame module
import pygame
import speech_recognition as sr
import sys
from sys import argv
import re
from chatbot import *


# Functions
def change_color(display, color: tuple): 
    display.fill(color)
    pygame.display.flip()
 
# Determine if we have a token
if len(sys.argv) < 2:
    print('[X] Please enter OpenAI key as argument')
    print('Example: chat.py <key>')
    sys.exit()
else:
    key = argv[1]

# Setup pygame display
pygame.init()
display = pygame.display.set_mode((500, 500))
pygame.display.set_caption('Chat With GPT-3')

# Setup recorder
r = sr.Recognizer()
mic = sr.Microphone()

# Setup chatbot
chatbot = Chatbot(key, '')
 
# Run  main loop
while True:
    change_color(display, (255, 25, 25))  # Red indicates not listening

    # Creating a loop to check events that
    # are occurring
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
         
        # Checking if keydown event happened or not
        if event.type == pygame.KEYDOWN:
           
            if event.key == pygame.K_SPACE:  # Space bar pressed
                with mic as source:
                    # 1. Listen for audio
                    change_color(display, (255, 255, 77))  # Yellow to show loading
                    r.adjust_for_ambient_noise(source)

                    change_color(display, (43, 255, 0))  # Green to show listening
                    print('Listening!')
                    audio = r.listen(source)

                    change_color(display, (255, 25, 25))  # Red to show no longer listening
                    print('Not listening')

                    # 2. Interpret audio
                    try:
                        speech = r.recognize_google(audio)
                        print(f'TYPE: {type(speech)}\nCONTENT: {speech}') 

                        change_color(display, (51, 187, 255))  # Blue to show processing reply
                        reply = chatbot.say_to_chatbot(speech)
                        print(f'REPLY: f{reply}')

                    except Exception as e:
                        print(f'Error: {e}')

            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit() 
