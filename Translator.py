from speak import Say
from fnmatch import translate
from time import sleep
import googletrans #pip install googletrans
from gtts import gTTS
import googletrans
import googletrans
from googletrans import Translator
from listen import Listen

def translate_word(word, target_language):
    translator = Translator(service_urls=['translate.google.com'])
    translation = translator.translate(word, dest=target_language)
    return translation.text

def translategl():
    Say("What is the word that you want to translate sir? ")
    word=Listen()
    print(googletrans.LANGUAGES)
    Say("Sir please enter the target language code (e.g., 'fr' for French): ")
    target_language = Listen()
    print("Translating....")
    translated_word = translate_word(word, target_language)
    Say(f"Translation: {translated_word}")