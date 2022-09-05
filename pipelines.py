# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from openpyxl import Workbook


class RegulationsPipeline:
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws_comment = self.wb.create_sheet("comment")

    def process_item(self, item, spider):
        if item.type=='regulation':
            self.ws.append([item['rid'],item['title'],item['postDate']])
        else:
            self.ws_comment.append([item['cid'], item['comment'], item['postDate'],item['poster']])
        return item

    def __del__(self):
        self.wb.save('test.xlsx')