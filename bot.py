import openai
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import random
import geocoder

# Set up OpenAI API credentials
openai.api_key = "YOUR_OPENAI_API"

listener = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 200)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.say('Hi, I am ONE, your personal chatbot. How can I help you today?')
engine.runAndWait()


def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    try:
        with sr.Microphone() as source:
            print('Listening...')
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            print(command)
    except sr.UnknownValueError:
        print('Sorry, I did not understand that.')
        command = ''
    except sr.RequestError as e:
        print('Sorry, my speech service is down.')
        command = ''
    return command


def get_location():
    g = geocoder.ip('me')
    lat, lng = g.latlng
    return lat, lng


def get_openai_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()


def handle_sadness():
    responses = ["I'm sorry to hear that. Would you like to talk about it?",
                 "That sounds tough. Is there anything I can do to help?",
                 "I'm here for you. Please tell me how you're feeling.",
                 "I understand. Please take care of yourself."]

    return random.choice(responses)


def run_alexa():
    while True:
        command = take_command()
        if 'thanks' in command or 'thank you' in command:
            talk('You are welcome!')
            break
        elif 'play' in command:
            song = command.replace('play', '')
            talk('Playing ' + song)
            pywhatkit.playonyt(song)
        elif 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            talk('The current time is ' + time)
        elif 'location' in command:
            talk('Your current location is')
            response = get_location()
            print(response)
            talk(response)
        elif 'sad' in command or 'depressed' in command or 'down' in command:
            talk(handle_sadness())
        elif 'happy' in command:
            talk("That's great!")
        elif 'stressed' in command or 'tired' in command or 'angry' in command:
            talk('Would you like a mood swinger?')
            talk('Click on the links below and feel refreshed!')
            print('http://www.pixelthoughts.co/')
            print('http://weavesilk.com/')
            print('https://www.rainymood.com/')
            print('http://incredibox.com/')
        else:
            response = get_openai_response(command)
            print(response)
            talk(response)
run_alexa()
