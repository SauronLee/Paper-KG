import scrapy
from stock_spider.items import StockSpiderItem
#//*[@id="abstract-2018--iwslt-1--24"]/div
#//*[@id="abstract-D18-1034"]/div
class Emnlp2018Spider(scrapy.Spider):
    name = 'emnlp_2018'
    allowed_domains = ['']
    start_urls = ['file:///Users/sauron/Desktop/Code/crawler/acl-abstract/emnlp/2018.html']

    def parse(self, response):
        stock_item = StockSpiderItem()
        conferences_name_list = ["d18-1", "d18-2", "d18-3","w18-51","w18-52","w18-53","w18-54","w18-55","w18-56","w18-57",
                                 "w18-58","w18-59","w18-60","w18-61","w18-62","w18-63","w18-64","2018-iwslt-1"]
        conferences_number_list = [550,30,6,21,19,11,57,29,24,14,20,21,23,30,51,28,90,29]

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
                abstract = response.xpath("//*[@id=\"abstract-" + type.replace("2019-","2019--")+ "--" + str(i) + "\"]/div/text()").extract()
            titles.append(title[0])
            if len(author) == 0:
                print(title, author, abstract, type)
            authors.append(author[0])
            abstracts.append(abstract)
        return titles, authors, abstracts
