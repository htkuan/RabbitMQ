import sys
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Message durability
# 雖然有ack機制可以確保接收者收到message,但是要是server直接掛掉,
# 消息還是會直接掰掉,所以可以在declare的時候,加上durable=True(worker也要加)
# 所以現在task_queue 這個queue 即使server重啟, 訊息也不會不見
# it may be just saved to cache and not really written to the disk!!
# If you need a stronger guarantee about message persistence
# then you can use publisher confirms.
# channel.queue_declare(queue='task_queue')
channel.queue_declare(queue='task_queue', durable=True)

message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=message,
                      properties=pika.BasicProperties(
                          delivery_mode=2,  # make message persistent
                      ))
print(" [x] Sent %r" % message)
