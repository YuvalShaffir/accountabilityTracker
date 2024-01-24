
import sqlite3
import shutil
import os
import time
from urllib.parse import urlparse
import lxml
# import cchardet
from urllib.error import HTTPError


class Scrapper:
    """Scrapper class for scraping the web and translating the content."""

    # ====== Constants ====== #
    DEST_FILE_NAME = 'History'  # the name of the Chrome history file
    DEFAULT_TIME_THRESHOLD = 1000000  # the default time threshold for the history file
    CHROME_PROFILE = 'Default'  # the Chrome profile

    def __init__(self, chrome_profile: str = CHROME_PROFILE
                 , dest_file_name: str = DEST_FILE_NAME,
                 default_time_threshold: float = DEFAULT_TIME_THRESHOLD):

        self._chrome_profile = chrome_profile
        self._dest_file_name = dest_file_name
        self._default_time_threshold = default_time_threshold

    # ====== private Methods ====== #
    def _get_history_file(self) -> str:
        """Returns the path to the Chrome history file."""
        default_profile_path = ''
        if os.name == 'posix':  # Linux or macOS
            default_profile_path = os.path.expanduser("~/config/google-chrome/" + self._chrome_profile + "/"
                                                      + self._dest_file_name)
        elif os.name == 'nt':  # Windows
            default_profile_path = os.path.expandvars(r"%LOCALAPPDATA%/Google/Chrome/User Data/" + self._chrome_profile
                                                      + "/" + self._dest_file_name)

        # Check if the path exists before returning
        if os.path.exists(default_profile_path):
            print("Chrome History file path:", default_profile_path)
            return default_profile_path
        else:
            raise Exception("Path does not exist for profile: " + self._chrome_profile)

    @staticmethod
    def _get_dest_path() -> str:
        """Returns the path to the destination to which we want to copy the Chrome history file to."""
        dest_path = os.path.dirname(os.path.abspath(__file__)) + "/"
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
        print("==== Connected to the database ====")

    def _search_database(self):
        """ Execute the SQL query to select search history from the last day """
        # Calculate the timestamp for the start of the last day (24 hours ago)
        start_of_last_day = int(time.time()) - 24 * 60 * 60

        # Execute the SQL query to select search history from the last day
        self._cursor.execute(
            "SELECT urls.url, visits.visit_duration FROM urls JOIN visits ON urls.id = visits.url WHERE urls.last_visit_time >= ?",
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

    # ====== public Methods ====== #
    def set_chrome_profile(self, chrome_profile: str):
        self._chrome_profile = chrome_profile

    def set_dest_file_name(self, dest_file_name: str):
        self._dest_file_name = dest_file_name

    def set_default_time_threshold(self, default_time_threshold: float):
        self._default_time_threshold = default_time_threshold

    def scrap_history(self):
        """Returns a dictionary of URLs and the time spent on each website {URL: Time Spent}
         from the history of chrome."""

        self._connect_history_file()

        results = self._search_database()

        url_dict = self._fill_url_dict(results)

        # Filter the URLs with time spent less than threshold time in microseconds.
        url_dict_min_time = self._filter_small_duration(url_dict, self._default_time_threshold)

        self._print_url_dict(url_dict_min_time)

        return url_dict_min_time


