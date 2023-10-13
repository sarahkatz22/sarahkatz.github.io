from newsapi import NewsApiClient

COUNTRIES = ["ae","ar","at","au","be","bg","br","ca","ch","cn","co","cu","cz","de","eg","fr","gb","gr", "hk","hu","id","ie","il","in","it","jp","kr","lt","lv","ma","mx","my","ng","nl","no","nz","ph","pl","pt","ro","rs","ru","sa","se","sg","si","sk","th","tr","tw","ua","us","ve","za"]
CATEGORIES = ["business", "entertainment", "general", "health", "science", "sports", "technology"]

class NewsPaper(): 

    country: str
    category: str
    sources: str
    q: str
    psize: int
    p: int

    def __init__(self, country, category, sources, q, psize, p): 
        self.place = country 
        self.cat = category 
        self.s = sources
        self.key = q
        self.pageSize = psize
        self.page = p

        self.api = NewsApiClient(api_key='c0199aec6219453ca2714cca98bb4b36')

    def get_sources(self): 
        """Returns list of sources based on set criteria."""

        sources = self.api.get_sources(category = self.cat, country=self.place)
        return sources

class AllArticles(NewsPaper): 
    def __init__(self, country, category, sources, q, psize, p):
        super().__init__(self, country, category, sources, q, psize, p)
        self.api = NewsApiClient(api_key='c0199aec6219453ca2714cca98bb4b36')


    def all_articles(self, sorter, from_p, to_p):
        """Returns all articles according to all paramater specifictions i.e. category, country, source, etc.""" 

        all_articles = self.api.get_everything(q= self.key, sources = self.s,
                                                   category = self.cat,
                                                   language = 'en',
                                                   country = self.place,
                                                   from_param = from_p,
                                                   to= to_p,
                                                   sort_by = sorter,
                                                   page = self.pageSize)
        
        return all_articles
    
    def get_sources(self):
        return super().get_sources()

class Headlines(NewsPaper):
    def __init__(self, country, category, sources, q, psize, p):
        super().__init__(country, category, sources, q, psize, p)
        self.api = NewsApiClient(api_key='c0199aec6219453ca2714cca98bb4b36')
    
    def top_headlines_country_cat(self): 
        """Returns live top and breaking headlines by country, category or country and category."""

        top_headlines = self.api.get_top_headlines(q= self.key, category = self.cat, 
                                                   language = 'en',country = self.place) 
                                                                                   
        return top_headlines
    
    def top_headlines_source(self):
        """Returns live top and breaking headlines by source/s.""" 

        top_headlines = self.api.get_top_headlines(q= self.key, sources = self.s, language = 'en') 
                                                                                   
        return top_headlines
    
    def get_sources(self):
        return super().get_sources()


