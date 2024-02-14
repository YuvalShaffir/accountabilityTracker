from unittest.mock import patch

from Scrapper.metaExtractor import metaExtractor
from Scrapper.scrapper import Scrapper
import unittest

URL_KEY = "https://www.ynet.co.il"
TEXT_TO_TRANSLATE = "אני אוהב אוכל"
TRANSLATION_TEST = "I love food"
TRASH_VALUE = 1.33


class TestMetaExtractor(unittest.TestCase):
    def test_forbidden_access_website_content(self):
        """I expect that it will return a wikipedia page of that website, because the website is forbidden access."""
        url_dict = {"https://stackoverflow.com/": 1.33}  # Assuming you have a value associated with the URL
        meta_extractor = metaExtractor(url_dict)
        print((meta_extractor.extract()))

    def test_dict_meta(self):
        url_dict = Scrapper().scrap_history()
        meta_extractor = metaExtractor(url_dict)
        print(meta_extractor.extract())

    @patch('Scrapper.metaExtractor.metaExtractor._check_forbidden_access', return_value=TEXT_TO_TRANSLATE)
    def test_translate_text(self, mock_check_forbidden_access):
        """ Check if the website is translated to English. """
        url_dict = {URL_KEY: TRASH_VALUE}
        meta_extractor = metaExtractor(url_dict)
        res = meta_extractor.extract()[URL_KEY]
        print(res)
        # print(res.replace('"', ''))
        assert (res == TRANSLATION_TEST)


if __name__ == '__main__':
    unittest.main()
