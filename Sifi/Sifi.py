import datetime
import re
import subprocess
import sys
import webbrowser
from ctypes import CDLL
from time import strftime
from urllib.request import urlopen

import openai
import pyttsx3
import requests
import speech_recognition as sr
import wikipedia
import wolframalpha
import yagmail
from bs4 import BeautifulSoup
from newsdataapi import NewsDataApiClient

engine = pyttsx3.init()

# RATE
rate = engine.getProperty('rate')
engine.setProperty('rate', 170)

# VOICE
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

welcomeMessage = 'Hi, I am Sifi, your intelligent virtual assistant. How can I help you?'
print(welcomeMessage)
engine.say(welcomeMessage)
engine.runAndWait()

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

app_id = 'HYPEHX-PGQGQTJJ6E'   # wolfram_API


def newCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Say something...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')
    # loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('Sorry I can\'t understand')
        command = newCommand()
    return command


def sifiResponse(audio):
    print(audio)
    engine.say(audio)
    engine.runAndWait()

def search_wikipedia(keyword=''):
    searchResults = wikipedia.search(keyword)
    if not searchResults:
        return 'No result received'
    try:
        wikiPage = wikipedia.page(searchResults[0])
    except wikipedia.DisambiguationError as error:
        wikiPage = wikipedia.page(error.options[0])
    print(wikiPage.title)
    wikiSummary = str(wikiPage.summary)
    return wikiSummary

