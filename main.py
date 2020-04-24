from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import  pytz
import speech_recognition as sr  #speech recognision module
import pyttsx3  #text to speech module
import requests #Requests is a Python HTTP library
import json  #JSON encoder and decoder
import geotext
import  os
import  time
import  webbrowser
import datetime
import wikipedia
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
DAY_EXTENSIONS = ["nd", "rd", "th", "st"]
lines=['tomorrow','day after tomorrow']
rem={}
engine=pyttsx3.init()
def speak(text):
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 140)
    engine.setProperty('language','en-IN')
    engine.say(text)
    engine.runAndWait()
    return 'done'


def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("wait a second adjusting noise")
        r.adjust_for_ambient_noise(source)
        print("listening.......")
        audio = r.listen(source, phrase_time_limit=4)
        try:
            r.record(source, duration=0.5)
            text = r.recognize_google(audio,language='en-In')
            print("\t \t \tyou said: "+text)
            return text
        except Exception as e:
            print(e)
            print("sorry can't hear your voice")
            return 'l'
        return 'done'
def authenticate_google():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return  service
def get_events(day, service):
    # Call the Calendar API
    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end = end.astimezone(utc)
    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(), timeMax=end.isoformat(),
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:

        return 'No upcoming events found'
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
        fr=(event['start'].get('dateTime')[14:19])
        t=(event['start'].get('dateTime')[20:])
        x='from: ' +fr[:2] +' hour '+ fr[3:] +' minute ' +' to '+t[:2] +' hour'+ t[3:] +' minute'
        return x,event['summary']
def get_date(text):
    text=text.lower()
    today=datetime.date.today()
    tomorrow=datetime.date.today() + datetime.timedelta(days=1)
    if "today" in text:
        return  today
    elif 'tomorrow' in text:
        return tomorrow
    day=-1
    day_of_week=-1
    month=-1
    year=today.year
    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word)+1
        elif word in DAYS:
            day_of_week=DAYS.index(word)
        elif word.isdigit():
            day=int(word)
        else:
            for ext in DAY_EXTENSIONS:
                found = word.find(ext)
                if found>0:
                    try:
                        day=int(word[:found])
                    except:
                        pass
    if month<today.month and not month==-1:
        year=year+1
    if day<today.day and month==-1 and not day==-1:
        month=month+1
    if month==-1 and day==-1 and not day_of_week==-1:
        current_day_of_the_week=today.weekday()
        diff=day_of_week-current_day_of_the_week
        if diff<0:
            diff+=7
            if text.count("next")>=1:
                diff+=7
        return today+datetime.timedelta(diff)
    return  datetime.date(month=month,day=day,year=year)



#function to extract location from ipadress
def loc():
    send_url = "http://api.ipstack.com/check?access_key=fa093da6b0eb77a092a86e2befdbcb2a"
    geo_req = requests.get(send_url)
    geo_json = json.loads(geo_req.text)
    c = geo_json['city']
    return c



#main function to give weather report
def wharth(city):
    r = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID=c7abd97279fc11ebc6e0e02d046da782')
    x = r.json()
    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        feels_like=y['feels_like']
        maxi=y['temp_max']
        mini=y['temp_min']
        humid=y['humidity']
        c=x['wind']
        wind_speed=c['speed']
        d=x['clouds']
        coulds=d['all']
        z = x["weather"]
        weather_description = z[0]["description"]
        forecast=(str(city) +" have temperature "+str(round(current_temperature-273))+"degree celcius"+"\n feels like"+str(round(feels_like-273))+"degree celcius"+"\n maxiumum will be " +str(round(maxi-273))+"minimum will be"+str(round(mini-273))+"\nhumidity in your area is "+str(humid)+"\n wind speed is"+str(wind_speed)+"killometre per hour"+"\n clouds in your area "+str(coulds)+"percent"+"\n overall weather will be"+str(weather_description))
    else:
        print(" City Not Found ")
    return forecast

def wishme():
    now = datetime.datetime.now()
    x = now.strftime("%H")
    if x>='0' and x<='12':
        speak('HEY!!! Good Morning G S AAshish')
    elif x>='12'  and x<='17':
        speak('HEY!!! Good Afternoon G S AAshish')
    elif x>='17' and x<='19':
        speak('HEY!!! Good Evening G S AAshish ')
    elif x>='19' and x<='24':
        speak(f"HEY!!! G S AASHISH")

def data_date():
    now = datetime.datetime.now()
    a = now.strftime("%Y %m %d")
    monts = {'01': 'january',
             '02': 'febuary',
             '03': 'march',
             '04': 'april',
             '05': 'may',
             '06': 'june',
             '07': 'july',
             '08': 'august',
             '09': 'september',
             '10': 'october',
             '12': 'december',
             '11': 'november',
             }
    li = [x for x in a.split(" ")]
    li[1] = monts[li[1]]
    speak(f"todays date is {li[2]} {li[1]} {li[0]}")


