import logging
import os
import socket
import sys

from margay.sdk.config import Config
from margay.sdk.logger import SDKLogger
from margay.sdk.protocol import RawMessage
from margay.sdk.publisher import Publisher
from margay.sdk.subscriber import Subscriber


class SimpleWorker(Subscriber):
    publisher: Publisher

    def __init__(self, pub, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.publisher = pub

    def process(self, message: RawMessage):
        response = f"Respond to -> {message.body}"
        self.publisher.publish_raw(
            response,
            sender=socket.gethostname(),
            recipient=message.headers[Config.protocol.sender],
        )


if __name__ == "__main__":

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    SDKLogger.setLevel(logging.DEBUG)
    Config.set("queue", "VanillaWorkerQueue")
    Config.set("dsn", os.getenv("MARGAY_TRANSPORT_DSN"))
    publisher = Publisher()
    worker = SimpleWorker(publisher)
    worker.run()
