from Scrapper.metaExtractor import metaExtractor
from Scrapper.scrapper import Scrapper
import unittest
import asyncio


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


if __name__ == '__main__':
    unittest.main()