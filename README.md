# Run RabbitMQ
```
run rabbitmq
$ docker run -d -p 5672:5672 --name my-rabbit rabbitmq:3
into rabbitmq container
$ docker exec -it my-rabbit bash
```

## tutorial 1 (Hello World!)
```
in shell 1
$ python receive.py
in shell 2
$ python send.py
```

## tutorial 2 (Work Queues)
```angular2html
in shell 1,2,3....
$ python worker.py
in new shell (repeat to sand task)
$ python new_task.py
```
## tutorial 3 (Publish/Subscribe)
其實producer並不是直接吧message送到queue裡面,或是說producer
根本不知道message會被送到哪個queue中,producer只會把message送給
"exchange",而exchange做的事情也很簡單,就是接收producer的
message然後把message push給queue,根據"exchange type" exchange
可以知道message要送到哪個queue或是多個亦或者是discard message.
有四種exchange type(direct, topic, headers and fanout)

* fanout: 把message廣播到所有queue
* direct: 把message送到綁定的queue(queue_bind綁定routing_key,basic_publish指定routing_key送)

```
in shell 1
$ python receive_logs.py
or save logs to a file
$ python receive_logs.py > logs_from_rabbit.log

in shell 2
$ python emit_log.py
```
## tutorial 4 (Routing)
exchange type = direct 的 exchange下

queue_bind綁定讓exchange綁定queue的routing_key(有點像路牌)

basic_publish時producer只能把message給exchange並指定routing_key

來告訴exchange往哪裡丟message,並不是直接往某個名字的queue丟message

***exchange同一個routing_key可以綁定多的queue(就是都會一起收到)***

```
in shell 1 (see all the log messages on your shell)
$ python receive_logs_direct.py info warning error
save only 'warning' and 'error' (and not 'info') log messages to a file
$ python receive_logs_direct.py warning error > logs_from_rabbit.log

in shell 2 (send error message)
$ python emit_log_direct.py error "Run. Run. Or it will explode."
```
## tutorial 5 (Topics)

## tutorial 6 (RPC)


## RabbitMQ command
```
list all queue
$ rabbitmqctl list_queues
print the messages_unacknowledged field
$ rabbitmqctl list_queues name messages_ready messages_unacknowledged
list the exchanges on the server
$ rabbitmqctl list_exchanges
list existing bindings using
$ rabbitmqctl list_bindings
```
