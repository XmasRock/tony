import pyttsx3

engine = pyttsx3.init()
engine.setProperty('voice', 'french')
engine.say("Bonjour, le système vocal est prêt.")
engine.runAndWait()
