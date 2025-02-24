# Python3 script that pulls all FRC registered teams for the current year and
#	writes the full team list to the teamsAll table in the Team 195 DB
# Script is intended to be run once at the beginning of the season. Note that 
#   the script will delete the eventsAll dB table contents. If there are events
#   entered in the events table it will cause an error due to a foreign key
#   constraint on the events table to the eventsAll table

# import statements
import mariadb as mariaDB
import tbapy
import datetime
import re
import sys
import argparse
import configparser

# Define login information for TBA
tba = tbapy.TBA('Tfr7kbOvWrw0kpnVp5OjeY780ANkzVMyQBZ23xiITUkFo9hWqzOuZVlL3Uy6mLrz')
currentYear = datetime.datetime.today().year

# parser to choose the database where the table will be written
parser = argparse.ArgumentParser()
parser.add_argument("-db", "--database", help = "Choices: dev1, dev2, testing, production", required=True)
parser.add_argument("-host", "--host", help = "Host choices: aws, localhost", required=True)
args = parser.parse_args()
input_db = args.database
input_host = args.host

if input_host == "aws":
    server = "scouting.team195.com"
elif input_host == "pi-10":
    server = "10.0.20.195"
elif input_host == "localhost":
    server = "localhost"
else:
    print(input_host + " is not a invalid choice. See --help for choices")
    sys.exit()

# Read the configuration file
config = configparser.ConfigParser()
config.read('../helpers/config.ini')

# Get the database login information from the configuration (ini) file
host = config[input_host+"-"+input_db]['host']
user = config[input_host+"-"+input_db]['user']
passwd = config[input_host+"-"+input_db]['passwd']
database = config[input_host+"-"+input_db]['database']
print(host + " " + user + " " + passwd + " " + database)
conn = mariaDB.connect(user=user, passwd=passwd, host=host, database=database)
cursor = conn.cursor()

def onlyascii(s):
    return "".join(i for i in s if ord(i) < 128 and ord(i) != 39)

def wipeBAE():
        cursor.execute("DELETE FROM eventsAll;")
        cursor.execute("ALTER TABLE eventsAll AUTO_INCREMENT = 1;")
        conn.commit()
wipeBAE() 

totalEvents = tba.events(year=currentYear)
eventList = []

for event in totalEvents:
    eventCode = event.get('event_code')
    eventName = event.get('short_name')
    eventWeek = event.get('week')
    eventCity = event.get('city')
    eventStateProv = event.get('state_prov')
    eventCountry = event.get('country')
    eventLocation = (eventCity + ", " + eventStateProv + ", " + eventCountry)
    eventStartDate = event.get('start_date')
    eventEndDate = event.get('end_date')
    BAEventID = event.get('key')
    
    eventName = onlyascii(eventName)
    eventLocation = onlyascii(eventLocation)

    if len(eventName) > 50:
        eventName = eventName[:40]
    if eventName is None:
    	eventName = "no name"
    eventName = re.sub("[{}]","", eventName)
    eventName = re.sub("[()]","", eventName)
    eventLocation = eventLocation.replace("'","")
    if len(eventCity) > 50:
    	eventCity = eventCity[:40]
    if len(eventCountry) > 50:
    	eventCountry = eventCountry[:40]
    if eventWeek is None:
    	eventWeek = 8
    
    query = "INSERT INTO eventsAll (eventCode, eventName, eventWeek, eventLocation, eventStartDate, eventEndDate, BAEventID) VALUES " + \
            "('" + str(eventCode) + \
            "','" + str(eventName) + \
            "','" + str(eventWeek) + \
            "','" + str(eventLocation) + \
            "','" + str(eventStartDate) + \
            "','" + str(eventEndDate) + \
            "','" + str(BAEventID) + "');"
    print(query)
    
    cursor.execute(query)
    conn.commit()
