from Scrapper.metaExtractor import metaExtractor
import unittest
import asyncio


class TestMetaExtractor(unittest.TestCase):
    def test_forbidden_access_website_content(self):
        url_dict = {"https://stackoverflow.com/": 1.33}  # Assuming you have a value associated with the URL
        meta_extractor = metaExtractor(url_dict)
        print((meta_extractor.extract()))


if __name__ == '__main__':
    unittest.main()