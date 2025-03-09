from HeilbronnScraper import HeilbronnScraper
from EmailSender import EmailSender
import asyncio
import json
import os
from time import sleep
from random import randint
from datetime import datetime
from config import MAX_DISTANCE, CONTACTS_FILE, MESSAGE, BASE_DIR, SUBJECT

async def main():
    today = datetime.today().strftime('%Y-%m-%d')
    now = datetime.now()
    id = int(now.strftime('%Y%m%d%H%M'))
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)
    json_filename = f"{BASE_DIR}/heilbronn_{today}_{id}.json"
    scraper = HeilbronnScraper()
    sender = EmailSender()
    #fetch dates
    if (not os.path.isfile(json_filename)):
        url = scraper.tools.build_dates_url(today)
        data = await scraper.fetch(url)
        if data:
            scraper.tools.save_results(data, json_filename)

    dates = scraper.tools.get_dates(json_filename)
    # for date in dates:
    date = dates[0]
    print(date)
    distance = scraper.tools.get_distance_date(date, today)
    if (distance > MAX_DISTANCE):
        print(f"The earliest date is {date} which is more than {MAX_DISTANCE} days away")
        return
    #fetch appointments
    appointments = []
    json_filename = f"{BASE_DIR}/heilbronn_{today}_{date}_{id}.json"
    data = await scraper.fetch_appointments_for_date(date, json_filename)
    appointments.append(data)
    # sleep(randint(50, 300) / 100)

    # now = datetime.now()
    # id = int(now.strftime('%Y%m%d%H%M'))
    #send the answer by email
    if (distance < MAX_DISTANCE):
        tmp_dict = {today:appointments}
        if (appointments):
            scraper.tools.save_dict_in_mongo(id, tmp_dict)
        appointment_time = data[0]["start"]

        with open(CONTACTS_FILE, "r", encoding="utf-8") as file:
            contacts = file.read().splitlines()
        
        subject = SUBJECT
        with open(MESSAGE, "r", encoding="utf-8") as file:
            print(appointment_time)
            body = file.read()
            body = body.replace("[appointment_time]", appointment_time)
        
        for contact in contacts:
            sender.send_email(contact, subject=subject, body=body)

    
if __name__ == "__main__":
    asyncio.run(main())