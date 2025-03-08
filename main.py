from HeilbronnScraper import HeilbronnScraper
import asyncio
import os
from time import sleep
from random import randint
from datetime import datetime

async def main():
    today = "2025-03-08"
    scraper = HeilbronnScraper()

    json_filename = f"../io/heilbronn_{today}.json"
    if (not os.path.isfile(json_filename)):
        url = scraper.tools.build_dates_url(today)
        data = await scraper.fetch(url)
        if data:
            scraper.tools.save_results(data, json_filename)

    dates = scraper.tools.get_dates(json_filename)
    now = datetime.now()
    id = int(now.strftime('%Y%m%d%H%M'))
    appointments = []
    for date in dates:
        url = scraper.tools.build_appointments_url(date)
        json_filename = f"../io/heilbronn_{today}_{date}.json"
        if (not os.path.isfile(json_filename)):
            data = await scraper.fetch(url)
            if data:
                scraper.tools.save_results(data, json_filename)
                appointments.append(data)
        sleep(randint(50, 300) / 100)
    
    tmp_dict = {today:appointments}
    print(tmp_dict)
    scraper.tools.save_dict_in_mongo(id, tmp_dict)
    

if __name__ == "__main__":
    asyncio.run(main())