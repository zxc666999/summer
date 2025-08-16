



import json

# 全局变量存储最后结果
last_result = None

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

def get_last_result():
    global last_result
    return last_result['result'] if last_result else None