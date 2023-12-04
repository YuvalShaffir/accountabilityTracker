import sqlite3
import shutil
import time
import os

shutil.copy(os.path.abspath('Google\\Chrome\\User Data\\Default\\History'), os.path.abspath('Acountability-Tracker'))
con = sqlite3.connect(os.path.abspath('Acountability-Tracker\\History'))
cursor = con.cursor()
# Calculate the timestamp for the start of the last day (24 hours ago)
start_of_last_day = int(time.time()) - 24 * 60 * 60

# Execute the SQL query to select search history from the last day
cursor.execute("SELECT urls.url, visits.visit_duration FROM urls, visits WHERE urls.id = visits.url AND urls.last_visit_time >= ?", (start_of_last_day,))

results = cursor.fetchall()

# Calculate and print the amount of time spent on each site
for url, visit_duration in results:
    # Convert microseconds to seconds
    time_duration_seconds = visit_duration / 1e6

    # Format the time duration in hours, minutes, and seconds
    formatted_time = time.strftime('%H:%M:%S', time.gmtime(time_duration_seconds))

    print(f"URL: {url}\nTime Spent: {formatted_time}\n")