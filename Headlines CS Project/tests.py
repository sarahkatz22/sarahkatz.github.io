import pytest
from headlines import Headlines

def test_top_headlines_country_1():
    """ Tests the function top_headlines_country_cat for correct country""" 


    h1 = Headlines(country='us', category='general', 
                   sources='cnn', q='', 
                   psize=20, p=100)
    
    res = h1.top_headlines_source()
    source_ids = [source['id'] for source in h1.get_sources()['sources']]

    for article in res['articles']:
        id = article['source']['id']
        assert id in source_ids
        

def test_top_headlines_2():
    """ Tests the function top_headlines_source """ 


    h2 = Headlines(country='us', category='general', sources='bbc-news', q='', 
                   psize=20, p=100)
    
    res = h2.top_headlines_source()
    for article in res['articles']: 
        assert article['source']['id'] == 'bbc-news'