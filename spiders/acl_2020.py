import scrapy
from stock_spider.items import StockSpiderItem

class Acl2020Spider(scrapy.Spider):
    name = 'acl_2020'
    allowed_domains = ['']
    start_urls = ['file:///Users/sauron/Desktop/Code/crawler/acl-abstract/acl/2020.html']

    def parse(self, response):
        stock_item = StockSpiderItem()
        conferences_name_list = ["acl-main","acl-demos","acl-srw","acl-tutorials","alvr-1","autosimtrans-1","bea-1","bionlp-1","challengehml-1",
                                 "ecnlp-1","fever-1","figlang-1","iwpt-1","iwslt-1","ngt-1","nli-1","nlp4convai-1",
                                 "nlpcovid19-acl","nlpmc-1","nuse-1","repl4nlp-1","sigmorphon-1","socialnlp-1","winlp-1"]
        conferences_number_list = [779,44,43,9,6,7,22,23,10,14,8,39,27,35,29,6,16,19,10,16,25,30,9,37]

        for index in range(0, len(conferences_name_list)):
            stock_item[conferences_name_list[index]+"_titles"], stock_item[conferences_name_list[index]+"_authors"], \
            stock_item[conferences_name_list[index]+"_abstracts"] = \
                self.get_form(response,conferences_number_list[index],conferences_name_list[index])

        yield stock_item

    def get_form(self,response,papers_number,type):
        titles = list()
        authors = list()
        abstracts = list()
        for i in range(1,papers_number):
            #//*[@id="abstract-2020--acl-tutorials--4"]/div
            title = response.xpath("string(//*[@id=\"2020-"+type+"\"]/p["+str(i+1)+"]/span[2]/strong/a)").extract()
            author = response.xpath("//*[@id=\"2020-"+type+"\"]/p["+str(i+1)+"]/span[2]/a/text()").extract()
            abstract = response.xpath("//*[@id=\"abstract-2020--"+type+"--"+str(i)+"\"]/div/text()").extract()
            titles.append(title[0])
            if len(author) == 0:
                print(title,author,abstract,type)
            authors.append(author[0])
            abstracts.append(abstract)
        return titles,authors,abstracts
