import scrapy
from datetime import datetime
from scrapy.selector import Selector
from tutorial.items import StackItem


class StackSpider(scrapy.Spider):
    name = "stack"
    allowed_domains = ['d1cm.com']
    start_urls = [
        'http://news.d1cm.com/col/1000/hwzx/'
    ]

    def parse(self, response):
        questions = Selector(response).xpath('//*[@id="listDiv"]/div/dl')
        print(questions.__len__())
        for question in questions:
            item = StackItem()
            item['title'] = question.xpath('a/dd/h2/text()').extract()[0]
            item['description'] = question.xpath('a/dd/p/text()').extract()[0]
            item['releasetime'] = question.xpath('a/dd/span/text()').extract()[0]
            flag = StackSpider()
            if flag.juge(item['releasetime'], 6):
                item['description'] = item['description'].replace('\n', '')
                item['releasetime'] = item['releasetime'].split('.')[0] + '-' + item['releasetime'].split('.')[1]\
                                  + '-' + item['releasetime'].split('.')[2].split(' ')[0]
            else:
                break

            yield item

    def juge(self, date, day_time):
        timeTuple = datetime.strptime(date, '%Y.%m.%d %H:%M')
        now = datetime.today()
        tomorrow = now.replace(day = now.day - day_time)
        print(day_time,tomorrow,now)
        if tomorrow < timeTuple :
            return True
        else:
            return False




