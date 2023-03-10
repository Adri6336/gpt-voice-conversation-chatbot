from rich import print as color
import os
 

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