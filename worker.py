import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# channel.queue_declare(queue='task_queue')
channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


# Message acknowledgment
# 為了要確保message一定能收到(ex. consumer dies), ack設定在worker必須回傳delivery_tag,
# 給server(收到後server才會從queue中刪除此訊息),否則server會重新發出此message
# ---------- no_ack ---------------------------
# def callback(ch, method, properties, body):
#     print(" [x] Received %r" % body)
#     time.sleep(body.count(b'.'))
#     print(" [x] Done")
#
#
# channel.basic_consume(callback,
#                       queue='hello',
#                       no_ack=True)  # 預設是有ack
# ---------------------------------------------
def callback(ch, method, properties, body):
    print(" [x] Received %r" % (body,))
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)  # 回傳 delivery_tag


# Fair dispatch(通常rabbit只是盲目的把every n-th message to the n-th consumer.)
# 用basic_qos method可以調度worker
# prefetch_count=1 表示一次不能給一個工作者多個消息
# 也就是說直到worker確認處理消息前不給他第二個message,會發給比較不忙的worker
channel.basic_qos(prefetch_count=1)

channel.basic_consume(callback,
                      queue='task_queue')

channel.start_consuming()
