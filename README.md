# RabbitMQ

RabbitMQ 是一個實現 AMQP 協定標準的開放原始碼訊息代理(message broker)和佇列伺服器, 

伺服器端用 Erlang 編寫, 支持多種客戶端, 常被運用在許多網站組件的解耦！

[AMQP 協定](https://en.wikipedia.org/wiki/Advanced_Message_Queuing_Protocol)

[rabbitmq github](https://github.com/rabbitmq)

# Install and Run RabbitMQ

Docker:
```
download image
$ docker pull rabbitmq:3-management

run rabbitmq
$ docker run -d -p 5672:5672 -p 8080:15672 --name my-rabbit rabbitmq:3-management

stop rabbitmq
$ docker stop my-rabbit

into rabbitmq container
$ docker exec -it my-rabbit bash
```

rabbitmq:3-management 這個版本提供 RabbitMQ 的 GUI 管理介面!

可以訪問這個網址[http://localhost:8080](http://localhost:8080)

預設帳號密碼為 guest/guest

若想設置 預設帳號密碼可以加上 RABBITMQ_DEFAULT_USER 和 RABBITMQ_DEFAULT_PASS 參數
```
$ docker run -d -p 5672:5672 -p 8080:15672 --name my-rabbit -e RABBITMQ_DEFAULT_USER=user -e RABBITMQ_DEFAULT_PASS=password rabbitmq:3-management
```

*rabbitmq也提供api接口*

可以訪問這個網址[http://localhost:8080/api](http://localhost:8080/api)

Mac 用戶也可以用 Homebrew 下載安裝:
```
Before installing make sure you have the latest brews
$ brew update

install RabbitMQ server
$ brew install rabbitmq
```

[官方下載頁面](https://www.rabbitmq.com/download.html)

# RabbitMQ 虛擬主機

RabbitMQ server 可以自己建立虛擬主機(vhost), 擁有自己的 Queue、exchange 和 binding

不同的 vhost 完全隔離獨立, 可以避免命名問題, 如果不建立 vhost 是用預設的虛擬主機 "/"

使用預設的帳號密碼 guest/guest

利用RabbitMQ 指令建立 vhost 並給定 permission
```
先進入 rabbitmq container
$ docker exec -it my-rabbit bash

加入 user
$ rabbitmqctl add_user username password

加入 vhost
$ rabbitmqctl add_vhost host_name

設置 permission
$ rabbitmqctl set_permission -p host_name username ".*" ".*" ".*"
最後三個設定分別代表 Queue 和 exchange 的 (建立刪除) (發布訊息) (消費訊息)

設置登入 GUI 管理介面許可
$ rabbitmqctl set_user_tags username administrator
```

若想直接開啟docker 就建立預設的vhost可以給定 RABBITMQ_DEFAULT_VHOST 參數
```
$ docker run -d -p 5672:5672 -p 8080:15672 --name my-rabbit -e RABBITMQ_DEFAULT_VHOST=my_vhost -e RABBITMQ_DEFAULT_USER=user -e RABBITMQ_DEFAULT_PASS=password rabbitmq:3-management
```

# Python client pika

本篇教學以 python 套件 pika 作為客戶端應用

python version: 3.6.4

install pika:
```
$ pip install pika
```

[pika api reference](https://pika.readthedocs.io/en/latest/index.html)

# RabbitMQ workflow

```
| 1. 訊息發布者(Producer): Message 的產生者
         
| 2. 交換機(Exchange): 交換機作為路由把從 Producer 接到的 Message 根據路由規則發送到綁定的 Queue

| 3. 佇列(Queue): 把訊息投遞給有訂閱的此佇列的 Consumer
    
| 4. 訊息訂閱者(Consumer): Consumer 也可以主動到佇列獲取 Message
``` 

# tutorial 1 (Hello World!)

producer (sender) -> queue (hello) -> consumer (receiver)

基本流程：
1. 建立連線
2. producer發送message到exchange, 再透過exchange把message送到指定的queue
3. consumer從queue中接收message

* Channel: Channel是RabbitMQ的最重要的一個API接口, 
我們大部分的業務操作是在Channel這個接口中完成的, 包括定義Queue、定義Exchange、綁定Queue與Exchange、發布消息等。

```
in shell 1
$ python receive.py

in shell 2
$ python send.py
```

# tutorial 2 (Work Queues)

producer -(tasks)-> task_queue -(tasks)-> multiple workers

可以開啟多個workers, 從queue中拿取task做consuming的動作


* Message acknowledgment: 參考worker.py中的註解
* Message durability: 參考new_task.py中的註解
* Fair dispatch: 參考worker.py中的註解

```
in shell 1,2,3....(create multiple workers)
$ python worker.py

in new shell (repeat to sand task)
$ python new_task.py
```

# tutorial 3 (Publish/Subscribe)

其實producer並不是直接吧message送到queue裡面,

或是說producer根本不知道message會被送到哪個queue中,

producer只會把message送給"exchange",而exchange做的事情也很簡單,

就是接收producer的message然後把message push給queue,

根據"exchange type" exchange可以知道message要送到哪個queue或是多個亦或者是discard message.

有四種exchange type(direct, topic, headers and fanout)

* fanout: 把message廣播到所有queue
* direct: 把message送到綁定的queue(queue_bind綁定routing_key,basic_publish指定routing_key送)
* topic: 把message送到綁定的queue(但是可以綁定多個條件)
* header: 比對AMQP的表頭而非routing_key,與direct使用上差不多,只有效能上的差異

示範 fanout
```
in shell 1
$ python receive_logs.py

or save logs to a file
$ python receive_logs.py > logs_from_rabbit.log

in shell 2
$ python emit_log.py
```
# tutorial 4 (Routing)
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
# tutorial 5 (Topics)
雖然exchange的fanout可以廣播,direct可以選擇要丟的queue,但是卻不能根據不同標準來丟message

像是log系統可以根據嚴重程度區分(info, error),但也可以根據產生的元件分別(auth, cron)

這時就需要第三個exchange type: topic 

topic如何做到,其實與direct差不多是利用routing_key的match

不過這次 routing_key 可以指定多個值(basic_publish跟queue_bind都可以)

取值規則 '\<xxx\>.\<aaa\>' or '\<xxx\>.\<zzz\>.\<aaa\>' 最多255bytes

\* 星號代表可替帶一個<> and # 代表可以替代一個或多個<>

ex. basic_publish 發給exchange routing_key='a.b.c'

| queue name | routing_key | received |
| :--------: | :---------: | :-----: |
|  queue 1   | 'g.b.*' |    X    |
|  queue 2   | '*.b.c' |    O    |
|  queue 3   | 'a.#' |    O    |
|  queue 4   | 'q.#' and 'a.b.*'|    O    |

```
To receive all the logs run:
$ python receive_logs_topic.py "#"

To receive all logs from the facility "kern":
$ python receive_logs_topic.py "kern.*"

if you want to hear only about "critical" logs:
$ python receive_logs_topic.py "*.critical"

You can create multiple bindings:
$ python receive_logs_topic.py "kern.*" "*.critical"

Receive nothing
$ python receive_logs_topic.py "nothing.*"

emit a log with a routing key "kern.critical" type:
$ python emit_log_topic.py "kern.critical" "A critical kernel error"
```


# tutorial 6 (Remote procedure call)
在 tutorial 2 中用了多個worker來consuming work_queue裡面的tasks,

但如果需要在遠端機器上跑程式然後等待結果,該怎麼在RabbitMQ上實現這個RPC系統呢?

工作模式由client發起Request到rpc_queue,由RPC worker(aka. server)來處理這個Request,

並且將處理過後的Reply根據Request的reply_to,將Reply發到callback_queue,

然而這樣client從callback_queue接回Reply並無法判別是哪個Request的Reply,

所以在Request給上correlation_id,並且回傳Reply也標記上同樣的id,來讓client知道!

client -> Request(reply_to=amqp.gen-X, correlation_id=abc) -> rpc_queue -> server
   
client <- Reply(correlation_id=abc) <- callback_queue(amqp.gen-X) <- server


```
start the RPC server
$ python rpc_server.py

To request a fibonacci number run the client
$ python rpc_client.py
```

## RabbitMQ command
```
list all users
$ rabbitmqctl list_users

list all vhost
$ rabbitmqctl list_vhost

list all queue
$ rabbitmqctl list_queues

print the messages_unacknowledged field
$ rabbitmqctl list_queues name messages_ready messages_unacknowledged

list the exchanges on the server
$ rabbitmqctl list_exchanges

list existing bindings using
$ rabbitmqctl list_bindings
```
## RabbitMQ Cluster
(rabbitmq 叢集文檔)[https://www.rabbitmq.com/clustering.html]

啟動 cluster
```
cd cluster/
docker-compose up -d
```

關閉
```
docker-compose down
```