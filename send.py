import pika

# establish a connection with RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# create a hello queue
channel.queue_declare(queue='hello')

# In RabbitMQ a message can never be sent directly to the queue,
# it always needs to go through an "exchange".

# use a default exchange identified by an empty string.
# This exchange is special
# ‒ it allows us to specify exactly to which queue the message should go.
# The queue name needs to be specified in the routing_key parameter:
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')

print(" [x] Sent 'Hello World!'")
connection.close()
