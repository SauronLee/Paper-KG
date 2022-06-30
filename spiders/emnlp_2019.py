import scrapy
from stock_spider.items import StockSpiderItem

class Emnlp2019Spider(scrapy.Spider):
    name = 'emnlp_2019'
    allowed_domains = ['']
    start_urls = ['file:///Users/sauron/Desktop/Code/crawler/acl-abstract/emnlp/2019.html']

    def parse(self, response):
        stock_item = StockSpiderItem()
        conferences_name_list = ["d19-1", "d19-2", "d19-3", "d19-50", "d19-51", "d19-52", "d19-53", "d19-54", "d19-55",
                                 "d19-56",
                                 "d19-57",
                                 "d19-58", "d19-59", "d19-60", "d19-61", "d19-62", "d19-63", "d19-64", "d19-65",
                                 "d19-66", "2019-iwslt-1"]
        conferences_number_list = [682,7,45,25,9,30,24,16,59,35,31,30,8,17,33,22,14,10,7,18,33]

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
                abstract = response.xpath("//*[@id=\"abstract-" + type.replace("2018-", "2018--") + "--" + str(
                    i) + "\"]/div/text()").extract()
            titles.append(title[0])
            if len(author) == 0:
                print(title, author, abstract, type)
            authors.append(author[0])
            abstracts.append(abstract)
        return titles, authors, abstracts
