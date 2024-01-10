import cloudscraper
from bs4 import BeautifulSoup
from googletrans import Translator
# import threading
import sqlite3
import shutil
from multiprocessing.pool import Pool
import os
import time
from urllib.parse import urlparse
import multiprocessing
import lxml
# import cchardet
from urllib.error import HTTPError


class Scrapper:
    """Scrapper class for scraping the web and translating the content."""

    # ====== Constants ====== #
    REQUEST_TIMEOUT = 0.001
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121' \
                 ' Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
    BROWSER = 'chrome'
    DEST_FILE_NAME = 'History'
    DEFAULT_TIME_THRESHOLD = 1000000
    CHROME_PROFILE = 'Default'

    def __init__(self, chrome_profile: str = CHROME_PROFILE, request_timeout: float = REQUEST_TIMEOUT
                 , user_agent: str = USER_AGENT, browser: str = BROWSER, dest_file_name: str = DEST_FILE_NAME,
                 default_time_threshold: float = DEFAULT_TIME_THRESHOLD):
        self._scraper = cloudscraper.create_scraper(browser=self.BROWSER)
        self._headers = {'user-agent': self.USER_AGENT}
        self._chrome_profile = chrome_profile
        self._request_timeout = request_timeout
        self._user_agent = user_agent
        self._browser = browser
        self._dest_file_name = dest_file_name
        self._default_time_threshold = default_time_threshold

    # todo: getters and setters

    def _get_history_file(self) -> str:
        """Returns the path to the Chrome history file."""
        default_profile_path = ''
        if os.name == 'posix':  # Linux or macOS
            default_profile_path = os.path.expanduser('~/.config/google-chrome/' + self._chrome_profile + '/'
                                                      + self._dest_file_name)
        elif os.name == 'nt':  # Windows
            default_profile_path = os.path.expandvars(r'%LOCALAPPDATA%/Google/Chrome/User Data/' + self._chrome_profile
                                                      + '/'+ self._dest_file_name)

        # Check if the path exists before returning
        if os.path.exists(default_profile_path):
            print("Chrome History file path:", default_profile_path)
            return default_profile_path
        else:
            raise Exception("Path does not exist for profile: " + self._chrome_profile)

    @staticmethod
    def _get_dest_path() -> str:
        """Returns the path to the destination to which we want to copy the Chrome history file to."""
        dest_path = os.path.dirname(os.path.abspath(__file__))
        if os.path.exists(dest_path):
            print("Destination path:", dest_path)
            return dest_path
        else:
            raise Exception("Destination path does not exist")

    def _connect_history_file(self) -> None:
        """Copies the Chrome history file to the destination path (helps to override the premission block of the file).
        Then connects to the database"""
        # copy the file to the destination path
        source_path = self._get_history_file()
        destination_path = self._get_dest_path()
        shutil.copy(source_path, destination_path)

        # connect to the database
        # todo: work on the exception handling
        con = sqlite3.connect(destination_path + self._dest_file_name)
        self._cursor = con.cursor()
        print("-Connected to the database")

    def _search_database(self):
        """ Execute the SQL query to select search history from the last day """
        # Calculate the timestamp for the start of the last day (24 hours ago)
        start_of_last_day = int(time.time()) - 24 * 60 * 60

        # Execute the SQL query to select search history from the last day
        self._cursor.execute(
            "SELECT urls.url, visits.visit_duration FROM urls JOIN visits ON "
            "urls.id = visits.url WHERE urls.last_visit_time >= ?",
            (start_of_last_day,))

        results = self._cursor.fetchall()
        return results

    @staticmethod
    def _clean_url(url):
        """ Remove the query and fragment parts of the URL"""
        url = urlparse(url)._replace(path='')._replace(fragment="")._replace(query='').geturl()
        return url

    @staticmethod
    def _get_formatted_time(visit_duration):
        """Calculate the formatted time of type Hours:Minutes:Seconds"""
        # Convert microseconds to seconds
        time_duration_seconds = visit_duration / 1e6
        # Format the time duration in hours, minutes, and seconds
        formatted_time = time.strftime('%H:%M:%S', time.gmtime(time_duration_seconds))
        return formatted_time

    @staticmethod
    def _filter_small_duration(url_dict, threshold_time):
        """Filter the URLs with time spent less than threshold time in microseconds"""
        url_dict_min_time = {u: v for u, v in url_dict.items() if v > threshold_time}
        return url_dict_min_time

    def _fill_url_dict(self, results):
        """Fill the dictionary with URLs and the time spent on each website {URL: Time Spent}"""
        url_dict = {}  # Dictionary of URLs and the time spent on each website {URL: Time Spent}
        for url, visit_duration in results:
            url = self._clean_url(url)

            if url not in url_dict:
                url_dict[str(url)] = visit_duration
            else:
                url_dict[str(url)] += visit_duration

        return url_dict

    def _print_url_dict(self, url_dict_min_time):
        for url, visit_duration in url_dict_min_time.items():
            formatted_time = self._get_formatted_time(visit_duration)
            print(f"URL: {url}\nTime Spent: {formatted_time}\n")

    def get_urls(self):
        """Returns a dictionary of URLs and the time spent on each website {URL: Time Spent}
         from the history of chrome."""

        self._connect_history_file()

        results = self._search_database()

        url_dict = self._fill_url_dict(results)

        # Filter the URLs with time spent less than threshold time in microseconds.
        url_dict_min_time = self._filter_small_duration(url_dict, self._default_time_threshold)

        self._print_url_dict(url_dict_min_time)

        return url_dict_min_time


