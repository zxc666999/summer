import pika
import json


def process_message(message):
    # 处理消息的逻辑
    print(f"Processing message: {message}")
    return message.get("data", "") + "_processed"


def consume_message_from_queue(queue_name):
    # 创建凭证，使用用户名和密码
    credentials = pika.PlainCredentials('admin', 'summer')

    # 连接到 RabbitMQ 服务，指定端口号为 5672
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            'localhost',  # RabbitMQ 主机
            5672,  # 端口号
            '/',  # 虚拟主机，默认是 '/'
            credentials  # 身份验证
        )
    )

    channel = connection.channel()

    # 确保队列存在，并且设置 durable 参数来确保一致性
    channel.queue_declare(queue=queue_name, durable=True)  # 设置持久化

    def callback(ch, method, properties, body):
        # 消费者接收到的消息体是字节流，转换为字典
        message = body
        result = process_message(message)
        print(f"处理结果: {result}")

        # 可以根据需求更新返回的值，这里可以模拟更新
        updated_result = result + "_updated"
        print(f"Updated result: {updated_result}")

        # 确认消息已被处理
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # 设置消费者处理的回调函数
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    print('Waiting for messages. To exit press CTRL+C')
    # 开始消费
    channel.start_consuming()


# 消费者示例
if __name__ == '__main__':
    consume_message_from_queue('scrapy_queue')
