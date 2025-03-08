from curl_cffi.requests import AsyncSession, BrowserType
import asyncio
import json
import random
import enum
from fake_useragent import UserAgent
from urllib.parse import quote, urlparse, urlunparse
from urllib.parse import unquote
from ScrapingTools import ScrapingTools
from Browser import BrowserType
from config import PROXY_URL

class HeilbronnScraper:
    def __init__(self):
        self.tools = ScrapingTools()  # Initialize the utility class
        self.proxies = {
            "http": PROXY_URL,
            "https": PROXY_URL
        }
        self.session = None

    def choose_impersonate(self):
        """Choose a random browser for the request."""
        available_browsers = [
            # BrowserType.CHROME,
            BrowserType.FIREFOX,
            # BrowserType.EDGE,
            # BrowserType.SAFARI,
        ]
        return random.choice(available_browsers).value

    async def start_session(self):
        """Start a new session."""
        self.session = AsyncSession(
            impersonate=self.choose_impersonate(),
            headers=self.tools.get_random_headers(),
            proxies=self.proxies,
            timeout=30
        )
        check_ip = await self.tools.check_ip(self.session)
        print(f"Server sees fixed IP: {check_ip}")
        


    async def fetch(self, url):
        """Main method to fetch data from Scribd."""
        #url = self.tools.decode_url(url)  # Use ScrapingTools method
        print(url)
        #headers = self.tools.get_random_headers()  # Use ScrapingTools method
        # async with AsyncSession(
        #     impersonate=impersonate,
        #     headers=headers,
        #     proxies=self.proxies,
        #     timeout=30
        # ) as session:
        if not self.session:
            await self.start_session()
        try:
            # ip_check = await session.get("https://httpbin.org/ip")
            # print(f"Server sees IP: {ip_check.json()['origin']}")
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