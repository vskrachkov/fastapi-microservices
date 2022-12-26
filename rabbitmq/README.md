### Installed plugins:
* rabbitmq_prometheus
* rabbitmq_web_stomp
* rabbitmq_stomp
* rabbitmq_management
* rabbitmq_web_dispatch
* rabbitmq_management_agent

### rabbit_stomp 
default user: `guest/guest`

### Ports
| Service                  | Internal port |
|--------------------------|---------------|
| Management plugin        | 15672         |
| STOMP TCP listener       | 61613         |
| rabbit_web_stomp         | 15674         |
| AMQP TCP listener        | 5672          |
| Prometheus metrics: HTTP | 15692         |

The STOMP specification does not prescribe what kinds of destinations a broker must support, 
instead the value of the destination header in SEND and MESSAGE frames is broker-specific. 
The RabbitMQ STOMP adapter supports a number of different destination types:
- /exchange -- `SEND` to arbitrary routing keys and `SUBSCRIBE` to arbitrary binding patterns;
- /queue -- `SEND` and `SUBSCRIBE` to queues managed by the STOMP gateway;
- /amq/queue -- `SEND` and `SUBSCRIBE` to queues created outside the STOMP gateway;
- /topic -- `SEND` and `SUBSCRIBE` to transient and durable topics;
- /temp-queue/ -- create temporary queues (in reply-to headers only).

Read more at https://www.rabbitmq.com/stomp.html
