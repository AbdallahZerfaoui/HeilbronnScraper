from HeilbronnScraper import HeilbronnScraper
from EmailSender import EmailSender
import asyncio
import json
import os
from time import sleep
from random import randint
from datetime import datetime
from config import MAX_DISTANCE, CONTACTS_FILE, MESSAGE

async def main():
    today = datetime.today().strftime('%Y-%m-%d')
    json_filename = f"../io/heilbronn_{today}.json"
    scraper = HeilbronnScraper()
    sender = EmailSender()
    #fetch dates
    if (not os.path.isfile(json_filename)):
        url = scraper.tools.build_dates_url(today)
        data = await scraper.fetch(url)
        if data:
            scraper.tools.save_results(data, json_filename)

    dates = scraper.tools.get_dates(json_filename)
    now = datetime.now()
    id = int(now.strftime('%Y%m%d%H%M'))
    appointments = []
    # for date in dates:
    date = dates[0]
    print(date)
    json_filename = f"../io/heilbronn_{today}_{date}.json"
    distance = scraper.tools.get_distance_date(date, today)
    # url = scraper.tools.build_appointments_url(date)
    # if (not os.path.isfile(json_filename)):
    #     data = await scraper.fetch(url)
    #     if data:
    #         scraper.tools.save_results(data, json_filename)
    #         appointments.append(data)
    # else:
    #     with open(json_filename, "r", encoding="utf-8") as file:
    #         data = json.load(file)
    data = await scraper.fetch_appointments_for_date(date, json_filename)
    appointments.append(data)
    # sleep(randint(50, 300) / 100)

    #send the answer by email
    if (distance < MAX_DISTANCE):
        tmp_dict = {today:appointments}
        if (appointments):
            scraper.tools.save_dict_in_mongo(id, tmp_dict)
        appointment_time = data[0]["start"]

        with open(CONTACTS_FILE, "r", encoding="utf-8") as file:
            contacts = file.read().splitlines()
        
        subject = "Your appointment"
        with open(MESSAGE, "r", encoding="utf-8") as file:
            print(appointment_time)
            body = file.read()
            body = body.replace("[appointment_time]", appointment_time)
        
        for contact in contacts:
            sender.send_email(contact, subject=subject, body=body)
    
if __name__ == "__main__":
    asyncio.run(main())