def translate_text(text):
    # Translate the text to English
    try:
        translator = Translator()
        translation = translator.translate(text[0:999], dest='en').text
        return translation

    except Exception as e:
        print(e)


def get_request(website):
    # sends an HTTP GET request to the specified website. The headers, including the User-Agent,
    # are provided to simulate a request from a specific browser and operating system.
    try:
        response = scraper.get(website, headers=headers, timeout=REQUEST_TIMEOUT)
    except Exception as e:
        print(e)
        response = None
    return response


def get_website_description(soup):
    description = soup.find('meta', attrs={'name': 'description'})
    # Check if the meta description tag has the 'content' attribute
    if 'content' in str(description):
        description = description.get('content')
    else:
        description = ""

    return description


def get_website_title(soup):
    """Extract the title from the HTML document"""
    try:
        title = soup.find('title')
        if title is not None:
            return title.text

    except Exception as e:
        print(e)
        return ""


def get_website_text(text_type, soup) -> str:
    """Extract the text from the HTML document"""
    try:
        tags = soup.find_all(text_type)
        text = ""
        for tag in tags:
            text += tag.text + " "
        return text

    except Exception as e:
        print(e)
        return ""


def create_soup(request):
    # The request is parsed using BeautifulSoup, that makes it easier to navigate the HTML document, and extract
    # the information from it.
    try:
        soup = BeautifulSoup(request.text, 'html.parser')
        return soup
    except Exception as e:
        print(e)
        return None


def get_website_content(website) -> str:
    try:
        request = get_request(website)
        if request is None:
            return ""

        soup = create_soup(request)
        if soup is None:
            return ""

        title = get_website_title(soup)
        description = get_website_description(soup)

        h1_text = get_website_text('h1', soup)
        h2_text = get_website_text('h2', soup)
        h3_text = get_website_text('h3', soup)
        p_text = get_website_text('p', soup)

        all_text = (str(title) + " " + str(description) + " " + str(h1_text) + " " + str(h2_text) + " " + str(h3_text)
                    + " " + str(p_text))

        return all_text[0:999]

    except Exception as e:
        print(e)
        return ""


def extract_metadata(url_dict) -> dict:
    metadata_dict = {}

    with Pool(processes=10) as pool:
        metadata_dict = pool.map(get_website_content, url_dict.keys())

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
