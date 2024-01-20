Jeeva - A sample module for webscrapping

## Description

The package is designed to perform Google searches, extract information from web pages, and conduct Named Entity Recognition (NER) using the SpaCy library. The core functionality revolves around a `NERProcessor` class that utilizes SpaCy for extracting entities such as names, emails, phone numbers, product names, and organizations from text. Additionally, the package includes functions for performing Google searches and extracting information from URLs.

## Features

1. **NERProcessor:**
   - Performs Named Entity Recognition (NER) on a given text.
   - Extracts entities such as names, emails, phone numbers, product names, and organizations.
   - Allows filtering entities based on specific types (e.g., person, email, phone, product, organization).

2. **Google Search:**
   - Conducts a Google search based on a user-provided query.
   - Retrieves a specified number of search results.

3. **Extract Information from URL:**
   - Extracts text content from a given URL.
   - Utilizes the `NERProcessor` for Named Entity Recognition if provided.
   - Handles cases where the `NERProcessor` is not provided, returning raw text.

4. **Main Script:**
   - Integrates the functionalities of the package into a user-friendly command-line interface.
   - Allows users to input a query, specify the type of entities to extract, and displays the results in a structured format.

5. **Contact Author Information:**
   - visit jeevanantham-portfolio.web.app

6. **Flexible NER Type Filtering:**
   - Allows users to filter entities based on specific types or extract all available entities if no type is specified.

This package is useful for scenarios where users want to automate Google searches, extract information from web pages, and perform basic Named Entity Recognition on text data. The flexible NER filtering provides customization options based on the user's specific needs.

## Installation

bash
pip install jeeva


## Usage

### NERProcessor

from jeeva import NERProcessor

# Create an instance of NERProcessor
ner_processor = NERProcessor()

# Perform Named Entity Recognition on a text
entities = ner_processor.perform_ner("Your sample text here")

# Access the extracted entities
print("Names:", entities["names"])
print("Emails:", entities["emails"])
print("Phone Numbers:", entities["phone_numbers"])
print("Product Names:", entities["product_names"])
print("Organizations:", entities["organizations"])


### Google Search


from jeeva import google_search

# Perform a Google search
links = google_search("Your query here", num_results=10)

### Extract Information from URL
from jeeva import extract_info_from_url
# Example usage when NERProcessor is provided
entities = extract_info_from_url("https://example.com", ner_processor, ner_type="person")

# Example usage when NERProcessor is not provided
text_content = extract_info_from_url("https://example.com", ner_processor=None)
print(text_content)

### Main Script

# Example usage of the main script
from jeeva import main

user_query = input("Enter your query: ")
user_ner_type = input("Enter the NER type (person, email, phone, product, organization) or leave blank for all: ")
main(user_query, ner_type=user_ner_type)


## Contact

For any issues or inquiries, please contact:

- Jeevanantham V
- jeevanantham.v26@gmail.com

## License

This project is free and open source as it is limited in features. To perform web scraping with NLP tasks with highest accuracy of 99.82% contact me. Th original module contains about 300 varieties of trained NLP categoriztion, advanced web scrapping techniques to scrap information from any site.
contact - www.jeevanantham-portfolio.web.app