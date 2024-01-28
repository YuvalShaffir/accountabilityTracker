from Scrapper.metaExtractor import metaExtractor
from Scrapper.scrapper import Scrapper
import unittest
import asyncio
from unittest.mock import patch
import pickle  # TODO: save the metadata dictionary to a file


class TestMetaExtractor(unittest.IsolatedAsyncioTestCase):

    async def test_forbidden_access_website_content(self):
        """I expect that it will return a wikipedia page of that website, because the website is forbidden access."""
        url_dict = {"https://stackoverflow.com/": 1.33}  # Assuming you have a value associated with the URL
        meta_extractor = metaExtractor(url_dict)
        print((await meta_extractor.extract()))

    @patch('Scrapper.metaExtractor.metaExtractor._get_website_content', return_value="This is a test")
    async def test_dict_meta(self):
        url_dict = Scrapper().scrap_history()
        meta_extractor = metaExtractor(url_dict)
        print(await meta_extractor.extract())


if __name__ == '__main__':
    unittest.main()