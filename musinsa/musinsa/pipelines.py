# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import logging

# 设置日志级别为 WARNING，这样就不会输出 DEBUG 信息了
logging.basicConfig(level=logging.WARNING)

# 如果想要更加控制，可以设置 pika 的日志处理器：
logging.getLogger('pika').setLevel(logging.WARNING)

class MusinsaPipeline:
    def process_item(self, item, spider):
        return item


import pika
import json


class MQPipeline:
    def __init__(self, mq_host, queue_name, mq_user, mq_password, mq_port):
        self.mq_host = mq_host
        self.queue_name = queue_name
        self.mq_user = mq_user
        self.mq_password = mq_password
        self.mq_port = mq_port  # 使用端口号
        self.connection = None
        self.channel = None

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        # 从 Scrapy 配置中获取 MQ 连接信息
        mq_host = crawler.settings.get('MQ_HOST')
        mq_port = crawler.settings.get('MQ_PORT')  # 获取端口号
        queue_name = crawler.settings.get('QUEUE_NAME')
        mq_user = crawler.settings.get('MQ_USER')  # 默认值是admin
        mq_password = crawler.settings.get('MQ_PASSWORD')  # 默认值是summer
        return cls(mq_host, queue_name, mq_user, mq_password, mq_port)  # 传递端口号

    def open_spider(self, spider):
        # 创建身份验证信息
        credentials = pika.PlainCredentials(self.mq_user, self.mq_password)

        # 建立连接并传入认证信息
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.mq_host,
                port=self.mq_port,  # 使用端口号
                credentials=credentials
            )
        )
        self.channel = self.connection.channel()

        # 声明队列
        self.channel.queue_declare(queue=self.queue_name, durable=True)

    # def close_spider(self, spider):
    #     # 关闭连接
    #     if self.connection:
    #         self.connection.close()

    def process_item(self, item, spider):
        # 将 item 转为 JSON 格式并发送到 MQ 队列
        item_json = json.dumps(dict(item))
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            body=item_json,
            properties=pika.BasicProperties(
                delivery_mode=2,  # 确保消息持久化
            )
        )
        return item


