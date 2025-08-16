import pika
import json

# 全局变量存储最后结果
last_result = None

# 消息处理函数
def process_message(message):
    global last_result
    message = json.loads(message.decode()) if isinstance(message, bytes) else message
    # 检查消息是否更新（假设消息有 'id' 字段）
    if last_result is None or message.get('id') != last_result.get('id'):
        # 新消息，处理并更新结果
        result = f"处理了 {message}"
        last_result = {'id': message.get('id'), 'result': result}
    else:
        # 重复使用上一次结果
        result = last_result['result']
    return result

# 回调函数处理队列消息
def callback(ch, method, properties, body):
    result = process_message(body)
    print(f"处理结果: {result}")
    # 确认消息
    ch.basic_ack(delivery_tag=method.delivery_tag)

# 连接参数
credentials = pika.PlainCredentials('admin', 'summer')
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', credentials))
channel = connection.channel()

# 声明队列
channel.queue_declare(queue='scrapy_queue', durable=True)

# 设置消费者
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='scrapy_queue', on_message_callback=callback)

print("等待消息。按 CTRL+C 退出")
channel.start_consuming()