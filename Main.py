
def main():
    """Main function"""
    url_dict = get_urls()
    metadata_dict = scrapper.extract_metadata(url_dict)
    print(metadata_dict)
    # predictions_dict = website_predictor.predict(metadata_dict)
    # show_predictions(predictions_dict, url_dict)
    # send_pie_chart(predictions_dict, url_dict)


if __name__ == '__main__':
    main()
