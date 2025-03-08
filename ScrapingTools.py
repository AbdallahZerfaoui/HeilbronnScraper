from curl_cffi.requests import AsyncSession, BrowserType
import asyncio
import json
import random
import enum
from fake_useragent import UserAgent
from urllib.parse import quote, urlparse, urlunparse
from urllib.parse import unquote
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from config import MONGO_URI


class ScrapingTools:
    @staticmethod
    def get_random_headers():
        """Generate random headers for requests."""
        return {
            "User-Agent": UserAgent().chrome,
            'Accept': 'application/json, text/plain',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Referer': 'https://www.qtermin.de/qtermin-stadtheilbronn-abh?lang=en',
            'Pragma': 'no-cache',
            'Content-Type': 'application/json',
            'webid': 'qtermin-stadtheilbronn-abh',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Priority': 'u=0',
            'Cache-Control': 'no-cache',
            'TE': 'trailers'
        }
    @staticmethod
    def build_dates_url(today):
        url = f"https://www.qtermin.de/api/timeslots?date={today}&serviceid=144511&rangesearch=1&caching=false&capacity=1&duration=20&cluster=false&slottype=0&fillcalendarstrategy=0&showavcap=false&appfuture=270&appdeadline=480&appdeadlinewm=1&oneoff=null&msdcm=0&calendarid="
        return url
    
    @staticmethod
    def build_appointments_url(date):
        url = f"https://www.qtermin.de/api/timeslots?date={date}&serviceid=144511&capacity=1&caching=false&duration=20&cluster=false&slottype=0&fillcalendarstrategy=0&showavcap=false&appfuture=270&appdeadline=480&msdcm=0&oneoff=null&appdeadlinewm=1&tz=W.%20Europe%20Standard%20Time&tzaccount=W.%20Europe%20Standard%20Time&calendarid="
        return url

    @staticmethod
    def decode_url(url):
        """Decode a URL-encoded string."""
        return unquote(url)

    @staticmethod
    def save_results(data, filename):
        """Save scraped data to a JSON file."""
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)
        print(f"Data saved to {filename}")

    @staticmethod
    async def check_ip(session):
        """
        Check the IP address being used by the session.
        :param session: An AsyncSession object.
        :return: IP address as a string.
        """
        try:
            response = await session.get("https://httpbin.org/ip")
            ip_data = response.json()
            return ip_data.get("origin", "Unknown IP")
        except Exception as e:
            print(f"Failed to check IP: {str(e)}")
            return None

    @staticmethod
    def save_in_mongo(id, filename):
        """Save the JSON file in MongoDB."""
        uri = MONGO_URI
        cluster = MongoClient(uri, server_api=ServerApi('1'))
        try:
            cluster.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)
        db = cluster["heilbronn_db"]
        collection = db["appointments"]
        data = json.load(open(filename))
        collection.insert_one({"_id": id, "data": data})

    @staticmethod
    def save_dict_in_mongo(id, dict):
        """Save the DICT file in MongoDB."""
        uri = MONGO_URI
        cluster = MongoClient(uri, server_api=ServerApi('1'))
        try:
            cluster.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)
        db = cluster["heilbronn_db"]
        collection = db["appointments"]
        collection.insert_one({"_id": id, "data": dict})
        print("data added successfuly !!")
    
    def get_dates(self, json_file):
        dates=[]
        with open(json_file, "r", encoding="utf-8") as file:
            data = json.load(file)
        for elem in data:
            raw_date = elem["start"]
            dates.append(self.extract_date(raw_date))

        return dates
        
    @staticmethod
    def extract_date(datetime_str):
        return datetime_str.split('T')[0]
    