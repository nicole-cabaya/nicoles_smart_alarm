"""
This module is the main module that contains the smart-alarm system.

What is does is, it extracts information from json files acquired using their corresponding APIs.
We can set alarms, read notifications and we are also able to delete them.

Functions:
hhmm_to_seconds(alarm_time) --
announce(announcement) --
title_content() --
enter_event() --
storing_alarms() --
set_default_notifications() --
news() -- we extract information from the news json, assign them to variables and return them
weather() -- we extract information from the news json, assign them to variables and return them
public_health_exeter() -- we extract information from the public health england json, assign them to variables and return them
public_health_england() -- we extract information from the public health england json, assign them to variables and return them
main_scheduler() -- this function is run in a loop by the flask module

"""

from datetime import datetime, date
import time
import sched
import logging
import json
from flask import request, Flask, render_template
import pyttsx3
from api_requests import news_request,weather_request
from api_requests import public_health_exeter_req, public_health_england_req

#initiate scheduler
s = sched.scheduler(time.time, time.sleep)
app = Flask(__name__)
#initiate text-to-speech to be used in announcements
engine = pyttsx3.init()
#date and time will be used to check for invalid alarms set
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
# Get today's date
today = date.today()

#convert the time interval between the alarm and the current time into seconds
def hhmm_to_seconds(alarm_time: str) -> int:
    "Convert time argument and current time into seconds, then return the delay time."
    split_hhmm = list(alarm_time.split(':'))
    hours_to_secs = int(split_hhmm[0]) * 3600
    mins_to_secs = int(split_hhmm[1]) * 60
    secs = int(split_hhmm[2])
    hhmm_to_secs = hours_to_secs + mins_to_secs + secs
    logging.info("alarm time delay calculated")
    return hhmm_to_secs

#this will enable text-to-speech to read the announcements out loud
def announce(announcement:str):
    "Enable text-to-speech, and use it in the announcement."
    try:
        engine.endLoop()
    except:
        logging.error('PyTTSx3 Endloop error')
    engine.say(announcement)
    engine.runAndWait()

#this will regularly update the notifications and alarms
def title_content() -> list:
    "Assign title and content to alarms and notifications."
    #appends updated alarms json file so that it is displayed in the html
    alarms = []
    with open("json_files/alarms.json","r") as file:
        alarms_file = json.load(file, strict=False)
    file.close()
    value_counter = 0
    alarms_in_json = alarms_file["data"]
    for key in list(alarms_in_json.keys()):
        time = list(alarms_in_json.values())[value_counter].replace("T", " ")
        alarms.append({"title": "ALARM LABEL: "+key,"content":"ALARM SET: "+time})
        value_counter = value_counter + 1
    now = datetime.now()
    if int(now.minute) == 0  :
        logging.info("default notifications set")
    notifications = set_default_notifications()
    return notifications, alarms


#if the alarm is set for today it will enter it in the scheduler
def enter_event():
    "Enter alarm in the scheduler."
    #alarms = title_content()
    notifs = set_default_notifications()
    notifs = notifs[3]["content"]
    #convert alarm_time to a delay
    delay = hhmm_to_seconds(ALARM_SPLIT_TIME) - hhmm_to_seconds(current_time)
    s.enter(int(delay), 1, announce, ["COVID RATES IN EXETER "+notifs,])
    logging.info("alarm set")

    #<<<COME BACK TO THIS LATER!!!: cancelling events>>>-------------------------------------------
    #with open("json_files/events.json","r") as f:
        #events_file = json.load(f)
    #f.close()
    #adds new alarm
    #events_file[alarm_text] = "why"
    #with open("json_files/events.json","w") as updated_file:
        #json.dump(events_file, updated_file, indent=2)
    #updated_file.close()

