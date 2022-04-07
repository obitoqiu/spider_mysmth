# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json


class MysmthPipeline:
    def __init__(self):
        self.f = open("data.txt", "a", encoding='utf-8')

    def process_item(self, item: object, spider) -> object:
        #print(str(item["name"]) + ":" + str(item["content"]) + "\n")
        #self.f.write(str(item["name"]) + ":" + str(item["content"]) + "\n")
        print(item, "\n")
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.f.write(lines)
        return item

    def __del__(self):
        self.f.close()
