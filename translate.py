from bs4 import BeautifulSoup



class Translation():
    q = ''
    def __init__(self, soup_main):
        self.soup_all = soup_main.find_all(class_="dictionaryEntity")

        # Add option to choose partOfSpeech (?)
        # self.partOfSpeech = [PoS.text.strip() for PoS in soup_main.find_all('div', 'partOfSpeech')]
        # go through tree step by step adding elements to the dictionary
        # if exists else None (sibling by sibling).

    def get_translation(self):
        for soup in self.soup_all:
            frases_en = soup.find(class_='hws').find_all(class_='hw')
            frase_en = [f_en.text.strip() for f_en in frases_en]
            foreign2native = soup.find_all("ol", class_="foreignToNativeMeanings")

            for frase in frase_en:
                print(*frase.upper(), '\n')
            for f2n in foreign2native:
                m = self.Meanings(f2n)
                # if m.partOfSpeech == PoS: then this is a part of speech that I'm looking for
                for d in m.translate():
                    print('_'*25)
                    print(d['meanings'].ljust(25), end='\t')
                    print(f"( {m.partOfSpeech()} )")
                    print('-'*25)
                    print(*d['examples'])
                print(*m.examplesAdditional())

    #get all if statements
    ##get meanings
    ### get also examples
    ## get additional examples
    #dictEntity.examples() so within examples flag to find only examples etc...

    class Meanings():

        def __init__(self, foreign2native):
            self.f2n = foreign2native


        def translate(self):

            def get_examplesMain(meaning):
                examples = meaning.find_all(class_='exampleSentence')
                new_line = '\n'
                return [ f'{ex.get_text(new_line, strip=True)}\n\n' for ex in examples ] # add if flag else None

            def get_meanings(tag):
                return ', '.join([hw.text.strip() for hw in tag.find_all(class_='hw')])

            return [{ 'meanings': get_meanings(meaning), 'examples': get_examplesMain(meaning) }
                for meaning in self.f2n.select("[id*='meaning']") ]


        def partOfSpeech(self):
            prevsib = self.f2n.find_previous_sibling(lambda prev: prev.name != None
                                                    and prev['class'] != ['vf'])

            return prevsib.text.strip() if prevsib and prevsib['class'][0] == 'partOfSpeechSectionHeader' else None


        def examplesAdditional(self):
            sibling = self.f2n.find_next_sibling(lambda sib: sib.name != None)
            if sibling and sibling['class'][0] == 'additionalSentences':
                p_en = sibling.find("div", "hiddenAdditionalSentences").find_all('p', {'lang': 'en'})
                return [f">> {p.text.strip()}\n" for p in p_en]
            else:
                return ''


        def __repr__(self):
            return str(
                dict({
                    'Part of speech': self.partOfSpeech(),
                    'Meanings': self.translate(),
                    'Additional examples': self.examplesAdditional()
                })
            )
