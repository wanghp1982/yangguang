# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
logger = logging.getLogger(__name__)
import re
class YangguangPipeline(object):
    def process_item(self, item, spider):
        # print(item)
        item["askTime"] = self.process_content(item["askTime"])
        logger.warning("-" * 10)
        return item
    def process_content(self,askTime):
        askTime = [re.sub(r"\n","",i) for i in askTime]
        askTime = [i for i in askTime if len(i)>0]
        return askTime
