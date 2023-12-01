import sqlite3
import shutil

shutil.copy('C:\\Users\\yshaf\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History', 'C:\\Users\\yshaf\\PycharmProjects\\Acountability-Tracker')
con = sqlite3.connect('C:\\Users\\yshaf\\PycharmProjects\\Acountability-Tracker\\History')
cursor = con.cursor()
cursor.execute("SELECT url FROM urls")
urls = cursor.fetchall()
# Access the first element of each tuple before joining
formatted_urls = '\n'.join(url[0] for url in urls)
print(formatted_urls)