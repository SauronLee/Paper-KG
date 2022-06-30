import scrapy
from stock_spider.items import StockSpiderItem
#//*[@id="2021-naacl-main"]/p[2]/span[2]/strong/a
#//*[@id="2021-naacl-main"]/p[2]/span[2]/a[1]
#//*[@id="abstract-2021--naacl-main--1"]/div
class Naacl2021Spider(scrapy.Spider):
    name = 'naacl_2021'
    allowed_domains = ['']
    start_urls = ['file:///Users/sauron/Desktop/Code/crawler/acl-abstract/naacl/2021.html']

    def parse(self, response):
        stock_item = StockSpiderItem()
        conferences_name_list = ["2021-naacl-main", "2021-naacl-demos", "2021-naacl-srw", "2021-naacl-tutorials",
                                 "2021-naacl-industry",
                                 "2021-alvr-1", "2021-americasnlp-1", "2021-autosimtrans-1", "2021-bionlp-1",
                                 "2021-calcs-1",
                                 "2021-clpsych-1", "2021-cmcl-1", "2021-dash-1", "2021-deelio-1", "2021-maiworkshop-1",
                                 "2021-nlp4if-1", "2021-nlpmc-1", "2021-nuse-1", "2021-privatenlp-1", "2021-sdp-1",
                                 "2021-sigtyp-1", "2021-smm4h-1", "2021-socialnlp-1", "2021-teachingnlp-1",
                                 "2021-textgraphs-1",
                                 "2021-trustnlp-1", "2021-vigil-1"]
        conferences_number_list = [478,18,22,7,40,8,31,7,39,21,25,29,17,15,14,22,10,11,8,23,15,34,17,27,21,9,1]

        if len(conferences_name_list) != len(conferences_number_list):
            print("error!---------size!")


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
            # //*[@id="n18-1"]/p[2]/span[2]/strong/a
            title = response.xpath("string(//*[@id=\"" + type + "\"]/p[" + str(i + 1) + "]/span[2]/strong/a)").extract()
            # //*[@id="p19-1"]/p[1]/span[2]/a[1] //*[@id="p19-4"]/p[2]/span[2]/a[1]
            author = response.xpath("//*[@id=\"" + type + "\"]/p[" + str(i + 1) + "]/span[2]/a/text()").extract()
            # //*[@id="abstract-P19-1001"]/div
            ##//*[@id="abstract-2021--naacl-main--1"]/div //*[@id="abstract-2021--naacl-main--3"]/div
            #"2021-naacl-main"

            abstract = response.xpath("//*[@id=\"abstract-" + type.replace("2021-","2021--")+ "--" + str(i) + "\"]/div/text()").extract()
            titles.append(title[0])
            if len(title) == 0:
                print("error of title extract!")
            if len(author) == 0:
                print("error of author extract!")
            authors.append(author[0])
            abstracts.append(abstract)
        return titles, authors, abstracts
