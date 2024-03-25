from Scrapper.scrapper import Scrapper


def test_scrap_history():
    s = Scrapper()
    url_dict = s.scrap_history()
    print(url_dict)

