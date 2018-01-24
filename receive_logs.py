import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')

# 如果沒有給queue命名(queue_declare不給queue參數),
# rabbit會給一個random queue name ex. amq.gen-JzTY20BRgKO-HjmUJj0wLg.
# exclusive=True則是在consumer disconnect時,這個queue會被刪掉
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue  # 會存一個 random queue name

# exchange和queue之間的關係被稱為binding
channel.queue_bind(exchange='logs',
                   queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] %r" % body)


channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
