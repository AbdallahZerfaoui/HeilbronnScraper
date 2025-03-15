from imports import *
from HeilbronnScraper import HeilbronnScraper
from EmailSender import EmailSender
# from AppointmentBooker import AppointmentBooker

async def main():
    today = datetime.today().strftime('%Y-%m-%d')
    now = datetime.now()
    id = int(now.strftime('%Y%m%d%H%M'))
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)
    json_filename = f"{BASE_DIR}/heilbronn_{today}_{id}.json"
    
    scraper = HeilbronnScraper()
    sender = EmailSender()
    # booker = await AppointmentBooker(headless=False)
    try:
        # Fetch valid appointments and related info
        appointments_data, distance = \
            await scraper.get_valid_appointments(today, json_filename, id)
        
        if appointments_data is None:
            return
        
        # Save data in MongoDB
        tmp_dict = {today:appointments_data}
        if (appointments_data):
            scraper.tools.save_dict_in_mongo(id, tmp_dict)
            
		# Read contacts from file
        names, contacts = sender.load_interested_contacts(distance)

		# Send email to each contact

        for fName, contact in zip(names, contacts):
            subject, body = sender.email_builder(today, appointments_data, id, fName)
            sender.send_email(contact, subject=subject, body=body)
    except Exception as e:
        sender.report_error(e)
    # finally:
    #     await booker.close()

if __name__ == "__main__":
    asyncio.run(main())