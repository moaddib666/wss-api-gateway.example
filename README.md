# Margay Gateway - Example docker
Example of `MargayGateway` integration with python backend

## Quickstart

Ensure you have `docker` and `docker-compose`
- run `docker-compose up` to start Gateway with Echo backend
  - Wait until all services up and ready - first run may take a while because of long RMQ startup.
  ```shell
  (margayexample-py3.10) moaddib@planetXhost ~/development/wss-api-gateway.example $ docker-compose up 
  Starting wss-api-gatewayexample_rabbitmq_1 ... done
  Starting wss-api-gatewayexample_margay_1   ... done
  Starting wss-api-gatewayexample_backend-service_1 ... done
  Starting wss-api-gatewayexample_client-service_1  ... done
  .....
  backend-service_1  | 2023-02-12 15:49:33,017 - margay.sdk.logger - DEBUG - Creating connection to `amqp://user:bitnami@rabbitmq:5672/`
  backend-service_1  | 2023-02-12 15:49:33,022 - margay.sdk.logger - DEBUG - Setup exchange to `MargayGatewayInbox`
  rabbitmq_1         | 2023-02-12 15:49:33.029556+00:00 [info] <0.588.0> accepting AMQP connection <0.588.0> (172.19.0.3:51370 -> 172.19.0.2:5672)
  rabbitmq_1         | 2023-02-12 15:49:33.032928+00:00 [info] <0.588.0> connection <0.588.0> (172.19.0.3:51370 -> 172.19.0.2:5672): user 'user' authenticated and granted access to vhost '/'
  backend-service_1  | 2023-02-12 15:49:33,033 - margay.sdk.logger - DEBUG - Creating connection to `amqp://user:bitnami@rabbitmq:5672/`
  backend-service_1  | 2023-02-12 15:49:33,034 - margay.sdk.logger - DEBUG - Setup exchange to `MargayGatewayOutbox`
  backend-service_1  | 2023-02-12 15:49:33,035 - margay.sdk.logger - DEBUG - Bind queue `VanillaWorkerQueue` to exchange `MargayGatewayOutbox`
  rabbitmq_1         | 2023-02-12 15:49:33.040083+00:00 [info] <0.594.0> accepting AMQP connection <0.594.0> (172.19.0.3:51372 -> 172.19.0.2:5672)
  backend-service_1  | 2023-02-12 15:49:33,046 - kombu.mixins - INFO - Connected to amqp://user:**@rabbitmq:5672//
  rabbitmq_1         | 2023-02-12 15:49:33.046224+00:00 [info] <0.594.0> connection <0.594.0> (172.19.0.3:51372 -> 172.19.0.2:5672): user 'user' authenticated and granted access to vhost '/'
  ```
  
- run client `docker exec -it wss-api-gatewayexample_client-service_1 python client.py`
  - You will see a prompt where you can type message like:
  ```shell
  (margayexample-py3.10) moaddib@planetXhost ~/development/wss-api-gateway.example $ docker exec -it wss-api-gatewayexample_client-service_1 python client.py
  Send to WSS: 
  ```
  - Let's type `hello world` message:
  ```shell
  Send to WSS: hello world
   -> hello world
   <- "Respond to -> hello world"
  Send to WSS: 
  ```
  In logs of our services we should find something like:
  ```shell
  margay_1           | 2023/02/12 15:51:17 Connection `JohnSnow` added to connection pool
  margay_1           | 2023/02/12 15:51:17 Sending message `{"meta":{"object_id":"JohnSnow","object_type":"client","publisher":"MargayGateway","event":"connected","created":"2023-02-12T15:51:17Z"},"data":{}}` to event bus - &{Sender:MargayGateway Recipient:*}
  backend-service_1  | 2023-02-12 15:51:17,746 - margay.sdk.logger - DEBUG - Received RAW message, body: `b'{"meta":{"object_id":"JohnSnow","object_type":"client","publisher":"MargayGateway","event":"connected","created":"2023-02-12T15:51:17Z"},"data":{}}'`, headers:`{'recipient': '*', 'sender': 'MargayGateway'}`
  backend-service_1  | 2023-02-12 15:51:17,754 - margay.sdk.logger - DEBUG - Message `b87d1924-d60b-4f58-932c-4914b6d6cf2e` was successfully decoded
  backend-service_1  | 2023-02-12 15:51:17,757 - margay.sdk.logger - DEBUG - Setup producer with Exchange MargayGatewayInbox(direct) serialized by `json`
  backend-service_1  | 2023-02-12 15:51:17,759 - margay.sdk.logger - DEBUG - Publishing RAW message body:`Respond to -> {"meta":{"object_id":"JohnSnow","object_type":"client","publisher":"MargayGateway","event":"connected","created":"2023-02-12T15:51:17Z"},"data":{}}`, headers: `{'sender': '03a82c325619', 'recipient': 'MargayGateway'}`
  margay_1           | 2023/02/12 15:51:17 Received a message: body:`"Respond to -> {\"meta\":{\"object_id\":\"JohnSnow\",\"object_type\":\"client\",\"publisher\":\"MargayGateway\",\"event\":\"connected\",\"created\":\"2023-02-12T15:51:17Z\"},\"data\":{}}"` id:`` headers:`map[recipient:MargayGateway sender:03a82c325619]`
  margay_1           | 2023/02/12 15:51:17 Found message in event bus for user `MargayGateway`
  margay_1           | 2023/02/12 15:51:17 Reject message due to invalid recipient `MargayGateway` is internal client
  backend-service_1  | 2023-02-12 15:51:17,770 - margay.sdk.logger - DEBUG - Message `b87d1924-d60b-4f58-932c-4914b6d6cf2e` was successfully processed
  backend-service_1  | 2023-02-12 15:51:17,776 - margay.sdk.logger - DEBUG - Message `b87d1924-d60b-4f58-932c-4914b6d6cf2e` has been acknowledged
  margay_1           | 2023/02/12 15:53:28 Sending message `hello world` to event bus - &{Sender:JohnSnow Recipient:*}
  backend-service_1  | 2023-02-12 15:53:28,484 - margay.sdk.logger - DEBUG - Received RAW message, body: `b'hello world'`, headers:`{'recipient': '*', 'sender': 'JohnSnow'}`
  backend-service_1  | 2023-02-12 15:53:28,486 - margay.sdk.logger - DEBUG - Message `7bfe5c09-e77d-4cd1-bf8f-2f4bde7540fb` was successfully decoded
  backend-service_1  | 2023-02-12 15:53:28,489 - margay.sdk.logger - DEBUG - Setup producer with Exchange MargayGatewayInbox(direct) serialized by `json`
  backend-service_1  | 2023-02-12 15:53:28,490 - margay.sdk.logger - DEBUG - Publishing RAW message body:`Respond to -> hello world`, headers: `{'sender': '03a82c325619', 'recipient': 'JohnSnow'}`
  margay_1           | 2023/02/12 15:53:28 Received a message: body:`"Respond to -> hello world"` id:`` headers:`map[recipient:JohnSnow sender:03a82c325619]`
  margay_1           | 2023/02/12 15:53:28 Found message in event bus for user `JohnSnow`
  margay_1           | 2023/02/12 15:53:28 Sent message to user `JohnSnow`
  backend-service_1  | 2023-02-12 15:53:28,498 - margay.sdk.logger - DEBUG - Message `7bfe5c09-e77d-4cd1-bf8f-2f4bde7540fb` was successfully processed
  backend-service_1  | 2023-02-12 15:53:28,499 - margay.sdk.logger - DEBUG - Message `7bfe5c09-e77d-4cd1-bf8f-2f4bde7540fb` has been acknowledged
  ```
