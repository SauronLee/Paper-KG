import scrapy
from stock_spider.items import StockSpiderItem
class Emnlp2021Spider(scrapy.Spider):
    name = 'emnlp_2021'
    allowed_domains = ['']
    start_urls = ['file:///Users/sauron/Desktop/Code/crawler/acl-abstract/emnlp/2021.html']

    def parse(self, response):
        stock_item = StockSpiderItem()
        conferences_name_list = ["2021-emnlp-main","2021-emnlp-demo","2021-emnlp-tutorials","2021-argmining-1",
                                 "2021-blackboxnlp-1","2021-cinlp-1","2021-codi-main","2021-codi-sharedtask",
                                 "2021-conll-1","2021-crac-1","2021-disrpt-1","2021-eancs-1","2021-econlp-1",
                                 "2021-eval4nlp-1","2021-fever-1","2021-findings-emnlp","2021-insights-1",
                                 "2021-latechclfl-1","2021-law-1","2021-mrl-1","2021-mrqa-1","2021-newsum-1",
                                 "2021-nllp-1","2021-nlp4convai-1","2021-sustainlp-1","2021-wmt-1","2021-wnut-1"]
        conferences_number_list = [848,43,7,22,44,9,17,9,53,17,7,4,13,25,14,425,21,22,19,25,17,17,25,28,18,122,57]

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
            abstract = response.xpath(
                "//*[@id=\"abstract-" + type.replace("2021-", "2021--") + "--" + str(i) + "\"]/div/text()").extract()
            titles.append(title[0])
            if len(author) == 0:
                print(title, author, abstract, type)
            authors.append(author[0])
            abstracts.append(abstract)
        return titles, authors, abstracts