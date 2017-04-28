import scrapy
import csv
from scrapy.spider import CrawlSpider, Rule
from datetime import datetime
from scrapy.selector import Selector
from E.items import EItem
from scrapy import log


class E03Spider(CrawlSpider):
    name = "e03"
    allowed_domains = ['eastmoney.com']
    start_urls = [
        'http://finance.eastmoney.com/yaowen_cgjjj.html'
    ]

    def parse(self, response):
        try:
            questions = Selector(response).xpath('//*[@class="artitleList"]/ul/li')
            urls = Selector(response).xpath('//*[@class="PageBox"]/div[@id="pageNoDiv"]/a[@class="f12"]/@href').extract()
            next_page = urls[urls.__len__()-1]

            page_urls = []
            if next_page in page_urls:
                next_page = None
            else:
                page_urls.append(next_page)

            for question in questions:
                item = EItem()
                item['title'] = question.xpath('div/p[@class="title"]/a/text()').extract_first()
                item['description'] = question.xpath('div/p[@class="info"]/text()').extract_first()
                item['releasetime'] = question.xpath('div/p[@class="time"]/text()').extract_first()
                item['releasetime'] = '2017-' + item['releasetime'].split(' ')[0].split('月')[0] + '-' + \
                                  item['releasetime'].split(' ')[0].split('月')[1].split('日')[0] + ' ' + item['releasetime'].split(' ')[1]
                print(item['releasetime'])
                item['label'] = []

                if self.juge(item['releasetime'], 0, 0, 0):
                    with open('E03世界经济.csv', 'rU') as f:
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
        tomorrow = now.replace(day = now.day - day_time, hour = now.hour - hour_time, minute = now.minute - minute_time)
        print(day_time,tomorrow,now,'E03')
        if day_time == 0 and hour_time == 0 and minute_time == 0:
            return True;
        else:
            if tomorrow < timeTuple :
                return True
            else:
                return False




