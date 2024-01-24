from Scrapper.scrapper import Scrapper


class testScrapper():
    def __init__(self):
        pass

    def test_scrap_history(self):
        s = Scrapper()
        url_dict = s.scrap_history()
        print(url_dict)

        
if __name__ == '__main__':
    testScrapper().test_scrap_history()