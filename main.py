import os
import sys
import traceback
from typing import List
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv

from selenium import webdriver
import pyttsx3 as p
from pyttsx3.voice import Voice
import speech_recognition as sr
import pyjokes
import pygame

load_dotenv()

engine = p.init()
engine.setProperty('rate', 200)
voices: List[Voice] = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
r = sr.Recognizer()
_options = Options()
_options.headless = True
_service = Service(executable_path=os.getenv('chrome_driver'))
driver = webdriver.Chrome(options=_options, service=_service)
pygame.init()
pygame.mixer.init()

dev = os.getenv('dev') == 'True'

def speak(text):
    print(f'Out: {text}')
    engine.say(text)
    engine.runAndWait()


def listen(source):
    print("listening...")
    if dev:
        return input('In: ')
    try:
        audio = r.listen(source=source)
        text = r.recognize_google(audio)
        print(f'In: {text}')
        return text
    except Exception as err:
        print(f'listening err {err}')
        print(traceback.format_exc())
        return ''


def get_info(query):
    driver.get(url="https://www.wikipedia.org")
    search = driver.find_element("xpath", '//*[@id="searchInput"]')
    search.click()
    search.send_keys(query)
    enter = driver.find_element("xpath", '//*[@id="search-form"]/fieldset/button')
    enter.click()


def play(query):
    driver.get(url="https://www.youtube.com/results?search_query=" + query)
    video = driver.find_element("xpath", '//*[@id="video-title"]/yt-formatted-string')
    video.click()


def Gambinopl():
    lists_of_gabino = os.listdir()

    for song in lists_of_gabino:
        if song.endswith(".mp3"):
            file_path = "./" + song
            pygame.mixer.music.load(str(file_path))
            pygame.mixer.music.play()
            print("playing Childish Gambino")
            while pygame.mixer.music.get_busy() == True:
                continue


def weather():
    driver.get(url="https://www.weather-forecast.com/locations/Mauensee/forecasts/latest")
    forecast = driver.find_element("xpath", '/html/body/main/section[3]/div/div/div[2]/div/table/thead/tr[1]/td[1]/p')
    return forecast.text


def main():
    speak("hello sir, how are you today?")
    with sr.Microphone() as source:
        r.energy_threshold = 10000
        r.adjust_for_ambient_noise(source, 1.2)
        while True:
            text = listen(source)
            if all(x in text for x in ["what", "about", "you"]) or all(
                    x in text for x in ["how", "about", "you"]) or all(x in text for x in ["how", "are", "you"]):
                speak("I am very good thank you")
            elif any(x in text for x in ["information", "facts"]):
                speak("you need information to which topic?")
                infor = listen(source)
                if infor == "":
                    speak("alright then keep your secrets")
                else:
                    speak(f"one moment I am looking for {infor} in wikipedia")
                    print(f"{infor} on wikipedia")
                    get_info(infor)
            elif any(x in text for x in ["song"]):
                speak("which song?")
                songname = listen(source)
                speak(f"one moment im looking for {songname} on youtube")
                print(f"playing {songname} on youtube")
                play(songname)
            elif any(x in text for x in ["joke"]):
                joke = pyjokes.get_joke()
                speak(f"here is a joke for you. {joke}")
            elif all(x in text for x in ["how", "weather"]):
                speak(f"the weather in Mauensee is, {weather()}")
            elif any(x in text for x in ["Gambino"]):
                speak("playing childish Gambino.")
                speak(f"{Gambinopl()}")
            elif any(x in text for x in ["goodbye", "shut up", "stop"]):
                exit()
            elif text != '':
                speak("I didn't get that. What can I do for you?")


try:
    if __name__ == '__main__':
        sys.exit(main())
except KeyboardInterrupt:
    pass
finally:
    print("Stopping...")
    driver.quit()
