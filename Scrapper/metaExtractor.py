# Scrapper\metaExtractor.py

import cloudscraper
from bs4 import BeautifulSoup
import asyncio
from tqdm import tqdm
from Utils.utils import get_website_name


class metaExtractor:
    """
    metaExtractor class for extracting the meta data from the web.

    Args:
        url_dict (dict): a dictionary of the form {url: time_threshold} where url is the url of the website and

    """

    # ====== Constants ====== #
    REQUEST_TIMEOUT = 30
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121' \
                 ' Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
    BROWSER = 'chrome'
    WIKIPEDIA_URL = 'https://en.wikipedia.org/wiki/'
    FORBIDDEN_ACCESS_LIST = ['forbidden access', '403 forbidden', '403 error', 'forbidden']

    def __init__(self, url_dict):
        self.url_dict = url_dict
        self._scraper = cloudscraper.create_scraper(browser=metaExtractor.BROWSER)
        self._headers = {'user-agent': metaExtractor.USER_AGENT}

    def _get_request(self, website):
        """
        sends an HTTP GET request to the specified website. The headers, including the User-Agent,
        are provided to simulate a request from a specific browser and operating system.
        @:param website: the website to send the request to.
        @:returns: the request from the website.
        """
        try:
            request = self._scraper.get(website, headers=self._headers, timeout=metaExtractor.REQUEST_TIMEOUT)
        except Exception as e:
            print(e)
            request = None
        return request

    def _get_website_description(self) -> str:
        """
        @:param website: the website to extract the description from.
        @:returns description: the description of the website.
        """
        description = self._soup.find('meta', attrs={'name': 'description'})
        # Check if the meta description tag has the 'content' attribute
        if 'content' in str(description):
            description = description.get('content')
        else:
            description = ""

        return description

    def _get_website_title(self) -> str:
        """Extract the title from the HTML document"""
        try:
            title = self._soup.find('title')
            if title is not None:
                return title.text

        except Exception as e:
            print(e)
            return ""

    def _get_website_text(self, text_type) -> str:
        """
        Extract the text from the HTML document
        Args:
            @:param text_type: The type of text to be extracted from the HTML document.
        @:returns text: The text extracted from the HTML document.
        """
        try:
            tags = self._soup.find_all(text_type)
            text = ""
            for tag in tags:
                text += tag.text + " "
            return text

        except Exception as e:
            print(e)
            return ""

    def _create_soup(self):
        """
        The request is parsed using BeautifulSoup, that makes it easier to navigate the HTML document, and extract
        the information from it.
        """
        try:
            soup = BeautifulSoup(self._request.text, 'html.parser')
            return soup
        except Exception as e:
            print(e)
            return None

    def _check_forbidden_access(self, metadata: str) -> str:
        """
        Checks for metadata that has 'forbidden access' in it, and then makes a new search using wikipedia.
        Args:
            @:param metadata: The metadata extracted from the HTML document.
        @:returns metadata: The metadata extracted from the HTML document, or from the wikipedia page of that site.
        """
        for forbidden_access in metaExtractor.FORBIDDEN_ACCESS_LIST:
            if forbidden_access in metadata.lower():
                website_title = get_website_name(self._request.url)
                metadata = self._get_website_content(metaExtractor.WIKIPEDIA_URL + website_title)
                break

        return metadata

    def _get_website_content(self, website: str) -> str:
        """
        Extracts the metadata from the HTML document.
        Args:
            @:param website: The URL of the website to be parsed.
        @:returns: The metadata extracted from the HTML document.
        """
        try:
            self._request = self._get_request(website)
            if self._request is None:
                return ""

            self._soup = self._create_soup()
            if self._soup is None:
                return ""

            title = self._get_website_title()
            description = self._get_website_description()

            h1_text = self._get_website_text('h1')
            h2_text = self._get_website_text('h2')
            h3_text = self._get_website_text('h3')
            p_text = self._get_website_text('p')

            all_text = (str(title) + " " + str(description) + " " + str(h1_text) + " " + str(h2_text) + " "
                        + str(h3_text) + " " + str(p_text))

            all_text = self._check_forbidden_access(all_text)

            return all_text[0:999]

        except Exception as e:
            print(e)
            return ""

    def extract(self):
        """
        Extracts the metadata from a dictionary of websites {{website : duration}}.
        Args:
            @:param: A dictionary of websites {{website : duration}}.
        @:returns: A dictionary of websites with metadata {{website : metadata}}.
        """
        metadata_dict = {website: self._get_website_content(website) for website in tqdm(self.url_dict.keys())}
        return {k: v for k, v in metadata_dict.items() if v != ""}  # remove empty metadata
