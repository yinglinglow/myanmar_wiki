import scrapy
from bs4 import BeautifulSoup
from myanmar.items import MyanmarItem

class MyanmarSpider(scrapy.Spider):
    name = "myanmar"
    allowed_domains = ["en.wikipedia.org"]

    def start_requests(self):
        urls = [
            'https://en.wikipedia.org/wiki/List_of_official_social_and_NGO_organisations_in_Myanmar',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        all_links = response.css('div.mw-parser-output>ul>li>a::attr(href)').extract()
        for link in all_links:
            url = response.urljoin(link)
            yield scrapy.Request(url, callback=self.parse_org_page)

    def parse_org_page(self, response):
        name = response.css('h1#firstHeading::text').extract_first()
        
        # to find cause_areas
        len_tr = response.css('table.infobox.vcard>tr>th::text').extract()
        print(len_tr)
        i = 1
        cause = 0
        for text in len_tr:
            if text == 'Focus':
                cause = i
            i += 1

        cause_areas = response.css('table.infobox.vcard>tr:nth-child(' + str(cause + 2) +')>td>a::text').extract()
        
        yield {'name': name,
            'cause_areas': cause_areas
            # 'location' : ,
            # 'website' : ,
            # 'programme_type' : ,
            # 'other_info' : ,
            # 'headcount' : ,
            # 'financials' : ,
            # 'established' : ,
            # 'religious' : ,
            # 'registered' : ,
            # 'outputs' : ,
            # 'mission' : ,
            # 'theory_of_change' : 
            } 
        
        
        # soup = BeautifulSoup(response.text, "lxml")
        # items = []

        # for link in soup.find("div", {"class":"mw-content-text"})
        #     .find_all('a', href=True): # finds all links to job pages
        #     yield {'link': link['href']} # assigns links under link