def wiki(txt):
    wikipedia.summary(txt,sentences=1)
    return wikipedia.summary(txt,sentences=1)
def closeOpera():
    browserExe = "opera.exe"
    return os.system("taskkill /f /im " + browserExe)
# def reminder():
#     speak('what i have to remember')
#     a=listen()
#     while 1:
#         with open('reminder.txt', 'r+')as f:
#             c=f.read()
#
#         if  a not in c:
#             with open('reminder.txt','a')as f:
#                 f.write(a)
#             speak(f"ok i'll remember this: {a}")
#         else:
#             speak("I'll remember that")
#             break
#         return reminder()



def main():
    while True:
        a = listen()
        if 'how are you' in a.lower():

            speak("i'm fine how are you ")
        elif 'hello' in a.lower():
            speak('hello tell me what can i do for you')
        elif 'time' in a.lower():
            now = datetime.datetime.now()
            a = now.strftime("%H:%M:%S")
            speak(a)

        elif  'weather' in a:
            try:
                cit=geotext.GeoText(a).cities
                con=geotext.GeoText(a).countries
                if not cit==[] :

                    speak(wharth(cit[0]))
                elif not con==[]:
                    speak(wharth(con[0]))

                else:

                    speak(wharth(loc()))
            except:

                city=loc()
                speak(wharth(city))

        elif  ('who created you' in a.lower()) or ('your creator name' in a.lower()) or ('your father name' in a.lower()) or ("tell me your creator name" in a.lower()) or 'creator' in a.lower():

                speak('MY CREATER IS G S AASHISH \n he created me on fourteenth april 2020 .........one very important  fact  on this day prime minister Shri Narender Modi of india announced extention of quarantine holiday  due to COVID-19  till 3rd may in his ten A.M. speech \n my creater created me in quarantine holidays')

        elif 'open spotify' in a.lower():
            url = "https://open.spotify.com"
            webbrowser.open(url)
            speak("opening spotify")

        elif 'prateek kuhad song' in a.lower() or 'prateek kuhad songs' in a.lower():
            url = "https://open.spotify.com/artist/0tC995Rfn9k2l7nqgCZsV7"
            webbrowser.open(url)
            speak("opening spotify")

        elif 'my mother name' in a :
            speak('Your Mother Name is Sadhna Lal')
            speak('Now she will give you 100 rupees')
        elif 'open sapne song' in a.lower() or 'sapna song' in a.lower():
            url="https://www.youtube.com/watch?v=UQoQRiOGqVg"
            webbrowser.open(url)
            speak("opening  Sapne song by MO JOJO youtube")

        elif 'open youtube' in a.lower():
            url="https://www.youtube.com"
            webbrowser.open(url)
            speak("opening   youtube")

        elif 'open youtube' in a.lower():
            url="https://www.google.com"
            webbrowser.open(url)
            speak("opening   youtube")

        elif 'date'  in a.lower():
            data_date()


        elif 'close opera' in a.lower() :
            closeOpera()
            speak("closing opera")

            time.sleep(5)
        elif 'wikipedia' in a.lower():
            a=a.replace('wikipedia','')
            print("new:",a)
            speak(wiki(a))

        elif 'play song' in a.lower():

            url = "https: // open.spotify.com / artist / 3Y5nIabMJLTsWgW6Jqdn7n"
            webbrowser.open(url)
            speak("opening spotify")

        elif 'she can' in a.lower():

            url = "https://www.youtube.com/watch?v=uj6pLKl2wU0"
            webbrowser.open(url)
            speak("opening youtube")

        elif 'exit' in a.lower() or 'sleep' in a.lower() or 'stop' in a.lower() or 'close' in a.lower():
            speak('going on sleep')
            break
        elif 'jor se bolo' in a.lower():
            speak('jai MATA di')
            print('\t \t \t jai mata dii 🚩🚩🚩🚩🚩🚩')
        elif a=="l":
            continue
        elif 'who lives in your heart' in a.lower():
            speak('Shri Ram Jaanki Baithee Hain Mere Seene Mein')
            speak('jai shri ram   ')
            print('\t\t\t jai shri ram🚩🚩🚩🚩🚩🚩')

        elif 'do i have' in a.lower() :
            SERVICE = authenticate_google()
            text = a.lower()
            try:
                c=get_events(get_date(text), SERVICE)

                if c=='No upcoming events found.':
                    speak("you don't have any event" )
                else:
                    speak('you have following events:')

                    speak(c)
            except:
                speak("sorry i could not able to hear your complete command say it again please!!")

        else:
            speak("can't able to perform this task")

        return main()
speak('intializing........ ')
print('intializing........ Niharika')
speak("hello I'm NIHAARIKA your virtual asistance , how Can I help you")
print("setting up your  Niharika environment........")
wishme()
main()
