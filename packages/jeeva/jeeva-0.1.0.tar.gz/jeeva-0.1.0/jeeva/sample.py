import jeeva

user_query = "about Larsen and toubro"
ner_processor = jeeva.NERProcessor()
results = jeeva.google_search(user_query)
print(results)
print("\n")

for i in results:
    info = jeeva.extract_info_from_url(i,ner_processor=None)
    print(i)
    print(info, end="\n")

## To get details just pass one line code
print(jeeva.main(user_query))

## To get specific 
print(jeeva.main(user_query, ner_type="person"))

##Availble types for free are person, organiation, email, phone number, product
#visit jeevanantham-portfolio.web.app
#contact details available in website