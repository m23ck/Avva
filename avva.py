# Imports
import speech_recognition as sr
import os, datetime, warnings, calendar, random, wikipedia
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
from core import *
# Ignore any Warnings we get
warnings.filterwarnings('ignore')

# Typical analogy of a virtual assistant
# listen for audio
# convert to text
# perform whatever task
# return a text 
# convert the text to audio


def recordAudio():# Capture audio and return text
    # Record
    recognizer= sr.Recognizer() #creating an instance of a recognizer object
    with sr.Microphone() as sourceAudio: # Open the mix and start recording
        print("Say Something..")
        audio_input= recognizer.listen(sourceAudio)
    # Implement Google Speech Recognition
    audio_input_as_text= "" 
    try:
        audio_input_as_text= recognizer.recognize_google(audio_input)
        print("You said: ", audio_input_as_text)
    except sr.UnknownValueError: #if the speechrecognition is unsure of what it was fed
        print("I Couldn't understand you. Please try again!")
    except sr.RequestError as reqError: #if there was a problem getting a response from google speechrecognition
        print("I'm Sorry, there is currently an unforseen problem with getting a response from Google Speech Regnition, Please check your internet connection. The error: ", reqError)
    return(audio_input_as_text)

def respondAsAudio(textCommand): # Respond to the interpreted text
    print(textCommand)
    try:
        #Convert text to speech
        interpreted_audio_output = gTTS(textCommand, lang='en', slow=False) #read text a slower when slow=True
        interpreted_audio_output.save('./tmp/response.mp3') #save the generated audio
        # os.system('start ./tmp/response.mp3') # Play the audio on windows
        play(AudioSegment.from_mp3("./tmp/response.mp3")) # Play the audio
    except:
        print("i could not understand you")
def wakeWord(text):
    text = text.lower() #make the text lowercase
    for phrase in wakeWords:
        if phrase in text:
            return(True)
     
    return(False)

def getDate():
    now = datetime.datetime.now()
    current_date = datetime.datetime.today()
    weekday = calendar.day_name[current_date.weekday()]
    month_as_number = now.month
    day_as_number = now.day
    return("Today is %s %s the %s." % (weekday, months[month_as_number - 1], ordinal_numbers[day_as_number - 1]))

def greeting(text):
    for section in text.split():
        if section.lower() in greeting_inputs:
            return random.choice("%s." % greeting_responses)
    return ''

def gratitude(text):
    grat = ''
    for section in text.split():
        if section.lower() in gratitude_inputs:
            grat = random.choice(gratitude_responses)
            return("%s." % grat)
    return grat

def whois(text):
    sections = text.split()
    for i in range(0, len(sections)):
        if i + 3 <= len(sections) - 1 and sections[i].lower() =="who" and sections[i +1] == "is":
            person = sections[i+2:(len(sections))]

def play(text):
    music_path= ""

while True:
    speech = recordAudio()
    response = ''

    if wakeWord(speech) == True:
        response = "%s %s" % (response, greeting(speech)) #check for greetings
        if 'date' in speech:
            response = "%s %s" % (response, getDate())

        if "who is" in speech:
            person = whois(speech)
            wiki_res = wikipedia.summary(person, sentences= 2)
            response= "%s %s" % (response, wiki_res)
        
        response = "%s %s" % (response, gratitude(speech)) #show gratitude

        respondAsAudio(response)
    else:
        random_passive = random.choice(passive_aggressive_notes)
        respondAsAudio("%s." % random_passive)
    response = "%s %s" % (response, gratitude(speech)) #show gratitude
    
        