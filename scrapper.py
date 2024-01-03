import cloudscraper
from bs4 import BeautifulSoup
from googletrans import Translator
# import threading
from multiprocessing.pool import Pool
import multiprocessing
import lxml
import cchardet

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121' \
             ' Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
BROWSER = 'chrome'

# create scrapper
scraper = cloudscraper.create_scraper(browser=BROWSER)
headers = {'user-agent': USER_AGENT}


def translate_text(text):
    # Translate the text to English
    try:
        translator = Translator()
        translation = translator.translate(text[0:999], dest='en').text
        return translation

    except Exception as e:
        print(e)


def get_website_content(website) -> str:
    try:
        # sends an HTTP GET request to the specified website. The headers, including the User-Agent,
        # are provided to simulate a request from a specific browser and operating system.
        response = scraper.get(website, headers=headers)

        # The response is parsed using BeautifulSoup, that makes it easier to navigate the HTML document, and extract
        # the information from it.
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the title and description from the HTML document
        title = soup.find('title').text
        description = soup.find('meta', attrs={'name': 'description'})

        # Check if the meta description tag has the 'content' attribute
        if 'content' in str(description):
            description = description.get('content')
        else:
            description = ""

        h1 = soup.find_all('h1')
        h2 = soup.find_all('h2')
        h3 = soup.find_all('h3')
        paragraphs = soup.find_all('p')

        # Extract the text from the h1, h2, and h3 tags
        h1_text = ""
        h2_text = ""
        h3_text = ""
        p_text = ""
        for tag in h1:
            h1_text += tag.text + " "
        for tag in h2:
            h2_text += tag.text + " "
        for tag in h3:
            h3_text += tag.text + " "
        for tag in paragraphs:
            p_text += tag.text + " "

        all_text = (str(title) + " " + str(description) + " " + str(h1_text) + " " + str(h2_text) + " " + str(h3_text)
                    + " " + str(p_text))

        print(all_text[0:999])

        return all_text[0:999]

    except Exception as e:
        print(e)


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
