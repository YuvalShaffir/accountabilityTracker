import os
from mpire import WorkerPool
from google.cloud import language_v1
from google.cloud import language

# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = ('C:\\Users\\User\\Documents\\Google Cloud Service\\'
#                                                 'banded-coder-408816-183df3de095c.json')

gcs_folder = os.path.expanduser('~\Documents\Google Cloud Services')
json_file = [pos_json for pos_json in os.listdir(gcs_folder) if pos_json.endswith('.json')]
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.expanduser(gcs_folder + "/" + json_file[0])
print(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
translation = 'Ynet - News, Economy, Sports and Health - Regular reports from Israel and the world the leading news site in Israel from Yedioth Ahronoth.Full coverage of news from Israel and the world, sports, economics, culture, food, science and nature, everything that is happening and everything interesting in Ynet Iran: a senior commander of the Revolutionary Guards is eliminated in Syria Netanyahu: "Military pressure";Hooded Families: "No Time" Hamas: We will not give up control for a ceasefire and Ariel Bibs 80 days in Hamas captivity: "Bad Dream" also under missiles: the factory in Sderot not stopped'
# print(f"Website Metadata: {translation}\n")


class websitePredictor:
    client_ = language_v1.LanguageServiceClient()
    type_ = language_v1.Document.Type.PLAIN_TEXT
    language_ = "en"

    def __init__(self, metadata_dict):
        self._meta_dict = metadata_dict

    def _get_prediction(self, metadata):
        try:
            text_content = str(metadata)[0:1000]

            document_dict = {"type": self.type_, "language": self.language_, "content": text_content}
            document = language_v1.ClassifyTextRequest(document=document_dict)
            encoding_type = language_v1.EncodingType.UTF8

            response = self.client_.classify_text(document)
            print(response.categories[0].name)
            print(str(int(round(response.categories[0].confidence, 3) * 100)) + "%")
            return [response.categories[0].name, int(round(response.categories[0].confidence, 3) * 100)]

        except Exception as e:
            print(e)

    def predict(self):
        predictions_dict = {}

        with WorkerPool(n_jobs=3) as pool:
            predictions_list = pool.map(self._get_prediction, self._meta_dict.values(), progress_bar=True)

        for i, url in enumerate(self._meta_dict.keys()):
            predictions_dict[url] = predictions_list[i]

        return predictions_dict

if __name__ == '__main__':
    predictor = websitePredictor({'www.ynet.co.il': translation})
    predictor.predict()