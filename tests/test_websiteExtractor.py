from Scrapper.metaExtractor import metaExtractor
import unittest
import asyncio


class TestMetaExtractor(unittest.TestCase):
    def test_get_website_content(self):
        url_dict = {"https://en.wikipedia.org/wiki/Stack_Overflow": 1.33}  # Assuming you have a value associated with the URL
        url_dict = {"https://stackoverflow.com/": 1.33}  # Assuming you have a value associated with the URL

        meta_extractor = metaExtractor(url_dict)
        print((meta_extractor.extract()))
        # Your test logic here


if __name__ == '__main__':
    unittest.main()