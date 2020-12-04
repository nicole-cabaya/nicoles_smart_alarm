>>>NAME:
  Covid-19 Smart Alarm System

>>>DESCRIPTION:
  This alarm system is linked to a html template and
  uses APIs from 3 different websites and extracts their corresponding
  json files with the relevant information.
  These json files are then used to display notifications in the webpage
  with information in them. Notifications are displayed on the right side
  of the webpage. We can delete notifications by pressing the x button of
  the target notification. Notifications are scheduled to be regularly
  updated using the "sched" and "time" python modules.

  In this smart alarm we can also set alarms that use the text-to-speech
  module to announce covid rates in Exeter using a json file that contains
  this information.
  Alarms can be set by entering into the label text box in the html.
  Alarms are displayed on the left side of the webpage and can be cancelled
  by pressing the x button of the alarm box.

>>>METADATA:
  Image used in the html: https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.digitaltechnologylabs.com%2F2019%2F06%2F24%2F21-hilarious-coding-memes%2F&psig=AOvVaw0rx_y1T2xJGQFuxqTSOsP5&ust=1607167610287000&source=images&cd=vfe&ved=2ahUKEwi6qKiFnLTtAhXGXxUIHbEWCuAQjRx6BAgAEAc
  APIs used:
    News -- https://newsapi.org/
    weather -- https://openweathermap.org
    Public Health England -- https://publichealthengland.github.io/coronavirus-dashboard-api-python-sdk/

>>>INSTALLATION:
  The Python version that I have used for this project was python 3.9.0.

  Libraries and modules used (some are built in python modules,
  others are installed using pip3):
    date_time
    time
    sched
    logging
    json
    flask
    pyttsx3
    requests

>>>AUTHOR:
  Me - Nicole Cabaya
  Matt Collison - some example code from workshops were used in this project
                including: html template, flask example, and text-to-speech example.
  I have also used stackoverflow and other internet resources
  to help me fix bugs.

>>>LICENSE:
  MIT License -- https://choosealicense.com/licenses/mit/

>>>PROJECT STATUS:
  I did not get to complete the full functionality of this smart alarm.

  Functionality already implemented:
    - be able to display alarms
    - be able to display Notifications
    - be able to extract data from APIs
    - be able to remove alarms from data structure
    - inserted image into html
    - keep logs of events an errors in a log file called 'sys.log'

  Functionality left to implement:
    - cancelling events (alarms)
    - be able to remove Notifications
    - schedule alarms that are set for today and store future alarms in
    a data structure
