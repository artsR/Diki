import os
import playsound, time
import speech_recognition as sr
from gtts import gTTS



class VoiceAssistant():
    awake = False
    speak_tmp = 1

    def __init__(self):
        self.r = sr.Recognizer()
        self.r.energy_threshold = 350
        self.r.dynamic_energy_threshold = False
        self.r.phrase_threshold = 0.2
        self.start_up = ['diki', 'daiky', 'daiki', 'dicky', 'dickey', 'dickay']
        self.speak("Daiki is ready to use. I'm in listening mode.")
        print('Call "Daiki" to wake me up.')

    def voice_process(self):
        """Listen to sounds from microphone and return audio as text."""
        voice_txt = ''

        with sr.Microphone() as source:
            try:
                audio = self.r.listen(source, phrase_time_limit=10)
                try:
                    voice_txt = self.r.recognize_google(audio)
                    print(f"You said: {voice_txt}")

                    if self.awake:
                        print("...Request processing...\n\n")
                        return voice_txt.lower()
                    elif voice_txt.lower() in self.start_up:
                        self.speak("Hello, sir. What do you need?")
                        print("M E N U:".center(25))
                        print("<copy> - to copy highlighted english word")
                        print("<word to translate>")
                        self.awake = True
                        return None
                    else:
                        return False
                except sr.UnknownValueError:
                    pass
                    return False
                except sr.RequestError as e:
                    print(f"Uh oh! Couldn't request results from Google Speech Recognition service; {e}")
                    return False
            except Exception:
                print('Exception of r.listen')
                return False

    @classmethod
    def speak(cls, text):
        tts = gTTS(text=text, lang='en')
        filename = 'speak_' + str(cls.speak_tmp) + '.mp3'
        cls.speak_tmp += 1
        tts.save(filename)
        playsound.playsound(filename)
        os.remove(filename)
