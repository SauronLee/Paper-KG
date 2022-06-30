import scrapy
from stock_spider.items import StockSpiderItem
#//*[@id="abstract-P18-1210"]/div
class Acl2018Spider(scrapy.Spider):
    name = 'acl_2018'
    allowed_domains = ['']
    start_urls = ['file:///Users/sauron/Desktop/Code/crawler/acl-abstract/acl/2018.html']

    def parse(self, response):
        stock_item = StockSpiderItem()
        conferences_name_list = ["p18-1", "p18-2", "p18-3", "p18-4", "p18-5", "w18-23", "w18-24", "w18-25", "w18-26", \
                                 "w18-27", "w18-28", "w18-29", "w18-30", "w18-31", "w18-32", "w18-33", "w18-34", \
                                 "w18-35", "w18-36", "w18-37"]
        conferences_number_list = [257,126,23,25,9,26,15,10,12,17,10,8,28,10,22,10,11,14,10,31]

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
            # //*[@id="p19-1"]/p[2]/span[2]/strong/a
            # //*[@id="p19-2"]/p[2]/span[2]/strong/a //*[@id="p19-1"]/p[3]/span[2]/strong/a
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
            if len(author) == 0:
                print(title, author, abstract, type)
            authors.append(author[0])
            abstracts.append(abstract)
        return titles, authors, abstracts
