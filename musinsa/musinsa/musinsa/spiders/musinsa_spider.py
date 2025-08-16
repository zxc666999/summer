




import json
import re
import scrapy
from loguru import logger
from scrapy import cmdline
from musinsa.musinsa_id import get_id
from musinsa.main import callback
class MusinsaSpiderSpider(scrapy.Spider):
    name = 'musinsa_spider'
    # allowed_domains = ['www.musinsa.com']
    # start_urls = ['http://www.musinsa.com/']



    def start_requests(self):
        get_id = ['104015004']
        for id in get_id:
            url = f'https://api.musinsa.com/api2/dp/v1/plp/goods?gf=A&category={id}&size=60&caller=CATEGORY&page=1'
            yield scrapy.Request(url, callback=self.get_parse, meta={'page': 1,'id':id}, dont_filter=False)

    def get_parse(self, response, **kwargs):

        page = response.meta['page']
        id = response.meta['id']
        logger.info(f'{id}正在处理第{page}页')
        data_list = response.json().get('data').get('list')
        # 如果没有内容，则退出爬取
        if not data_list:
            logger.info(f'没有更多的页面，结束爬取')
            return

        for node in data_list:
            goodsLinkUrl = node['goodsLinkUrl']
            yield scrapy.Request(url=goodsLinkUrl)

        # 翻页：如果有数据，则请求下一页
        next_page = page + 1
        next_url = f'https://api.musinsa.com/api2/dp/v1/plp/goods?gf=A&category={id}&size=60&caller=CATEGORY&page={next_page}'
        yield scrapy.Request(next_url, callback=self.get_parse,  meta={'page': next_page, 'id': id}, dont_filter=False)

    def parse(self, response,**kwargs):
        res = re.findall('window.__MSS__.product.state = (.*?)};',response.text)[0] + "}"
        # print(res)
        red_dict= json.loads(res)
        item = {}
        item['goodsNo'] = red_dict['goodsNo']
        item['goodsNm'] = red_dict['goodsNm']
        data = {
            'callback':callback,
            'item':item
        }
        if callable(callback):
            callback(item)
        print(data)
        yield data





if __name__ == '__main__':
    cmdline.execute('scrapy crawl musinsa_spider'.split())