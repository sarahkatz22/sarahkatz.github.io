
import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
import difflib

# 1. Create Beautiful Soup objects for each website to parse the HTML content:

URL1 = "https://www.speedcubes.co.za/12-2x2x2"
page1 = requests.get(URL1)
soup1 = BeautifulSoup(page1.content, "html.parser")

URL2 = "https://cubeco.co.za/collections/2x2"
page2 = requests.get(URL2)
soup2 = BeautifulSoup(page2.content, "html.parser")

# Function to find the best matching product name
def find_matching_product(target_product, product_list, threshold):
    best_match = None
    best_ratio = 0

    for product in product_list:
        ratio = difflib.SequenceMatcher(None, target_product.lower(), product.lower()).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best_match = product

    # Check if a suitable match is found
    if best_match is None or best_ratio < threshold:
        return None
    else:
        return best_match

# Product comparison: 
products1 = soup1.find_all('article')
products2 = soup2.find('div', class_="grid-uniform grid-link__container")

dict1 = {}

for product1 in products1: 
    title1 = product1.find('h2', class_='h3 product-title').text.strip()
    price1 = product1.find('span', class_='price').text.strip()
    dict1[title1[:-3]] = [price1[1:]]

list2 = []
dict2 = {}
for product2 in products2.find_all('div', class_="grid__item wide--one-fifth large--one-quarter medium-down--one-half"): 

    title2 = product2.find('p', class_='grid-link__title')
    title2_text = title2.get_text(strip=True)
    list2.append(title2_text)

    price2 = product2.find('p', class_='grid-link__meta')
    price2_text = price2.contents[-1].strip()

    dict2[title2_text] = price2_text[2:]

print(dict1)
print(list2)

for key, val in dict1.items():
    match = find_matching_product(key, list2, 0.605) 
    if match != None: 
        dict1[key].append(dict2[match])

risk_products = []
safe_products = []



for key, val in dict1.items():
    val_num = list(map(float, val)) 
    if len(val_num) > 1:
        if val_num[0] > val_num[1]: 
            risk_products.append(key)
        elif val_num[1] >= val_num[0]: 
            safe_products.append(key)

print(risk_products)
print(safe_products)





