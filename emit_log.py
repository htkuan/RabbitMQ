import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs',  # exchange name
                         exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or "info: Hello World!"
# 先前使用default exchange也就是把exchange命名為" "(空字串),
# 這樣message會被送到routing_key指定的queue(如果存在)
channel.basic_publish(exchange='logs',
                      routing_key='',  # 現在使用了fanout,所以不需要指定queue
                      body=message)
print(" [x] Sent %r" % message)
connection.close()
