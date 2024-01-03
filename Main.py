import sqlite3
import shutil
import time
from urllib.parse import urlparse
# import website_predictor
import os
import scrapper
import matplotlib.pyplot as plt

# The default Chrome profile name, if you have multiple profiles,
# change this to the name of the profile you want to use.
DEFAULT_TIME_THRESHOLD = 1000000
CHROME_PROFILE = 'Default'
DEST_FILE_NAME = 'History'


def get_history_file(profile=CHROME_PROFILE):
    """Returns the path to the Chrome history file.
    @param profile: Name of the chrome Profile, profile = 'Default'.
    example: get_history_file('Profile 1')"""
    default_profile_path = ''
    if os.name == 'posix':  # Linux or macOS
        default_profile_path = os.path.expanduser('~/.config/google-chrome/'+profile+'/History')
    elif os.name == 'nt':  # Windows
        default_profile_path = os.path.expandvars(r'%LOCALAPPDATA%/Google/Chrome/User Data/'+profile+'/History')

    # Check if the path exists before returning
    if os.path.exists(default_profile_path):
        print("Chrome History file path:", default_profile_path)
        return default_profile_path
    else:
        raise Exception("Path does not exist for profile: "+profile)


def get_dest_path():
    """Returns the path to the destination to which we want to copy the Chrome history file to."""
    dest_path = os.path.dirname(os.path.abspath(__file__))
    if os.path.exists(dest_path):
        print("Destination path:", dest_path)
        return dest_path
    else:
        raise Exception("Destination path does not exist")


def connect_history_file():
    """Copies the Chrome history file to the destination path (helps to override the premission block of the file).
    Then connects to the database and returns the cursor."""
    # copy the file to the destination path
    source_path = get_history_file()
    destination_path = get_dest_path()
    shutil.copy(source_path, destination_path)

    # connect to the database
    con = sqlite3.connect(destination_path + DEST_FILE_NAME)
    cursor = con.cursor()
    return cursor


def search_database(cursor):
    """ Execute the SQL query to select search history from the last day """
    # Calculate the timestamp for the start of the last day (24 hours ago)
    start_of_last_day = int(time.time()) - 24 * 60 * 60

    # Execute the SQL query to select search history from the last day
    cursor.execute(
        "SELECT urls.url, visits.visit_duration FROM urls JOIN visits ON urls.id = visits.url WHERE urls.last_visit_time >= ?",
        (start_of_last_day,))

    results = cursor.fetchall()
    return results


def clean_url(url):
    """ Remove the query and fragment parts of the URL"""
    url = urlparse(url)._replace(path='')._replace(fragment="")._replace(query='').geturl()
    return url


def get_formatted_time(visit_duration):
    """Calculate the formatted time of type Hours:Minutes:Seconds"""
    # Convert microseconds to seconds
    time_duration_seconds = visit_duration / 1e6
    # Format the time duration in hours, minutes, and seconds
    formatted_time = time.strftime('%H:%M:%S', time.gmtime(time_duration_seconds))
    return formatted_time


def filter_small_duration(url_dict, threshold_time):
    """Filter the URLs with time spent less than threshold time in microseconds"""
    url_dict_min_time = {u: v for u, v in url_dict.items() if v > threshold_time}
    return url_dict_min_time


def fill_url_dict(results):
    """Fill the dictionary with URLs and the time spent on each website {URL: Time Spent}"""
    url_dict = {}  # Dictionary of URLs and the time spent on each website {URL: Time Spent}
    for url, visit_duration in results:
        url = clean_url(url)

        if url not in url_dict:
            url_dict[str(url)] = visit_duration
        else:
            url_dict[str(url)] += visit_duration

    return url_dict


def print_url_dict(url_dict_min_time):
    for url, visit_duration in url_dict_min_time.items():
        formatted_time = get_formatted_time(visit_duration)
        print(f"URL: {url}\nTime Spent: {formatted_time}\n")


def get_urls():
    """Returns a dictionary of URLs and the time spent on each website {URL: Time Spent}  from the history of chrome."""
    cursor = connect_history_file()

    results = search_database(cursor)

    url_dict = fill_url_dict(results)

    # Filter the URLs with time spent less than threshold time in microseconds.
    url_dict_min_time = filter_small_duration(url_dict, DEFAULT_TIME_THRESHOLD)

    print_url_dict(url_dict_min_time)

    return url_dict_min_time


def show_predictions(predictions_dict, url_dict):
    plt.pie([v for v in url_dict.values()], labels=[k for k in predictions_dict.keys()],
            autopct='%1.1f%%')
    plt.savefig('E:\\PythonProjects\\Acountability-Tracker\\website_usage.png', bbox_inches='tight')
    plt.show()


def main():
    """Main function"""
    get_dest_path()
    # url_dict = get_urls()
    # metadata_dict = scrapper.extract_metadata(url_dict)
    # print(metadata_dict)
    # predictions_dict = website_predictor.predict(metadata_dict)
    # show_predictions(predictions_dict, url_dict)
    # send_pie_chart(predictions_dict, url_dict)


if __name__ == '__main__':
    main()
