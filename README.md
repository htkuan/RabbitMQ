# Run RabbitMQ
```
$ docker run -d -p 5672:5672 --name my-rabbit rabbitmq:3
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
