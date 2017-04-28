import scrapy
import csv
from scrapy.spider import CrawlSpider, Rule
from datetime import datetime
from scrapy.selector import Selector
from E.items import EItem
from scrapy import log
from scrapy import cmdline


class E02Spider(CrawlSpider):
    name = "e02"
    # allowed_domains = ['cngold.com.cn']
    start_urls = [
        'http://forex.cngold.com.cn/whxw.html'
    ]

    def parse(self, response):
        try:
            questions = Selector(response).xpath('//*[@class="news_list"]/div[@class="news_ul"]/ul/li')
            next_page = Selector(response).xpath(
                '//*[@class="fenye"]/div[@class="page"]/a[@class="page_next"]/@href').extract_first()
            for question in questions:
                item = EItem()
                item['title'] = question.xpath('h4/a/text()').extract_first()
                item['description'] = question.xpath('p[@class="p1"]/text()').extract_first()
                item['releasetime'] = question.xpath('p[@class="p2"]/text()').extract_first()
                print(item['releasetime'])
                item['releasetime'] = item['releasetime'].replace('时间：', '')
                item['label'] = []

                if self.juge(item['releasetime'], 0, 0, 0):
                    with open('E02汇市新闻币种动态.csv', 'rU') as f:
                        reader = csv.DictReader(f)
                        column = [row['名称'] for row in reader]
                        for c in column:
                            if c in item['title']:
                                if not c in item['label']:
                                    item['label'].append(c)

                            if c in item['description']:
                                if not c in item['label']:
                                    item['label'].append(c)
                else:
                    break
                yield item

            if next_page is not None:
                next_page = response.urljoin(next_page)
                print(next_page)
                yield scrapy.Request(next_page, callback=self.parse)

        except Exception as error:
            log(error)


    def juge(self, date, day_time, hour_time, minute_time):
         timeTuple = datetime.strptime(date, '%Y-%m-%d %H:%M')
         now = datetime.today()
         tomorrow = now.replace(day=now.day - day_time, hour=now.hour - hour_time, minute=now.minute - minute_time)
         print(day_time, tomorrow, now,'E02')
         if day_time == 0 and hour_time == 0 and minute_time == 0:
             return True;
         else:
             if tomorrow < timeTuple:
                 return True
             else:
                 return False