def assistant(command):
    # if statements for executing commands

    # Questions about Sifi
    if 'your name' in command:
        sifiResponse('My name is Sifi. Nice to meet you!')
    elif 'who are you' in command:
        sifiResponse('I\'m Sifi, your intelligent virtual assistant!')
    elif 'do you feel' in command:
        sifiResponse('I\'m doing great, thanks for asking.')
    elif 'old are you' in command:
        sifiResponse('I was born last week.')
    elif 'what can you do' in command:
        sifiResponse(
            'I can do a lot of things, to help you throughout your day.')
    elif 'help me' in command:
        sifiResponse('I\'m here to help, you can ask me what I can do.')
    elif 'like siri' in command:
        sifiResponse('I like Siri, she\'s very nice.')

    # Greet Sifi
    elif 'hello' in command:
        day_time = int(strftime('%H'))
        if day_time < 12:
            sifiResponse('Hello, Good morning!')
        elif 12 <= day_time < 18:
            sifiResponse('Hello, Good afternoon!')
        else:
            sifiResponse('Hello, Good evening!')
    elif 'thank you' in command:
        sifiResponse('You\'re Welcome!')

    # Make Sifi stop
    elif 'shutdown the program' in command:
        sifiResponse('Bye bye. Have a nice day!')
        sys.exit()

    # Open Twitter
    elif 'open twitter' in command:
        reg_ex = re.search('open twitter (.*)', command)
        url = 'https://www.twitter.com/'
        if reg_ex:
            handle = reg_ex.group(1)
            url = url + handle
        webbrowser.open(url)
        sifiResponse(
            'Opening Twitter.')

    # Open Instagram
    elif 'open instagram' in command:
        reg_ex = re.search('open instagram (.*)', command)
        url = 'https://www.instagram.com/'
        if reg_ex:
            handle = reg_ex.group(1)
            url = url + handle
        webbrowser.open(url)
        sifiResponse(
            'Opening Instagram.')

    # Open subreddit Reddit
    elif 'open reddit' in command:
        reg_ex = re.search('open reddit (.*)', command)
        url = 'https://www.reddit.com/'
        if reg_ex:
            subreddit = reg_ex.group(1)
            url = url + 'r/' + subreddit
        webbrowser.open(url)
        sifiResponse(
            'Opening Reddit.')

    # Open any website
    elif 'open' in command:
        reg_ex = re.search('open (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            url = 'https://www.' + domain
            webbrowser.open(url)
            sifiResponse(
                'Opening ' + domain)

    # Make a search on Google
    elif 'search' in command:
        reg_ex = re.search('search (.+)', command)
        if reg_ex:
            subject = reg_ex.group(1)
            url = 'https://www.google.com/search?q=' + subject
            webbrowser.open(url)
            sifiResponse(
                'Searching for ' + subject + ' on Google.')

    # Play a song on Youtube
    elif 'play' in command:
        reg_ex = re.search('play (.+)', command)
        if reg_ex:
            searchedSong = reg_ex.group(1)
            url = 'https://www.youtube.com/results?q=' + searchedSong
            try:
                source_code = requests.get(url, headers=headers, timeout=15)
                plain_text = source_code.text
                soup = BeautifulSoup(plain_text, "html.parser")
                songs = soup.findAll('div', {'class': 'yt-lockup-video'})
                song = songs[0].contents[0].contents[0].contents[0]
                hit = song['href']
                webbrowser.open('https://www.youtube.com' + hit)
                sifiResponse('Playing ' + searchedSong + ' on Youtube.')
            except Exception as e:
                webbrowser.open(url)
                sifiResponse('Searching for ' + searchedSong + ' on Youtube.')

    # Send Email
    elif 'email' in command:
        sifiResponse('What is the receiver email?')
        receiver = newCommand().replace(" ","")
        sender = "sarthak2952@gmail.com"
        password = "Youngdumb"
        if '@' in receiver:
            sifiResponse('What is the subject?')
            subject = newCommand()
            sifiResponse('What should I say to him?')
            content = newCommand()
            try:
                yag = yagmail.SMTP(sender, password)
                yag.send(
                    to=receiver,
                    subject=subject,
                    contents=content
                )
                sifiResponse(
                    'Email has been sent successfuly.')
            except Exception as e:
                print(e)
        else:
            sifiResponse('I don\'t know anyone named ' + receiver + '.')

    # Launch apps
    elif 'launch' in command:
        reg_ex = re.search('launch (.*)', command)
        if reg_ex:
            appname = reg_ex.group(1)
            appname1 = appname+".app"
            subprocess.run(["/usr/bin/open", "-a", appname1])
            subprocess.Popen(["/usr/bin/open", "-a", appname1])
            sifiResponse('Launching ' + appname + '.')
            newCommand()

    # Get current time
    elif 'time' in command:
        now = datetime.datetime.now()
        sifiResponse('Current time is %d:%d.' %
                      (now.hour, now.minute))

    # Get recent news
    elif 'news' in command:
        try:
            api = NewsDataApiClient(apikey="pub_19348ced16687bb956e90fc4ba74f90d363e7")
            response = api.news_api(language="en")
            thislist = response["results"]
            news_list = []
            for i in range(len(thislist)):
                news_list.append(thislist[i]["title"])
            for news in news_list[:5]:
                sifiResponse(news)
        except Exception as e:
            print(e)

    # Lock the device
    elif 'lock' in command:
        try:
            sifiResponse("Locking the device.")
            loginPF = CDLL('/System/Library/PrivateFrameworks/login.framework/Versions/Current/login')
            result = loginPF.SACLockScreenImmediate()
        except Exception as e:
            print(str(e))

    # Ask general questions
    elif 'tell me about' in command:
        reg_ex = re.search('tell me about (.*)', command)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                sifiResponse(search_wikipedia(topic))
        except Exception as e:
            sifiResponse(e)
    elif any(c in command for c in ("what is", "what\'s")):
        reg_ex = re.search(' (.*)', command)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                sifiResponse(search_wikipedia(topic))
        except Exception as e:
            sifiResponse(e)

    # All other cases
    else:
        try:
            # wolframalpha
            client = wolframalpha.Client(app_id)
            res = client.query(command)
            answer = next(res.results).text
            sifiResponse(answer)
        except:
            openai.api_key = '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'
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=command,
                temperature=0.3,
                max_tokens=80,
            )
            sifiResponse(response.choices[0].text)


while True:
    assistant(newCommand())


