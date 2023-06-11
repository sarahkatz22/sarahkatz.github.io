
import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
import difflib

def get_soup(url):
    """
    Creates Beautiful Soup object from a URL to parse its HTML content. 
    Returns soup. 
    """ 
    URL = f'{url}'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup

def find_matching_product(target_product, product_list, threshold):
    """
    Finds the best matching product to the target product name from a given product list, 
    based on the SequenceMatcher algorithm, using a given threshold. 
    """ 
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

def product_comparision(soup1, soup2): 
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

    for key, val in dict1.items():
        match = find_matching_product(key, list2, 0.605) 
        if match != None: 
            dict1[key].append(dict2[match])

    return dict1

def str_to_float(dict): 
    new_dict = {}
    for key, val in dict.items(): 
        n_val = [(item.replace(',', '')) for item in val]
        l_num = list(map(float, n_val)) 
        new_dict[key] = l_num
    
    return new_dict


def at_risk(soup1, soup2): 

    risk_products = []

    d1 = product_comparision(soup1, soup2)
    n_dict = str_to_float(d1)

    for key, val in n_dict.items():
        if len(val) > 1:
            if val[0] > val[1]: 
                risk_products.append(key)

    return risk_products 
     

def safe(soup1, soup2):

    safe_products = []

    d1 = product_comparision(soup1, soup2)
    n_dict = str_to_float(d1)
    
    for key, val in n_dict.items():
        if len(val) > 1:
            if val[1] >= val[0]: 
                safe_products.append(key)
    
    return safe_products




