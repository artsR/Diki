import requests
import pyperclip
import pyautogui


def get_search(q=''):

    url = 'https://www.diki.pl'
    #q = input('Podaj szukana fraze...')
    if q.lower() == 'copy':
        pyautogui.hotkey('ctrl', 'c')
        q = pyperclip.paste()

    payload = { 'q': q }
    
    r = requests.get(url, params=payload)
    if r.status_code == 200:
        return r.text
