from Scrapper.metaExtractor import metaExtractor
import unittest
import asyncio

class TestMetaExtractor(unittest.TestCase):
    def test_get_website_content(self):
        url_dict = {"https://edition.cnn.com/": 1.33}  # Assuming you have a value associated with the URL
        meta_extractor = metaExtractor(url_dict)
        print(asyncio.run(meta_extractor.extract()))
        # Your test logic here

if __name__ == '__main__':
    unittest.main()