#this will store and remove alarms from the alarms.json file
def storing_alarms():
    "Store alarm in alarms json file to enable to add/remove alarms."
    global ALARM_SPLIT_TIME, ALARM_TEXT
    alarm_time = request.args.get("alarm")
    ALARM_TEXT = request.args.get("two")
    if alarm_time:
        alarm_split_date_time = alarm_time.split("T")
        alarm_split_date = str(alarm_split_date_time[0])
        ALARM_SPLIT_TIME = str(alarm_split_date_time[1]) + ":00"
        year = int(alarm_split_date[:4])
        month = int(alarm_split_date[5:7])
        day = int(alarm_split_date[-2:])
        with open("json_files/alarms.json","r") as file:
            alarms_file = json.load(file, strict=False)
        file.close()
        #check if the alarm time set has passed
        if datetime(year,month,day,int(ALARM_SPLIT_TIME[:2]),int(ALARM_SPLIT_TIME[-5:-3])) < now:
            logging.error("Alarm time set has passed")
        #if the alarm set is for today enter in the scheduler
        elif alarm_split_date == str(today):
            enter_event()
        if ALARM_TEXT in list(alarms_file["data"].keys()):
            #counter used to access the corresponding value of the key
            x_counter=1
            #if the labels are duplicated, just add a number in the label
            while ALARM_TEXT in list(alarms_file["data"].keys()):
                x_counter = x_counter+1
                ALARM_TEXT = ALARM_TEXT+str(x_counter)
        logging.info("existing label detected")
        if datetime(year,month,day,int(ALARM_SPLIT_TIME[:2]),int(ALARM_SPLIT_TIME[-5:-3])) >= now:
            #adds new alarm
            alarms_file["data"][ALARM_TEXT] = alarm_time
            #updates alarms_json
            with open("json_files/alarms.json","w") as updated_file:
                json.dump(alarms_file, updated_file, indent=2)
            updated_file.close()

def set_default_notifications():
    "Set the notifications to default notifications."
    #extract inormation from corresponding json files
    title1, content1, title2, content2 = news()
    weather_city, weather_temp, weather_des, weather_pre, weather_hum = weather()
    date1, area_name1, new_cases1, cumulative_cases1 = public_health_exeter()
    date2, area_name2, new_cases2, cumulative_cases2 = public_health_england()
    weather_city = str(weather_temp)
    weather_pre = str(weather_pre)
    weather_hum = str(weather_hum)
    #assign the extracted information from APIs to variables
    title1 = "NEWS: "+title1
    title2 = "NEWS: "+title2
    title3 = "WEATHER (right now) : "+weather_city
    title4 = "PUBLIC HEALTH ENGLAND--YESTERDAY'S COVID-19 RATES: {area}".format(area=area_name1)
    title5 = "PUBLIC HEALTH ENGLAND--YESTERDAY'S COVID-19 RATES: {area}".format(area=area_name2)
    content3_1 = "TEMPERATURE(Kelvin): {temp}, DESCRIPTION: {des},"
    content3_2 = " PRESSURE(hPa): {pre}, HUMIDITY(%): {hum}"
    content3 = content3_1+content3_2
    cont3 = content3.format(temp=weather_temp, des=weather_des, pre=weather_pre, hum=weather_hum)
    content4_1 = "DATE: {date1}, NEW CASES: {new_cases1}, CUMULATIVE CASES: {cum_cases1}"
    content4 = content4_1.format(date1=date1, new_cases1=new_cases1, cum_cases1=cumulative_cases1)
    content4_1 = "DATE: {date2}, NEW CASES: {new_cases2}, CUMULATIVE CASES: {cum_cases2}"
    content5 = content4_1.format(date2=date2, new_cases2=new_cases2, cum_cases2=cumulative_cases2)
    #notifications data structure
    notifications = [{"title" : title1,"content" : content1},
    {"title" : title2,"content" : content2},
    {"title" : title3,"content" : cont3},
    {"title" : title4,"content" : content4},
    {"title" : title5,"content" : content5}]
    return notifications

