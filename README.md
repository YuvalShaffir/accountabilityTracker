# Acountability-Tracker
כ![ImgProUtils](https://github.com/YuvalShaffir/accountabilityTracker/assets/34415892/1b61f165-a055-45e9-bd9b-2c8817b52bd5)

As a result of the Oct 7th war, I found myself, and my friends more addicted to news and social media. This project might help with that by sending a categorized summary of the user's browsing history each day to an accountability friend through Telegram. 

# Project in-progress steps:
- Website scrapping - [V]
- Extracting metadata from each website - [V]
- Categorizing websites using Google machine learning NLP categorization model - [V]
- Designing the project as organized packages - [V]
- Sending a message through Telegram - [ ]
- Creating GUI - [ ]

# Classes:
Scrapper
- scrapper.py: Getting the browser history file, opening its database using SQL request, and extracting the websites and duration.
- metaExtractor.py: Extracting metadata from all websites in the list.

websitePredictor
- websitePredictor.py: Using Google language model to categorize the websites by subjects.

