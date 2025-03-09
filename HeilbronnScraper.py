from imports import *
from ScrapingTools import ScrapingTools
from Browser import BrowserType
# from curl_cffi.requests import AsyncSession, BrowserType
# import asyncio
# import json
# import random
# import enum
# import os
# from fake_useragent import UserAgent
# from urllib.parse import quote, urlparse, urlunparse
# from urllib.parse import unquote
# from config import PROXY_URL, TIMEOUT, BASE_DIR, MAX_DISTANCE

class HeilbronnScraper:
    def __init__(self):
        self.base_dir = BASE_DIR
        self.tools = ScrapingTools()
        self.proxies = {
            "http": PROXY_URL,
            "https": PROXY_URL
        }
        self.session = None

    def choose_impersonate(self):
        """Choose a random browser for the request."""
        available_browsers = [
            BrowserType.CHROME,
            BrowserType.FIREFOX,
            BrowserType.EDGE,
            BrowserType.SAFARI,
        ]
        return random.choice(available_browsers).value

    async def start_session(self):
        """Start a new session."""
        self.session = AsyncSession(
            impersonate=self.choose_impersonate(),
            headers=self.tools.get_random_headers(),
            proxies=self.proxies,
            timeout=TIMEOUT,
        )
        check_ip = await self.tools.check_ip(self.session)
        print(f"Server sees fixed IP: {check_ip}")
        

    async def fetch(self, url):
        """Main method to fetch data from Scribd."""
        print(url)
        if not self.session:
            await self.start_session()
        try:
            response = await self.session.get(url)
            if response.status_code in [403, 429]:
                print(f"Blocked - Status Code: {response.status_code}")
                return None

            data = response.json() if 'application/json' in response.headers.get('content-type', '') else response.text
            #self.tools.save_results(data)  # Use ScrapingTools method
            return data

        except Exception as e:
            print(f"Request failed: {str(e)}")
            return None
        
    async def fetch_dates(self, today, json_filename):
        """Fetch dates and save the results."""
        url = self.tools.build_dates_url(today)
        if not os.path.isfile(json_filename):
            data = await self.fetch(url)
            if data:
                self.tools.save_results(data, json_filename)
        dates = self.tools.get_dates(json_filename)
        return dates

    async def fetch_appointments_for_date(self, date, json_filename):
        """Fetch appointments for a specific date and save the results."""
        url = self.tools.build_appointments_url(date)
        if not os.path.isfile(json_filename):
            data = await self.fetch(url)
            if data:
                self.tools.save_results(data, json_filename)
                return data
        else:
            with open(json_filename, "r", encoding="utf-8") as file:
                return json.load(file)
            
    async def get_valid_appointments(self, today, json_filename, id):
        """Orchestrate date and appointment fetching.
        Returns (appointments_data, distance, earliest_date)."""
        dates = await self.fetch_dates(today, json_filename)
        if not dates:
            return None, None, None
        earliest_date = dates[0]
        distance = self.tools.get_distance_date(earliest_date, today)
        if distance > MAX_DISTANCE:
            print(f"Earliest date {earliest_date} is over {MAX_DISTANCE} days away.")
            return None, None, None
        json_filename = f"{BASE_DIR}/heilbronn_{today}_{earliest_date}_{id}.json"
        appointments_data = await self.fetch_appointments_for_date(earliest_date, json_filename)
        return appointments_data, distance, earliest_date