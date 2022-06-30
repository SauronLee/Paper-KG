import scrapy

from stock_spider.items import StockSpiderItem
#//*[@id="2021-acl-short"]/p[2]/span[2]/strong/a
#//*[@id="2021-acl-srw"]/p[2]/span[2]/strong/a

#//*[@id="2021-acl-tutorials"]/p[2]/span[2]/strong/a

#//*[@id="2021-bppf-1"]/p[2]/span[2]/strong/a
#//*[@id="2021-bppf-1"]/p[2]/span[2]/a[1]
#//*[@id="abstract-2021--bppf-1--1"]/div
#//*[@id="2021-dialdoc-1"]/p[2]/span[2]/strong/a
#//*[@id="2021-semeval-1"]/p[2]/span[2]/strong/a
#//*[@id="2021-semeval-1"]/p[2]/span[2]/a[1]
#//*[@id="abstract-2021--semeval-1--1"]/div

class Acl2021Spider(scrapy.Spider):
    name = 'acl_2021'
    allowed_domains = ['']
    start_urls = ['file:///Users/sauron/Desktop/Code/crawler/acl-abstract/acl/2021.html']

    def parse(self, response):
        stock_item = StockSpiderItem()
        conferences_name_list = ["long","short","srw","demo","tutorials","bppf","case","dialdoc","internlp", \
                                 "iwpt","iwslt","lchange","metanlp","mwe","nlp4posimpact","nlp4prog","repl4nlp", \
                                 "semeval","sigmorphon","splurobonlp","spnlp","starsem","unimplicit","wat","woah"]
        conferences_number_list = [572,140,37,44,7,5,28,17,8,25,34,10,10,9,17,11,33,187,30,10,9,31,9,31,25]
        for index in range(0,5):
            stock_item[conferences_name_list[index]+"_titles"], stock_item[conferences_name_list[index]+"_authors"], \
            stock_item[conferences_name_list[index]+"_abstracts"] = \
                self.get_form(response,conferences_number_list[index],conferences_name_list[index])
        for index in range(5, len(conferences_name_list)):
            #stock_item["long_titles"],stock_item["long_authors"],stock_item["long_abstracts"] = self.get_long(response,long_papers_number)
            stock_item[conferences_name_list[index]+"_titles"], stock_item[conferences_name_list[index]+"_authors"], \
            stock_item[conferences_name_list[index]+"_abstracts"] = \
                self.get_form2(response,conferences_number_list[index],conferences_name_list[index])

        yield stock_item

    def get_form(self,response,papers_number,type):
        titles = list()
        authors = list()
        abstracts = list()
        for i in range(1,papers_number):
            #title: //*[@id="2021-acl-short"]/p[2]/span[2]/strong/a
            title = response.xpath("string(//*[@id=\"2021-acl-"+type+"\"]/p["+str(i+1)+"]/span[2]/strong/a)").extract()
            author = response.xpath("//*[@id=\"2021-acl-"+type+"\"]/p["+str(i+1)+"]/span[2]/a/text()").extract()
            #abstract: //*[@id="abstract-2021--acl-short--1"]/div
            abstract = response.xpath("//*[@id=\"abstract-2021--acl-"+type+"--"+str(i)+"\"]/div/text()").extract()
            titles.append(title[0])
            authors.append(author[0])
            abstracts.append(abstract)
        return titles,authors,abstracts

    def get_form2(self,response,papers_number,type):
        titles = list()
        authors = list()
        abstracts = list()
        for i in range(1,papers_number):
            #title: //*[@id="2021-bppf-1"]/p[4]/span[2]/strong/a
            title = response.xpath("string(//*[@id=\"2021-"+type+"-1\"]/p["+str(i+1)+"]/span[2]/strong/a)").extract()
            author = response.xpath("//*[@id=\"2021-"+type+"-1\"]/p["+str(i+1)+"]/span[2]/a/text()").extract()
            #abstract: //*[@id="abstract-2021--dialdoc-1--8"]/div
            abstract = response.xpath("//*[@id=\"abstract-2021--"+type+"-1--"+str(i)+"\"]/div/text()").extract()
            titles.append(title[0])
            authors.append(author[0])
            abstracts.append(abstract)
        return titles,authors,abstracts


