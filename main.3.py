import pyttsx3  # Text-to-Speech
import speech_recognition as sr  # Speech Recognition
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import pywhatkit as kit
import pyjokes
import requests
import pyautogui
import pyperclip
from googlesearch import search
from googletrans import Translator
import secrets
import string
import psutil
import openai
import random

# Initialize speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# OpenAI API Key (Replace with your own)
openai.api_key = "AIzaSyDbKSglWmhlUm71xaQAbFzjV0tyKk47i4g"

def speak(audio):
    """Convert text to speech"""
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    """Greet the user based on time"""
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    speak("Hello, I am Jarvis. How can I assist you?")

def takeCommand():
    """Take voice input from the user and convert it to text"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)  # Reduce background noise
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        return query.lower()
    except Exception:
        print("Could not understand, please say that again.")
        return "None"

def sendEmail(to, content):
    """Send an email (Replace with your credentials)"""
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('your_email@gmail.com', 'your_password')
    server.sendmail('your_email@gmail.com', to, content)
    server.close()

def get_news():
    """Fetch top news headlines"""
    url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=YOUR_NEWSAPI_KEY"
    response = requests.get(url).json()
    articles = response["articles"][:3]  # Get top 3 news
    headlines = [f"News {i+1}: {news['title']}" for i, news in enumerate(articles)]
    return " ".join(headlines)

def get_weather(city):
    """Get weather details for a city"""
    api_key = "577b5e171b8877340b40a98ca67b61ae"
    url = f"https://api.openweathermap.org/data/2.5/weather?lat=44.34&lon=10.99&appid={api_key}&units=metric"
    response = requests.get(url).json()
    if "current" in response:
        condition = response["current"]["condition"]["text"]
        temp = response["current"]["temp_c"]
        return f"The weather in {city} is {condition} with a temperature of {temp} degrees Celsius."
    return "Could not fetch weather details."

def get_stock_price(company_symbol):
    url = f"https://financialmodelingprep.com/api/v3/quote/{company_symbol}?apikey=YOUR_API_KEY"
    response = requests.get(url).json()
    if response:
        return f"The stock price of {company_symbol} is {response[0]['price']} USD."
    return "Could not fetch stock price."

# Function to fetch random facts
def get_random_fact():
    url = "https://uselessfacts.jsph.pl/random.json?language=en"
    response = requests.get(url).json()
    return response["text"]

def ask_openai(question):
    """Get an AI-generated response"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful AI assistant."},
                  {"role": "user", "content": question}]
    )
    return response["choices"][0]["message"]["content"]

# Function to control PC (shutdown, restart, lock)
def control_pc(command):
    if "shutdown" in command:
        speak("Shutting down the computer in 3 seconds.")
        os.system("shutdown /s /t 5")
    elif "restart" in command:
        speak("Restarting the computer in 5 seconds.")
        os.system("shutdown /r /t 5")
    elif "lock" in command:
        speak("Locking the computer.")
        os.system("rundll32.exe user32.dll,LockWorkStation")

def translate_text(text, lang="fr"):
    translator = Translator()
    translated_text = translator.translate(text, dest=lang).text
    return translated_text

# Function to generate a random password
def generate_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return "".join(secrets.choice(chars) for _ in range(length))



if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand()

        if "wikipedia" in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak(results)
            

        elif "chrome" in query:
         os.system("start chrome")

        elif "open youtube" in query:
            webbrowser.open("youtube.com")

        elif "open google" in query:
            webbrowser.open("google.com")

        elif "open stackoverflow" in query:
            webbrowser.open("stackoverflow.com")

        elif "whatsapp" in query:
            webbrowser.open("https://web.whatsapp.com/")

        elif "play music" in query:
            music_dir = 'D:\\Music'  # Change to your music folder
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, random.choice(songs)))

        elif "the time" in query:
            speak(f"The time is {datetime.datetime.now().strftime('%H:%M:%S')}")

        elif "email to ritesh" in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                sendEmail("ritesh@example.com", content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry, I couldn't send the email.")

        elif "news" in query:
            speak("Fetching the latest news...")
            speak(get_news())

        elif "weather" in query:
            speak("Which city?")
            city = takeCommand()
            speak(get_weather(city))

        elif "screenshot" in query:
            img = pyautogui.screenshot()
            img.save("screenshot.png")
            speak("Screenshot taken!")

        elif "cpu" in query:
            usage = str(psutil.cpu_percent())
            speak(f"CPU usage is at {usage} percent.")

        elif "battery" in query:
            battery = psutil.sensors_battery()
            speak(f"Battery is at {battery.percent} percent.")

        elif "tell me a joke" in query:
            speak(pyjokes.get_joke())

        elif "search in google for" in query:
            search_query = query.replace("search google for", "").strip()
            kit.search(search_query)
            speak(f"Searching Google for {search_query}")

        elif "whatsapp message" in query:
            speak("Who should I send it to?")
            phone_number = input("Enter phone number: ")
            speak("What message should I send?")
            message = takeCommand()
            kit.sendwhatmsg(phone_number, message, datetime.datetime.now().hour, datetime.datetime.now().minute + 1)
            speak("Message sent.")

        elif "stock price" in query:
            speak("Which company?")
            company = takeCommand()
            speak(get_stock_price(company))

        elif "random fact" in query:
                speak("Here's a fun fact for you!")
                speak(get_random_fact())
        
        elif "set reminder" in query:
            speak("What should I remind you about?")
            task = takeCommand()
            speak("In how many minutes?")
            duration = int(takeCommand())

        elif "shutdown" in query or "restart" in query or "lock" in query:
            control_pc(query)

        elif "translate" in query:
            speak("What do you want to translate?")
            text = takeCommand()
            speak("Which language?")
            lang = takeCommand()
            translated_text = translate_text(text, lang)
            speak(f"The translation is: {translated_text}")

        elif "generate password" in query:
            password = generate_password()
            pyperclip.copy(password)
            speak("Here is a secure password. I have copied it to your clipboard.")

        elif "open code" in query:
            code_path = "C:/Users/username/Documents/Code"  # Change to your code editor path
            os.startfile(code_path)

        elif "open notepad" in query:
            os.system("notepad")

        elif "open camera" in query:
            os.system("camera")
            
        elif "increase volume" in query:
            pyautogui.press("volumeup")

        elif "decrease volume" in query:
            pyautogui.press("volumedown")

        elif "mute" in query:
            pyautogui.press("volumemute")

        elif "ai chat" in query:
            speak("What do you want to ask?")
            question = takeCommand()
            answer = ask_openai(question)
            speak(answer)

        elif "exit" in query or "stop" in query:
            speak("Goodbye! Have a great day.")
            exit()
