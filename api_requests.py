"""
This module extracts information from corresponding APIs using json files.

Functions:
access_config_file() -- acessses resources from config file
news_request() -- extracts news json file from news api
weather_request() -- extracts weather json file from weather api
public_health_exeter_req() -- extracts covid-19 information from public health england api
public_health_england_req() -- extracts covid-19 information from public health england api

"""
import json
from datetime import date
from datetime import timedelta
import requests

def access_config_file() -> str:
    "Open config json file and extract keys"
    with open("json_files/config.json",'r') as file:
        json_file = json.load(file, strict=False)
    keys = json_file["API-KEYS"]
    location = json_file["location"]
    base_url = json_file["base_url"]
    file.close()
    return keys, location, base_url

def news_request():
    "Open news json file and extract keys"
    keys, location, base_url = access_config_file()
    base_url = base_url["news_url"]
    api_key = keys["news"]
    country = location['country']
    complete_url = base_url + "country=" + country + "&apiKey=" + api_key
    response = requests.get(complete_url)
    news_json = response.json()
    with open('json_files/news_json.json', 'w') as file:
        json.dump(news_json, file, indent=2)
    file.close()

def weather_request():
    "Open weather json file and extract keys"
    keys, location, base_url = access_config_file()
    base_url = base_url["weather_url"]
    api_key = keys["weather"]
    city = location["city"]
    complete_url = base_url + "q=" + city + "&appid=" + api_key
    response = requests.get(complete_url)
    weather_json = response.json()
    with open('json_files/weather_json.json', 'w') as file:
        json.dump(weather_json, file, indent=2)
    file.close()

def public_health_exeter_req():
    "Open public health england json file and extract keys"
    # Get today's date
    today = date.today()
    # Yesterday date
    yesterday = today - timedelta(days = 1)
    keys, location, base_url = access_config_file()
    structure = "structure=" +'{"date":"date","areaName":"areaName","newCasesByPublishDate":"newCasesByPublishDate","cumCasesByPublishDate":"cumCasesByPublishDate"}'
    filter_exeter = base_url["filter_ex"]+str(yesterday)+'&'
    complete_url = base_url["public_h_eng"] + filter_exeter + structure
    response = requests.get(complete_url)
    covid_json_exeter = response.json()
    with open('json_files/public_health_exeter.json', 'w') as file:
        json.dump(covid_json_exeter, file, indent=2)
    file.close()

def public_health_england_req():
    "Open public health england json file and extract keys"
    # Get today's date
    today = date.today()
    # Yesterday date
    yesterday = today - timedelta(days = 1)
    keys, location, base_url = access_config_file()
    structure = "structure=" +'{"date":"date","areaName":"areaName","newCasesByPublishDate":"newCasesByPublishDate","cumCasesByPublishDate":"cumCasesByPublishDate"}'
    filter_england = base_url["filter_en"]+str(yesterday)+'&'
    complete_url = base_url["public_h_eng"] + filter_england + structure
    response = requests.get(complete_url)
    covid_json_england = response.json()
    with open('json_files/public_health_england.json', 'w') as file:
        json.dump(covid_json_england, file, indent=2)
    file.close()
