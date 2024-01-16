# Scrapper\metaExtractor.py

import cloudscraper
from bs4 import BeautifulSoup
import asyncio


class metaExtractor:
    REQUEST_TIMEOUT = 0.001
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121' \
                 ' Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
    BROWSER = 'chrome'

    def __init__(self, url_dict):
        self.url_dict = url_dict
        self._scraper = cloudscraper.create_scraper(browser=metaExtractor.BROWSER)
        self._headers = {'user-agent': metaExtractor.USER_AGENT}

    async def _get_request(self, website):
        # sends an HTTP GET request to the specified website. The headers, including the User-Agent,
        # are provided to simulate a request from a specific browser and operating system.
        try:
            response = self._scraper.get(website, headers=self._headers, timeout=metaExtractor.REQUEST_TIMEOUT)
        except Exception as e:
            print(e)
            response = None
        return response

    async def _get_website_description(self):
        description = self._soup.find('meta', attrs={'name': 'description'})
        # Check if the meta description tag has the 'content' attribute
        if 'content' in str(description):
            description = description.get('content')
        else:
            description = ""

        return description

    async def _get_website_title(self):
        """Extract the title from the HTML document"""
        try:
            title = self._soup.find('title')
            if title is not None:
                return title.text

        except Exception as e:
            print(e)
            return ""

    async def _get_website_text(self, text_type) -> str:
        """Extract the text from the HTML document"""
        try:
            tags = self._soup.find_all(text_type)
            text = ""
            for tag in tags:
                text += tag.text + " "
            return text

        except Exception as e:
            print(e)
            return ""

    async def _create_soup(self):
        # The request is parsed using BeautifulSoup, that makes it easier to navigate the HTML document, and extract
        # the information from it.
        try:
            soup = BeautifulSoup(self._request.text, 'html.parser')
            return soup
        except Exception as e:
            print(e)
            return None

    async def _get_website_content(self, website) -> str:
        try:
            self._request = await self._get_request(website)
            if self._request is None:
                return ""

            self._soup = await self._create_soup()
            if self._soup is None:
                return ""

            title = await self._get_website_title()
            description = await self._get_website_description()

            h1_text = await self._get_website_text('h1')
            h2_text = await self._get_website_text('h2')
            h3_text = await self._get_website_text('h3')
            p_text = await self._get_website_text('p')

            all_text = (str(title) + " " + str(description) + " " + str(h1_text) + " " + str(h2_text) + " "
                        + str(h3_text) + " " + str(p_text))

            return all_text[0:999]

        except Exception as e:
            print(e)
            return ""

    async def extract(self):
        metadata_dict = {}
        metadata_dict = await asyncio.gather(*[self._get_website_content(website) for website in self.url_dict.keys()])

        # with Pool(processes=10) as pool:
        #     metadata_dict = pool.map(self._get_website_content, self.url_dict.keys())

        # threads = []
        # for i in range(10):
        #     x = threading.Thread(target=get_website_content, args=(url_dict[i],))
        #     threads.append(x)
        #     x.start()
        #
        # for index, thread in enumerate(threads):
        #     metadata_dict[url_dict[index]] = thread.join()

        # for url, time_spent in url_dict.items():
        #     metadata_dict[url] = get_website_content(url)
        return metadata_dict
