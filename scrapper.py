import cloudscraper
from bs4 import BeautifulSoup
from googletrans import Translator
# from google.cloud import translate

# Create scrapper
scraper = cloudscraper.create_scraper(browser='chrome')
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
}


def get_website_content(website):
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
        translator = Translator()
        # return all_text[0:999]
        translation = translator.translate(all_text[0:999], dest='en').text
        return translation

    except Exception as e:
        print(e)

print(get_website_content("https://www.ynet.co.il"))