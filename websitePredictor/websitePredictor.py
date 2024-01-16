import os
from google.cloud import language_v1
from google.cloud import language

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = ('C:\\Users\\User\\Documents\\Google Cloud Service\\'
                                                'banded-coder-408816-183df3de095c.json')

# translation = 'Ynet - News, Economy, Sports and Health - Regular reports from Israel and the world the leading news site in Israel from Yedioth Ahronoth.Full coverage of news from Israel and the world, sports, economics, culture, food, science and nature, everything that is happening and everything interesting in Ynet Iran: a senior commander of the Revolutionary Guards is eliminated in Syria Netanyahu: "Military pressure";Hooded Families: "No Time" Hamas: We will not give up control for a ceasefire and Ariel Bibs 80 days in Hamas captivity: "Bad Dream" also under missiles: the factory in Sderot not stopped'
# print(f"Website Metadata: {translation}\n")


class websitePredictor:
    def __init__(self, metadata_dict):
        self._meta_dict = metadata_dict

    @staticmethod
    def _get_prediction(metadata):
        try:
            text_content = str(metadata)[0:1000]

            client = language_v1.LanguageServiceClient()

            type_ = language_v1.Document.Type.PLAIN_TEXT
            language_ = "en"
            document_dict = {"type": type_, "language": language_, "content": text_content}
            document = language_v1.ClassifyTextRequest(document=document_dict)
            encoding_type = language_v1.EncodingType.UTF8

            response = client.classify_text(document)
            print(response.categories[0].name)
            print(str(int(round(response.categories[0].confidence, 3) * 100)) + "%")
            return [response.categories[0].name, int(round(response.categories[0].confidence, 3) * 100)]

        except Exception as e:
            print(e)

    def predict(self):
        predictions_dict = {}
        for url, metadata in self._meta_dict.items():
            predictions_dict[url] = self._get_prediction(metadata)
        return predictions_dict
