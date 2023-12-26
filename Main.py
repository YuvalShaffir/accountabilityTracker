import sqlite3
import shutil
import time
import website_predictor
import scrapper
import matplotlib.pyplot as plt


def get_urls():
    url_dict = {}  # Dictionary of URLs and the time spent on each website {URL: Time Spent}
    source_path = 'C:\\Users\\User\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History'
    destination_path = 'E:\\PythonProjects\\Acountability-Tracker'

    shutil.copy(source_path, destination_path)
    con = sqlite3.connect('E:\\PythonProjects\\Acountability-Tracker\\History')
    cursor = con.cursor()
    # Calculate the timestamp for the start of the last day (24 hours ago)
    start_of_last_day = int(time.time()) - 24 * 60 * 60

    # Execute the SQL query to select search history from the last day
    cursor.execute(
        "SELECT urls.url, visits.visit_duration FROM urls, visits WHERE urls.id = visits.url AND urls.last_visit_time >= ?",
        (start_of_last_day,))

    results = cursor.fetchall()
    print(results)
    # Calculate and print the amount of time spent on each site
    for url, visit_duration in results:
        # Convert microseconds to seconds
        time_duration_seconds = visit_duration / 1e6

        # Format the time duration in hours, minutes, and seconds
        formatted_time = time.strftime('%H:%M:%S', time.gmtime(time_duration_seconds))
        # add to the list
        url_dict[url] = formatted_time
        print(f"URL: {url}\nTime Spent: {formatted_time}\n")

    return url_dict


def show_predictions(predictions_dict, url_dict):
    plt.pie([v for v in url_dict.values()], labels=[k for k in predictions_dict.keys()],
            autopct='%1.1f%%')
    plt.savefig('E:\\PythonProjects\\Acountability-Tracker\\website_usage.png', bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    url_dict = get_urls()
    metadata_dict = scrapper.extract_metadata(url_dict)
    predictions_dict = website_predictor.predict(metadata_dict)
    show_predictions(predictions_dict, url_dict)
    # send_pie_chart(predictions_dict, url_dict)