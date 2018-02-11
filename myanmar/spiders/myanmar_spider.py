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

        # to extract name
        name = response.css('h1#firstHeading::text').extract_first()
        
        # to extract all tr and td content
        all_tr = response.css('table.infobox.vcard>tr').extract() # obtain all th
        td_text = response.css('table.infobox.vcard>tr>td').extract() # obtain all td
        td_content_list = [BeautifulSoup(td).get_text() for td in td_text]

        # to extract cause
        cause = 'NA'
        for i, text in enumerate(all_tr):
            if 'Focus' in text:
                cause = i
        if cause != 'NA':
            cause_areas = td_content_list[cause]
        else:
            cause_areas = cause
        
        yield {'name': name,
            'cause_areas': cause_areas,
            #'location' : all_tr,
            #'website' : td_content_list
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
