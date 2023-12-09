import sqlite3
import shutil
import time
import os
from urllib.parse import urlsplit
import matplotlib.pyplot as plt

SOURCE_PATH = 'C:\\Users\\yshaf\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History'
DESTINATION_PATH = 'C:\\Users\\yshaf\\PycharmProjects\\Acountability-Tracker'
SQL_QUERY = "SELECT urls.url, visits.visit_duration FROM urls, visits WHERE urls.id = " \
            "visits.url AND urls.last_visit_time >= ?"


def get_history():
    """Copies the Chrome history file and connects to the copied file."""
    shutil.copy(SOURCE_PATH, DESTINATION_PATH)
    con = sqlite3.connect(os.path.join(DESTINATION_PATH, 'History'))
    cursor = con.cursor()

    # Calculate the timestamp for the start of the last day (24 hours ago)
    start_of_last_day = int(time.time()) - 24 * 60 * 60

    # Execute the SQL query to select search history from the last day
    cursor.execute(SQL_QUERY, (start_of_last_day,))
    results = cursor.fetchall()
    return results


def print_results(results):
    """Prints the results of the history file."""
    # Calculate and print the amount of time spent on each site
    for url, visit_duration in results.items():
        print(f"URL: {url}\nTime Spent: {time.strftime('%H:%M:%S', time.gmtime(visit_duration / 1e6))}\n")


def clean_results(results):
    """Cleans the results of the history file.
    Removes https://, www., and .com from the URL."""
    cleaned_results = {}

    for url, visit_duration in results:
        # Use urlsplit to parse the URL
        parsed_url = urlsplit(url)

        # Extract the netloc (domain) from the parsed URL
        site_name = parsed_url.netloc

        # Add the cleaned URL and visit duration to the dictionary
        if site_name not in cleaned_results.keys():
            cleaned_results[site_name] = visit_duration
        else:
            cleaned_results[site_name] += visit_duration

    return cleaned_results


def analyze_history(categories, results):
    """Analyzes the history file and returns the amount of time spent on each category."""
    pass


def create_pie_chart(results):
    """Creates a pie chart of the time spent on each site."""
    labels = list(results.keys())
    sizes = list(results.values())

    # Plotting the pie chart
    plt.pie(sizes, labels=None, autopct='%1.1f%%', startangle=140)

    # Adding a legend with site name - duration percentage
    legend_labels = [f"{label} - {size:.1f}%" for label, size in zip(labels, sizes)]
    plt.legend(legend_labels, loc="best", bbox_to_anchor=(1, 0.5))

    # Equal aspect ratio ensures that the pie chart is circular.
    plt.axis('equal')

    # Display the pie chart
    plt.show()


def send_message():
    pass


def main():
    """Main function."""
    results = get_history()
    results = clean_results(results)
    # print_results(results)
    categories = ['Social Media', 'Entertainment', 'News', 'Shopping', 'Other', 'School', 'Work']
    # analyze_history(categories, results)
    create_pie_chart(results)
    # send_message()


if __name__ == '__main__':
    main()