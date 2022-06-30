import scrapy
from stock_spider.items import StockSpiderItem
#//*[@id="2020-emnlp-main"]/p[2]/span[2]/strong/a
class Emnlp2020Spider(scrapy.Spider):
    name = 'emnlp_2020'
    allowed_domains = ['']
    start_urls = ['file:///Users/sauron/Desktop/Code/crawler/acl-abstract/emnlp/2020.html']

    def parse(self, response):
        stock_item = StockSpiderItem()
        conferences_name_list = ["2020-emnlp-main","2020-emnlp-demos","2020-emnlp-tutorials","2020-alw-1",
                                 "2020-blackboxnlp-1","2020-clinicalnlp-1","2020-cmcl-1","2020-codi-1","2020-deelio-1",
                                 "2020-eval4nlp-1","2020-findings-emnlp","2020-insights-1","2020-intexsempar-1","2020-louhi-1",
                                 "2020-nlpbt-1","2020-nlpcovid19-2","2020-nlpcss-1","2020-nlposs-1","2020-privatenlp-1",
                                 "2020-scai-1","2020-sdp-1","2020-sigtyp-1","2020-splu-1","2020-spnlp-1","2020-sustainlp-1",
                                 "2020-wmt-1","2020-wnut-1"]
        conferences_number_list = [752,30,8,23,33,34,11,18,12,18,448,19,7,17,10,38,24,22,6,4,42,7,8,13,25,142,81]

        for index in range(0, len(conferences_name_list)):
            stock_item[conferences_name_list[index] + "_titles"], stock_item[conferences_name_list[index] + "_authors"], \
            stock_item[conferences_name_list[index] + "_abstracts"] = \
                self.get_form(response, conferences_number_list[index], conferences_name_list[index])

        yield stock_item

    def get_form(self, response, papers_number, type):
        titles = list()
        authors = list()
        abstracts = list()
        for i in range(1, papers_number):
            # //*[@id="abstract-2020--acl-tutorials--4"]/div
            title = response.xpath("string(//*[@id=\"" + type + "\"]/p[" + str(i + 1) + "]/span[2]/strong/a)").extract()
            author = response.xpath("//*[@id=\"" + type + "\"]/p[" + str(i + 1) + "]/span[2]/a/text()").extract()
            abstract = response.xpath("//*[@id=\"abstract-" + type.replace("2020-","2020--")+ "--" + str(i) + "\"]/div/text()").extract()
            titles.append(title[0])
            if len(author) == 0:
                print(title, author, abstract, type)
            authors.append(author[0])
            abstracts.append(abstract)
        return titles, authors, abstracts
