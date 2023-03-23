from rich import print as color
import os
import re

def declares_self_ai(text) -> bool:
    pattern = r'As an AI'
    match = re.search(pattern, text, re.IGNORECASE)
    return bool(match)

def replace_time(original, time):
    result = re.sub(r'\d+:\d+ [A, P]M', time, original)
    return result

def replace_od(text):
    return re.sub(r'\bod\b', 'Good', text, flags=re.IGNORECASE)
 
def convert_to_12hr(hour_24, minutes):
    '''
    Converts 24 hour time into a nicely formatted 12 hour timestamp
    '''
    if minutes < 10:
        minutes = f'0{minutes}'

    if hour_24 == 0:
        return '12:' + str(minutes) + ' AM'
    elif hour_24 < 12:
        return str(hour_24) + ':' + str(minutes) + ' AM'
    elif hour_24 == 12:
        return '12:' + str(minutes) + ' PM'
    else:
        return str(hour_24 - 12) + ':' + str(minutes) + ' PM'

def chunk_list(list1, chunk_by: int):
    """
    Creates a new list (list2) that is composed of all the elements
    of list1, chunked by chunk_by for as long as it can.
    """
    list2 = []
    while list1:
        if len(list1) >= chunk_by:
            list2.append(list1[:chunk_by])
            list1 = list1[chunk_by:]

        else:
            list2.append(list1)
            list1 = []

    return list2

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