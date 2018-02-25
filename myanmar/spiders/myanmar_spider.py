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

        # extracting all tr and td content
        all_tr = response.css('table.infobox.vcard>tr').extract() # obtain all th
        td_text = response.css('table.infobox.vcard>tr>td').extract() # obtain all td
        td_content_list = [BeautifulSoup(td).get_text() for td in td_text]

        # extracting each of the fields:
        cause = 'NA'
        location = 'NA'
        website = 'NA'
        for i, text in enumerate(all_tr):
            if 'Focus' in text:
                cause = i
            elif 'Location' in text:
                location = i
            elif 'Website' in text:
                website = i

        # name
        name = response.css('h1#firstHeading::text').extract_first()

        # cause
        if cause != 'NA':
            cause_areas = td_content_list[cause]
        else:
            cause_areas = cause
        
        # location
        if location != 'NA':
            location_area = td_content_list[location].strip()
        else:
            location_area = location

        # website
        if website != 'NA':
            website_link = td_content_list[website].strip()
        else:
            website_link = website

        # established (first intro para)
        intro_para = ''.join(response.css('div.mw-parser-output>p:first-of-type *::text').extract())

        # mission
        try: 
            mission_id_m = ''.join(response.css("div.mw-parser-output>h2>span[id*='mission']::attr(id)").extract())
            mission_id_M = ''.join(response.css("div.mw-parser-output>h2>span[id*='Mission']::attr(id)").extract())
            if len(mission_id_m) > 0:
                string = "div.mw-parser-output>h2>span#%s::text"% (mission_id_m)
            if len(mission_id_M) > 0:
                string = "div.mw-parser-output>h2>span#%s::text" % (mission_id_M)
            mission = response.css(string).extract()
        except:
            mission = 'NA'

        yield {'name': name,
            'cause_area': cause_areas,
            'location' : location_area,
            'website' : website_link,
            'established/ intro statement' : intro_para,
            # 'programme_types' : ,
            # 'other_info' : ,
            # 'headcount' : ,
            # 'financials' : ,

            # 'religious' : ,
            # 'registered' : ,
            # 'outputs' : ,
            'mission' : mission,
            # 'theory_of_change' : 
            }
        
        

        """
        ['name', 'cause_areas', 'location', 'website', 'programme_type', 'other_info', 'headcount', 
        'financials', 'established', 'religious', 'registered', 'outputs', 'mission','theory_of_change']
        """