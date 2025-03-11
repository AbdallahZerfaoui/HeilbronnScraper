from imports import *
from HeilbronnScraper import HeilbronnScraper
from EmailSender import EmailSender
# import asyncio
# import json
# import os
# from time import sleep
# from random import randint
# from datetime import datetime
# from config import MAX_DISTANCE, CONTACTS_FILE, MESSAGE, BASE_DIR, SUBJECT

async def main():
    today = datetime.today().strftime('%Y-%m-%d')
    now = datetime.now()
    id = int(now.strftime('%Y%m%d%H%M'))
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)
    json_filename = f"{BASE_DIR}/heilbronn_{today}_{id}.json"
    scraper = HeilbronnScraper()
    sender = EmailSender()
    try:
        # Fetch valid appointments and related info
        appointments_data, distance, earliest_date = \
            await scraper.get_valid_appointments(today, json_filename, id)
        
        if appointments_data is None:
            return
        
        #fetch appointments
        # appointments = []
        # json_filename = f"{BASE_DIR}/heilbronn_{today}_{earliest_date}_{id}.json"
        # data = await scraper.fetch_appointments_for_date(earliest_date, json_filename)
        # appointments.append(appointments_data)

        #send the answer by email
        # if (distance < MAX_DISTANCE):
        tmp_dict = {today:appointments_data}
        if (appointments_data):
            scraper.tools.save_dict_in_mongo(id, tmp_dict)
        # appointment_time = appointments_data[0]["start"]

        with open(CONTACTS_FILE, "r", encoding="utf-8") as file:
            contacts = file.read().splitlines()

        # subject = SUBJECT
        # with open(MESSAGE, "r", encoding="utf-8") as file:
        #     print(appointment_time)
        #     body = file.read()
        #     body = body.replace("[appointment_time]", appointment_time)
        subject, body = sender.email_builder(today, appointments_data, id)

        for contact in contacts:
            sender.send_email(contact, subject=subject, body=body)
    except Exception as e:
        sender.report_error(e)

if __name__ == "__main__":
    asyncio.run(main())