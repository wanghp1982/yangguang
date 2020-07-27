# -*- coding: utf-8 -*-
import scrapy
from yangguang.items import YangguangItem
import logging
logger = logging.getLogger(__name__)
class YgSpider(scrapy.Spider):
    name = 'yg'
    allowed_domains = ['sun0769.com']
    start_urls = ['http://wz.sun0769.com/political/index/supervise?page=1']
    base_url = "http://wz.sun0769.com"
    def parse(self, response):
        tr_list = response.xpath('//div[@class="width-12"]//ul[@class="title-state-ul"]/li')
        for tr in tr_list:
            item = YangguangItem()
            item["title_NO"] = tr.xpath('./span[@class="state1"]/text()').extract_first()
            item["status"] = tr.xpath('./span[@class="state2"]/text()').extract_first()
            item["title"] = tr.xpath('./span[@class="state3"]/a/text()').extract_first()
            item["title_url"] = tr.xpath('./span[@class="state3"]/a/@href').extract_first()
            item["title_url"] = self.base_url +item["title_url"]
            item["askTime"] = tr.xpath('./span[@class="state4"]/text()').extract_first()
            item["answerTime"] = tr.xpath('./span[@class="state5 "]/text()').extract_first()
        # print(item)
            logger.warning(item)
            yield scrapy.Request(item["title_url"],
                                 callback=self.parse_detail,
                                 meta={"item":item}
                                 )
            next_url = response.xpath('//div[@class="mr-three paging-box"]//a[@class="arrow-page prov_rota"]/@href').extract_first()
            if next_url is not None:
                yield scrapy.Request(self.base_url+next_url,callback=self.parse
                                     )

    def parse_detail(self,response):
        item = response.meta["item"]
        item["content_title"] = response.xpath('//div[@class="mr-three"]/p[@class="focus-details"]/text()').extract_first()
        item["content_ask"] = response.xpath('//div[@class="mr-three"]/div[@class="details-box"]/pre/text()').extract_first()
        item["content_answer"] = response.xpath('//div[@class="mr-five"]/div[@class="gf-reply mr-two"]/pre/text()').extract_first()
        logger.warning(item)
        yield item