import scrapy

from stock_spider.items import StockSpiderItem


class Acl2019Spider(scrapy.Spider):
    name = 'acl_2019'
    allowed_domains = ['']
    start_urls = ['file:///Users/sauron/Desktop/Code/crawler/acl-abstract/acl/2019.html']

    def parse(self, response):
        stock_item = StockSpiderItem()
        conferences_name_list = ["p19-1", "p19-2", "p19-3", "p19-4", "w19-32", "w19-33", "w19-34", "w19-35", "w19-36", \
                                 "w19-37", "w19-38", "w19-39", "w19-40", "w19-41", "w19-42", "w19-43", "w19-44", \
                                 "w19-45", "w19-46", "w19-47", "w19-48", "w19-49", "w19-50", "w19-51", "w19-52", \
                                 "w19-53", "w19-54"]
        conferences_number_list = [661, 61, 35, 10, 26, 23, 15, 21, 57, 18, 25, 6, 29, 17, 27, 33, 53, 21, 40, 35, 29, 1,
                                   60, 22, 13, 69, 42]

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
            #//*[@id="p19-2"]/p[2]/span[2]/strong/a //*[@id="p19-1"]/p[3]/span[2]/strong/a
            title = response.xpath("string(//*[@id=\"" + type + "\"]/p[" + str(i + 1) + "]/span[2]/strong/a)").extract()
            #//*[@id="p19-1"]/p[1]/span[2]/a[1] //*[@id="p19-4"]/p[2]/span[2]/a[1]
            author = response.xpath("//*[@id=\"" + type + "\"]/p[" + str(i + 1) + "]/span[2]/a/text()").extract()
            #//*[@id="abstract-P19-1001"]/div
            if len(type) + len(str(i)) == 8:
                abstract = response.xpath("//*[@id=\"abstract-" + type.upper() + str(i) + "\"]/div/text()").extract()
            elif len(type) + len(str(i)) == 7:
                abstract = response.xpath("//*[@id=\"abstract-" + type.upper() + "0" + str(i) + "\"]/div/text()").extract()
            elif len(type) + len(str(i)) == 6:
                abstract = response.xpath("//*[@id=\"abstract-" + type.upper() + "00" + str(i) + "\"]/div/text()").extract()
            else:
                print("error of abstract extract!")
            titles.append(title[0])
            if len(author) == 0:
                print(title, author, abstract, type)
            authors.append(author[0])
            abstracts.append(abstract)
        return titles, authors, abstracts

