from bs4 import BeautifulSoup
from voice_assistant import VoiceAssistant
from get_html import get_search
from translate import Translation



def diki_main(assist):
    last_query = []
    while True:
        voice_txt = assist.voice_process()
        if voice_txt and assist.awake:
            response_html = get_search(voice_txt)
            if response_html:
                soup = BeautifulSoup(response_html, 'html.parser').find('div', class_='diki-results-left-column')
                if soup:
                    last_query.append(Translation(soup))
                    last_query[-1].q = voice_txt
                    last_query[-1].get_translation()
                    assist.awake = False
                    assist.speak("Good luck!")
                    print("sleeping mode... zzz ZZZ")
                    print('Call "Daiki" to wake me up.')
                else:
                    print(f"There is no '{voice_txt}' in the dictionary")



if __name__ == '__main__':
    diki_assist = VoiceAssistant()
    diki_main(diki_assist)
