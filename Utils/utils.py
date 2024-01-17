from googletrans import Translator
import matplotlib.pyplot as plt
import tldextract



def translate_text(text: str):
    # Translate the text to English
    try:
        translator = Translator()
        translation = translator.translate(text[0:999], dest='en').text
        return translation

    except Exception as e:
        print(e)


def show_predictions(predictions_dict, url_dict):
    plt.pie([v for v in url_dict.values()], labels=[k for k in predictions_dict.keys()],
            autopct='%1.1f%%')
    plt.savefig('E:\\PythonProjects\\Acountability-Tracker\\website_usage.png', bbox_inches='tight')
    plt.show()


def get_website_name(url: str) -> str:
    extracted_info = tldextract.extract(url)
    return extracted_info.domain