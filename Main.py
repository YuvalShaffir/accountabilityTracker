from Scrapper.scrapper import Scrapper
from Scrapper.metaExtractor import metaExtractor
from websitePredictor.websitePredictor import websitePredictor
import asyncio

async def main():
    """Main function"""
    s = Scrapper()
    url_dict = s.scrap_history()

    metadata_dict = await metaExtractor(url_dict).extract()
    predicted_dict = websitePredictor(metadata_dict).predict()

    print(predicted_dict)


if __name__ == '__main__':
    asyncio.run(main())
