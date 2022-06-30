import scrapy
from stock_spider.items import StockSpiderItem
#//*[@id="abstract-P17-2001"]/div
class Acl2017Spider(scrapy.Spider):
    name = 'acl_2017'
    allowed_domains = ['']
    start_urls = ['file:///Users/sauron/Desktop/Code/crawler/acl-abstract/acl/2017.html']

    def parse(self, response):
        stock_item = StockSpiderItem()
        conferences_name_list = ["p17-1", "p17-2", "p17-3", "p17-4", "p17-5"]
        conferences_number_list = [196,108,24,22,7]

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

