import scrapy
from bs4 import BeautifulSoup
from myanmar.items import MyanmarItem

class ThailandSpider(scrapy.Spider):
    country = 'Thailand'
    name = "thailand"
    allowed_domains = ["en.wikipedia.org"]

    def start_requests(self):
        urls = [
            'https://en.wikipedia.org/wiki/List_of_non-governmental_organizations_in_Thailand',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        all_links = response.css('div.mw-parser-output>ul>li>a::attr(href)').extract()
        for link in all_links:
            url = response.urljoin(link)
            yield scrapy.Request(url, callback=self.parse_org_page)

    def parse_org_page(self, response, country=country):

        # extracting all tr and td content
        all_tr = response.css('table.infobox.vcard>tr').extract() # obtain all th
        td_text = response.css('table.infobox.vcard>tr>td').extract() # obtain all td
        td_content_list = [BeautifulSoup(td).get_text() for td in td_text]

        # initiate as 'NA' for each variable
        var_list = ['cause_areas', 'location_area', 'website_link', 'method',
        'method', 'revenue', 'employees']
        var_text = ['Focus', 'Area served', 'Website', 'Method', 
        'Product', 'Revenue', 'Employees']
        variables_and_text = {text:var for (var, text) in zip(var_list,var_text)}
        data = {var:'NA' for var in var_list}

        # if name of variable is in column, return table index of variable as variable
        for i, actual_text in enumerate(all_tr):
            for var_text_ in variables_and_text.keys():
                if var_text_ in actual_text:
                    var = variables_and_text[var_text_]
                    data[var] = td_content_list[i]

        # name
        name = response.css('h1#firstHeading::text').extract_first()

        # description (first intro paragraph)
        intro_para = ''.join(response.css('div.mw-parser-output>p:first-of-type *::text').extract())


        yield {'name': name,
            'description': intro_para,
            'website': data['website_link'],
            'cause_area': data['cause_areas'],
            'country': country,
            'city': data['location_area'],
            'programme_types': data['method'],
            'revenue': data['revenue'],
            'employees': data['employees']
            # 'address': ,
            # 'contact_number' : ,
            # 'email' : ,
            # 'contact_person' : ,
            }
        
