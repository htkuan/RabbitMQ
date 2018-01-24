# Run RabbitMQ
```
run rabbitmq
$ docker run -d -p 5672:5672 --name my-rabbit rabbitmq:3
into rabbitmq container
$ docker exec -it my-rabbit bash
```

## tutorial 1
```
in shell 1
$ python receive.py
in shell 2
$ python send.py
```

## tutorial 2
```angular2html
in shell 1,2,3....
$ python worker.py
in new shell (repeat to sand task)
$ python new_task.py
```
## tutorial 3
其實producer並不是直接吧message送到queue裡面,或是說producer
根本不知道message會被送到哪個queue中,producer只會把message送給
"exchange",而exchange做的事情也很簡單,就是接收producer的
message然後把message push給queue,根據"exchange type" exchange
可以知道message要送到哪個queue或是多個亦或者是discard message.
有四種exchange type(direct, topic, headers and fanout)

* fanout: 把message廣播到所有queue

```
in shell 1
$ python receive_logs.py
or save logs to a file
$ python receive_logs.py > logs_from_rabbit.log

in shell 2
$ python emit_log.py
```

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
