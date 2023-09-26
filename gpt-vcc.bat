@echo off

python -c "import sys; print(sys.version)" 
IF %ERRORLEVEL% NEQ 0 (
    echo Install Python First
    pause
    explorer https://www.python.org/
    exit
)

type .gvi
IF %ERRORLEVEL% NEQ 0 (
    echo Installing....
    pip install playsound==1.2.2
    pip install gTTS==2.3.1
    pip install SpeechRecognition==3.10.0
    pip install pygame
    pip install pyaudio==0.2.13
    pip install gTTS==2.3.1
    pip install nltk==3.8.1
    pip install requests>=2.31.0
    pip install openai
    pip install langdetect==1.0.9
    pip install pyttsx3==2.90
    pip install rich
    pip install numpy
    pip install elevenlabs
    echo > .gvi
    clear
    echo Pip Installation Attempted
)

WHERE wt
IF %ERRORLEVEL% EQU 0 wt -p "Command Prompt" -d "%cd%" cmd /k python main.py

WHERE wt
IF %ERRORLEVEL% EQU 1 (
    clear
    echo GPT-VCC Looks Best With Windows Terminal
    python main.py
)