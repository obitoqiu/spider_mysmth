import re
from lxml import etree
import requests
import scrapy
from scrapy.selector import Selector
from ..items import MysmthItem


class SmthSpider(scrapy.Spider):
    name = 'smth'
    allowed_domains = ['mysmth.net']
    start_urls = ['https://www.mysmth.net/nForum/board/MilitaryView?ajax&p=%s' % i for i in range(1, 153)]

    def parse(self, response, **kwargs):
        items = MysmthItem()
        selector = Selector(response)
        texts = selector.xpath("//td[@class='title_9']/a/@href").extract()
        page_nums = selector.xpath("//tbody/tr/td[contains(@class, 'title_11')][3]/text()").extract()
        for i, j in zip(page_nums, texts):
            msg_id = re.search(r'\d+', j)
            msg_id = msg_id.group()
            for t in range(1, int(i) // 10 + 2):
                url = "https://www.mysmth.net" + j + "?ajax&p=%s" % t
                res1 = requests.get(url)
                html1 = etree.HTML(res1.text)
                names = html1.xpath("//div[@class='a-u-uid']")
                contents = html1.xpath("//td[@class='a-content']")
                floor = 0
                if len(names) != 0 and len(contents) != 0 and len(names) == len(contents):
                    for m, n in zip(names, contents):
                        name = m.xpath("text()")[0]
                        content = ""
                        for k in n.xpath("p/text()"):
                            if "发信人" not in k and " 标题" not in k and "】" not in k and " 发信站" not in k \
                                    and "题:" not in k and "--" not in k and len(str(i).strip()) > 0:
                                content += str(k).strip()
                            elif "发信站" in k:
                                pub_time = k[k.index("(")+1: k.index(")")].replace("\xa0\xa0", "")
                        content = ",".join(content.split("\n")).replace("\xa0\xa0", ",")
                        new_content, num = re.subn('<br>', ',', content)
                        if t == 1 and floor == 0:
                            items["msgid"] = msg_id
                            items["refid"] = -1
                        else:
                            items["msgid"] = -1
                            items["refid"] = msg_id

                        items["pubtime"] = pub_time
                        items["name"] = name
                        items["content"] = new_content
                        floor += 1
                        yield items
