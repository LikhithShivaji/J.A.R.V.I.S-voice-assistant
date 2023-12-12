import wolframalpha
import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)
r=sr.Recognizer()

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def WolfRamAlpha(query):
    apikey="449A97-G5HJ95UEG3"
    requester= wolframalpha.Client(apikey)
    requested=requester.query(query)
    try:
        answer=next(requested.results).text
        return answer
    except:
        speak("The value is not answerable")

def Calc(query):
    Term=str(query)
    Term=Term.replace("jarvis","")
    Term=Term.replace("plus","+")
    Term=Term.replace("minus","-")
    Term=Term.replace("factorial","!")
    Term=Term.replace("multiplied by","*")
    Term=Term.replace("divided by","/")

    Final = str(Term)
    try:
        result = WolfRamAlpha(Final)
        print(f"{result}")
        speak(result)
    
    except:
        speak("The value is not answerable")
