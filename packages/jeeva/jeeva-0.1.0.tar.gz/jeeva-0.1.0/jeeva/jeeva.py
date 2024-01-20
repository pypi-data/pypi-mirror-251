import requests
from bs4 import BeautifulSoup
from googlesearch import search
import spacy

class NERProcessor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def perform_ner(self, text, ner_type=None):
        doc = self.nlp(text)
        entities = {
            "names": [],
            "emails": [],
            "phone_numbers": [],
            "product_names": [],
            "organizations": [],
        }

        for ent in doc.ents:
            if ner_type is None or ent.label_ == ner_type.upper():
                if ent.label_ == "PERSON":
                    entities["names"].append(ent.text)
                elif ent.label_ == "EMAIL":
                    entities["emails"].append(ent.text)
                elif ent.label_ == "PHONE":
                    entities["phone_numbers"].append(ent.text)
                elif ent.label_ == "PRODUCT":
                    entities["product_names"].append(ent.text)
                elif ent.label_ == "ORG":
                    entities["organizations"].append(ent.text)

        return entities

def google_search(query, num_results=10):
    links = []
    for j in search(query, stop=num_results, pause=2):
        links.append(j)
    return links

def extract_info_from_url(url, ner_processor, ner_type=None):
    if ner_processor is None:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract text content from the page and remove newline characters
        text_content = soup.get_text().replace('\n', ' ')
        return text_content
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract text content from the page and remove newline characters
    text_content = soup.get_text().replace('\n', ' ')

    # Perform NER using the provided ner_processor
    entities = ner_processor.perform_ner(text_content, ner_type=ner_type)

    # Remove duplicates and strip newline characters
    entities["names"] = list(set(entity.strip() for entity in entities["names"]))
    entities["emails"] = list(set(entity.strip() for entity in entities["emails"]))
    entities["phone_numbers"] = list(set(entity.strip() for entity in entities["phone_numbers"]))
    entities["product_names"] = list(set(entity.strip() for entity in entities["product_names"]))
    entities["organizations"] = list(set(entity.strip() for entity in entities["organizations"]))

    return entities


def main(query, ner_type=None):
    # Create NERProcessor instance
    ner_processor = NERProcessor()

    # Perform Google search and get links
    links = google_search(query)

    # Extract information from each link
    results = []
    for link in links:
        entities = extract_info_from_url(link, ner_processor, ner_type=ner_type)
        results.append({
            'Link': link,
            'Entities': entities
        })

    # Display the results in a simple table-like structure
    for result in results:
        print(f"Link: {result['Link']}")
        print("Entities:")
        if ner_type is None or ner_type.lower() == 'person':
            print(f"Name: {result['Entities']['names']}")
        if ner_type is None or ner_type.lower() == 'email':
            print(f"Email: {result['Entities']['emails']}")
        if ner_type is None or ner_type.lower() == 'phone':
            print(f"Phone Number: {result['Entities']['phone_numbers']}")
        if ner_type is None or ner_type.lower() == 'product':
            print(f"Product Name: {result['Entities']['product_names']}")
        if ner_type is None or ner_type.lower() == 'organization':
            print(f"Organization: {result['Entities']['organizations']}")
        print("Contact Author: 9360985570 (for more detailed data)\n")

if __name__ == "__main__":
    user_query = input("Enter your query: ")
    user_ner_type = input("Enter the NER type (person, email, phone, product, organization) or leave blank for all: ")
    main(user_query, ner_type=user_ner_type)
