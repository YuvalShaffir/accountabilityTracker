import cloudscraper
from bs4 import BeautifulSoup
from googletrans import Translator
# import threading
from multiprocessing.pool import Pool
import multiprocessing
import lxml
import cchardet
from urllib.error import HTTPError

REQUEST_TIMEOUT = 0.001

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
