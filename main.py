import asyncio
import csv
from datetime import datetime
import requests
import re
from bs4 import BeautifulSoup
import os

FILENAME = "data.csv"
HEADER = ['ID','Time','Station','Available Bikes','Available Shelters']
TIMESPAN = 10 #in minutes
STATION_NAME = "Rovetta"
URL ="https://bicimia.bresciamobilita.it/frmLeStazioni.aspx"
actual_id = -1

class Station:
    def __init__(self, id_val, name, time, bikes, shelters):
        self.id_val = id_val
        self.name = name
        self.time = time
        self.bikes = bikes
        self.shelters = shelters

def get_station(name):
    global actual_id
    time = datetime.now()

    #Get the response from URL
    resp = requests.get(URL)
    soup = BeautifulSoup(resp.content, "html.parser")
    station = soup.find(class_="Stazione", string=name)

    # Get the status of the given station
    station_div = station.find_parents("div")[0]
    temp_str = station_div.find(class_="Red").text
    nums = re.findall(r'\d+', temp_str)
    bikes = nums[0]
    shelters = nums[1]

    return Station(id_val=actual_id, name=name, time=time, bikes=bikes, shelters=shelters)

async def task_data_coroutine(_minutes):
    global actual_id
    while True:
        #Get the station
        station = get_station(name=STATION_NAME)

        #Open the CSV file
        data = [str(station.id_val), str(station.time), str(station.name), str(station.bikes), str(station.shelters)]
        with open(FILENAME, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)
            file.close()

        actual_id += 1
        await asyncio.sleep(delay=_minutes*60)

def find_files(filename, search_path):
   result = []
   for root, dir, files in os.walk(search_path):
      if filename in files:
         result.append(os.path.join(root, filename))
   return result

async def main():
    global actual_id
    # Open the csv file
    result = find_files(FILENAME, "..\statistic_bicimia")
    if not result: #the file does not exist, so create it and format it
        with open(FILENAME, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(HEADER)
            file.close()
        actual_id = 1
    else:
        #Get the actual number of rows
        with open(FILENAME, 'r') as file:
            rows = csv.reader(file)
            for row in rows:
                actual_id += 1
            file.close()

    # Set the loop task
    task_data = asyncio.create_task(task_data_coroutine(TIMESPAN), name="GetDataTask")
    #task_network = asyncio.create_task(task_network_coroutine(TIMESPAN/2), name="NetInfoTask")
    await task_data

asyncio.run(main())