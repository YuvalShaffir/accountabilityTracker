from ...Acountability-Tracker.Scrapper import metaExtractor
import unittest


class TestMetaExtractor(unittest.TestCase):
    def test_get_website_content(self):
        url_dict = {"https://www.cnn.com": 1.33}  # Assuming you have a value associated with the URL
        meta_extractor = metaExtractor(url_dict)

        # Your test logic here

if __name__ == '__main__':
    unittest.main()