#announcements section---------
def news():
    "Extract covid related information from the news json file."
    news_request()
    covid_words = ['covid','lockdown',"coronavirus","covid-19"]
    covid_filter ={"articles":[]}
    with open('json_files/news_json.json', 'r') as file:
        news_json = json.load(file, strict=False)
    articles = news_json["articles"]
    for article in articles:
        for word in covid_words:
            if word in article['title'].lower():
                if {"title":article['title'], "content":article["description"]} not in covid_filter["articles"]:
                    covid_filter["articles"].append({"title":article['title'], "content":article["description"]})
    with open('json_files/news_notifs.json', 'w') as file:
        json.dump(covid_filter, file, indent=2)
    file.close()
    title1 = covid_filter["articles"][0]["title"]
    content1 = covid_filter["articles"][0]["content"]
    title2 = covid_filter["articles"][1]["title"]
    content2 = covid_filter["articles"][1]["content"]
    logging.info("news extracted")
    return title1, content1, title2, content2

def weather():
    "Extract weather information from weather json file."
    weather_request()
    with open('json_files/weather_json.json', 'r') as file:
        weather_file = json.load(file, strict=False)
    if weather_file["cod"] != "404":
        city = weather_file["name"]
        temperature = weather_file["main"]["temp"]
        description = weather_file["weather"][0]["description"]
        pressure = weather_file["main"]["pressure"]
        humidity = weather_file["main"]["humidity"]
    file.close()
    logging.info("weather extracted")
    return city, temperature, description, pressure, humidity

def public_health_exeter():
    "Extract covid rates in Exeter from corresponding json file."
    public_health_exeter_req()
    with open('json_files/public_health_exeter.json', 'r') as file:
        exeter_file = json.load(file, strict=False)
        try:
            date_yes = exeter_file["data"][0]["date"]
            area_name = exeter_file["data"][0]["areaName"]
            new_cases = exeter_file["data"][0]["newCasesByPublishDate"]
            cumulative_cases = exeter_file["data"][0]["cumCasesByPublishDate"]
        except:
            logging.error("Error occurred while passing information from API")
            date_yes = "ERROR-404"
            area_name = "ERROR-404"
            new_cases = "ERROR-404"
            cumulative_cases = "ERROR-404"
    file.close()
    logging.info("covid rates in exeter extracted")
    return date_yes, area_name, new_cases, cumulative_cases

def public_health_england():
    "Extract covid rates in England from corresponding json file."
    public_health_england_req()
    with open('json_files/public_health_england.json', 'r') as file:
        exeter_file = json.load(file, strict=False)
        try:
            date_yes = exeter_file["data"][0]["date"]
            area_name = exeter_file["data"][0]["areaName"]
            new_cases = exeter_file["data"][0]["newCasesByPublishDate"]
            cumulative_cases = exeter_file["data"][0]["cumCasesByPublishDate"]
        except:
            logging.error("Error occurred while passing information from API")
            date_yes = "ERROR-404"
            area_name = "ERROR-404"
            new_cases = "ERROR-404"
            cumulative_cases = "ERROR-404"

    file.close()
    logging.info("covid rates in england extracted")
    return date_yes, area_name, new_cases, cumulative_cases

#main function--------
@app.route('/index')
def main_scheduler():
    "Render template and connect other functions to allow full functionality."
    #access config file
    with open("json_files/config.json","r") as config:
        config_file = json.load(config,strict=False)
    logfile = config_file["filepaths"]["logfile"]
    config.close()
    #create a log file to store a log of events and errors
    logging.basicConfig(filename=logfile,level=logging.INFO)
    s.run(blocking=False)
    cancel_alarm = request.args.get("alarm_item")
    #cancel alarms if the x button is pressed
    if cancel_alarm:
        logging.info("alarm cancelled")
        with open("json_files/alarms.json","r") as file:
            alarms_file = json.load(file, strict=False)
        file.close()
        label = cancel_alarm.replace("ALARM LABEL: ","")
        #cancels alarms (removes alarm from json file)
        del alarms_file["data"][label]
        with open("json_files/alarms.json","w") as updated_file:
            json.dump(alarms_file, updated_file, indent=2)
        updated_file.close()
    notifications, alarms = title_content()
    storing_alarms()
    #access image from config file
    with open("json_files/config.json",'r') as file:
        config_file = json.load(file, strict=False)
    image = config_file["filepaths"]["image"]
    template = config_file["filepaths"]["template"]
    file.close()
    return render_template(template,notifications=notifications, alarms=alarms, image=image)

if __name__ == '__main__':
    app.run()
