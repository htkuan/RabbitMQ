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

## Best Practice

[cloud amqp ref](https://www.cloudamqp.com/blog/tag/guide.html)

* max size of one single message
  * size limit in RabbitMQ is 2GB
  * recommend sending messages smaller than 128MB
* Too many queued messages, high message rate during a long time or frequently opened and closed connections have been the most common reasons for high CPU usage.
* CPU 80% up alarm; Memory 90% up alarm
* Most common errors/mistakes cause High CPU & Memory usage
  1. TOO MANY QUEUED MESSAGES -> high RAM usage(因為訊息會先 cache 在 memory)
  2. TOO MANY UNACKNOWLEDGED MESSAGES -> high RAM usage(All unacknowledged messages have to reside in RAM on the servers.)
  3. TOO HIGH MESSAGE THROUGHPUT -> If CPU User time is high, it could be due to high message throughput.
  4. TOO MANY QUEUES
  5. FREQUENTLY OPENING AND CLOSING CONNECTIONS -> If CPU System time is high, you should check how you are handling your connections.
  6. CONNECTION OR CHANNEL LEAK

* lazy queues: 啟用的話，訊息會先寫進 disk，需要時才寫入 memory 使用，好處是節省 memory，壞處是 disk I/O 變多，會變慢
* FOR PYTHON CELERY: https://www.cloudamqp.com/docs/celery.html
    * 關掉一些不必要的訊息傳遞，跟心跳設定 
    * disable the result backend(CELERY_RESULT_BACKEND = None)
* Benchmark testing: https://www.cloudamqp.com/blog/2016-11-18-load-testing-and-performance-measurements-rabbitmq.html
* persist messages: 
  * Declared your queue as durable: 目的是 RabbitMQ 重啟時，會保留原本的 queue，但跟 queue 裡面的訊息沒關係
  * Set message delivery mode to persistent: 訊息 delivery 時分為 persistent mode 跟 transient mode。
* Keep your queue short (if possible): < 10000
* Enable lazy queues to get predictable performance
  * 如果 worker 消費跟不上，建議啟用，可以減少 RAM 的使用，如批次作業
  * 如果需要高吞吐量，則建議禁用，因為 disk I/O 會拖慢速度
* Limit queue size with TTL or max-length
  * Another recommendation for applications that often get hit by spikes of messages, and where throughput is more important than anything else, is to set a max-length on the queue.
  * This keeps the queue short by discarding messages from the head of the queue so that it never gets larger than the max-length setting.
* Number of queues
  * Queues are single-threaded in RabbitMQ 
  * one queue can handle up to about 50 thousand messages
  *  You will achieve better throughput on a multi-core system if you have multiple queues and consumers and if you have as many queues as cores on the underlying node(s).
  * RabbitMQ management interface 要收集資訊，如果太多 queue，會拖慢速度
* Split your queues over different cores
  * https://www.cloudamqp.com/blog/2017-12-29-part1-rabbitmq-best-practice.html#split-your-queues-over-different-cores
* Don’t set your own names on temporary queues: 如果只是暫時的 queue，就直接用系統給得隨機名字
* Auto-delete queues you are not using: 有可能因為客戶端的錯誤創建很多 queue 而影響效能
  * Set a TTL policy in the queue: 設置幾天後自動刪除沒有被消費的 queue
  * Set auto-delete queue: 會在 queue 失去最後一個 connection 得時候刪掉 queue
  * exclusive queue: deleted when their declaring connection is closed or gone
* Set limited use of priority queues: 優先級跟會佔用資源，通常5以下就夠了
* RabbitMQ message size and types: 雖然發送巨大的訊息不是好的作法，但是多個小訊息會更慢，所以適時的把多個小訊息捆綁成一個較大的訊息發送會優化效能
* Don’t share channels between threads
* Don’t open and close connections or channels repeatedly
* Separate connections for publisher and consumer
* A large number of connections and channels might affect the RabbitMQ management interface performance
* Acknowledgements and Confirms