import scrapy
from stock_spider.items import StockSpiderItem

class Naacl2019Spider(scrapy.Spider):
    name = 'naacl_2019'
    allowed_domains = ['']
    start_urls = ['file:///Users/sauron/Desktop/Code/crawler/acl-abstract/naacl/2019.html']

    def parse(self, response):
        stock_item = StockSpiderItem()
        conferences_name_list = ["n19-1", "n19-2", "n19-3", "n19-4", "n19-5", "w19-13", "w19-14",
                                 "w19-15", "w19-16", "w19-17", "w19-18", "w19-19", "w19-20", "w19-21",
                                 "w19-22", "w19-23", "w19-24", "w19-25", "w19-25", "w19-27", "w19-28", "w19-29", "w19-30"]
        conferences_number_list = [424,29,20,25,7,12,26,6,9,8,9,20,14,13,10,12,7,17,11,21,7,19,26]

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
            if len(type) + len(str(i)) == 8:
                abstract = response.xpath("//*[@id=\"abstract-" + type.upper() + str(i) + "\"]/div/text()").extract()
            elif len(type) + len(str(i)) == 7:
                abstract = response.xpath(
                    "//*[@id=\"abstract-" + type.upper() + "0" + str(i) + "\"]/div/text()").extract()
            elif len(type) + len(str(i)) == 6:
                abstract = response.xpath(
                    "//*[@id=\"abstract-" + type.upper() + "00" + str(i) + "\"]/div/text()").extract()
            else:
                print("error of abstract extract!")
            titles.append(title[0])
            if len(title) == 0:
                print("error of title extract!")
            if len(author) == 0:
                print("error of author extract!")
            authors.append(author[0])
            abstracts.append(abstract)
        return titles, authors, abstracts