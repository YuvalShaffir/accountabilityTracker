
![Accountability Tracker](https://github.com/YuvalShaffir/accountabilityTracker/assets/34415892/05f24280-f093-4839-a238-7f5c63d05da4)


Following the events of the October 7th war, I observed a significant surge in news and social media consumption among my friends, family, and myself. This surge negatively impacted our work efficiency, prompting me to seek a solution. 
Drawing from my experiences with accountability partners during my student life, I developed a tool aimed at enhancing productivity.

This tool generates a categorized pie chart of my internet usage, breaking down the data into specific subjects such as Work, Social Media, News, and more. 
To achieve this, I utilize cloudscraper for website data scraping and the Google Language V1 categorization model to analyze and categorize the metadata from various websites. 
This innovative approach not only addresses the challenges posed by increased media consumption but also provides a tangible solution for maintaining focus and productivity.

 

# Project in-progress steps:

- [x] Website scrapping
- [x] Extracting metadata from each website 
- [x] Categorizing websites using Google machine learning NLP categorization model 
- [x] Designing the project as organized packages
- [x] Add multiprocessing to the extraction of metadata.
- [x] Add multiprocessing to the predictor.
- [ ] Sending a message through Telegram
- [ ] Creating GUI 

# Classes:
Scrapper
- scrapper.py: Getting the browser history file, opening its database using SQL request, and extracting the websites and duration.
- metaExtractor.py: Extracting metadata from all websites in the list.

websitePredictor
- websitePredictor.py: Using Google language model to categorize the websites by subjects.

