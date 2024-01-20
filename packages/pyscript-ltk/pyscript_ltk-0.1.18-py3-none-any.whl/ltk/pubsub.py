# LTK - Copyright 2023 - All Rights Reserved - chrislaffra.com - See LICENSE 

import json
import logging
import sys
import time

from ltk import schedule

"""

Implements a publish-subscribe facility.

Note this is a standalone module, not importing anything from LTK.
This allows its use in Workers, which may not want to include any UIs.

A receiver registers for events using "subscribe".
A sender broadcasts events using "publish".

Communication between the main UI and workers is done using the worker sync.

"""

__all__ = [
    "TOPIC_CRITICAL", "TOPIC_INFO", "TOPIC_DEBUG", "TOPIC_ERROR", "TOPIC_WARNING", "TOPIC_CRITICAL",
    "TOPIC_REQUEST", "TOPIC_RESPONSE", "TOPIC_WORKER_RUN", "TOPIC_WORKER_RESULT",
    "publish", "subscribe", "register_worker"
]

TOPIC_INFO = "log.info"
TOPIC_DEBUG = "log.debug"
TOPIC_ERROR = "log.error"
TOPIC_WARNING = "log.warning"
TOPIC_CRITICAL = "log.critical"

TOPIC_REQUEST = "app.request"
TOPIC_RESPONSE = "app.response"
TOPIC_WORKER_RUN = "worker.run"
TOPIC_WORKER_RESULT = "worker.result"

_logger = logging.getLogger('root')
_log_topics = {
    "log.info": _logger.info,
    "log.debug": _logger.debug,
    "log.error": _logger.error,
    "log.warning": _logger.warning,
    "log.critical": _logger.critical,
}

_name = "pubsub_mpy" if "MicroPython" in sys.version else "pubsub_py"
workers = {}
start = time.time()
show_publish = False

class _Message():
    def __init__(self, sender, receiver, topic, data):
        self.sender = sender
        self.receiver = receiver
        self.topic = topic
        self.data = data

class _PubSub():
    def __init__(self):
        self.subscribers = []
        self.queue = {}
   
    def match(self, message, receiver, receiver_topic, handler):
        if message.topic == receiver_topic and message.sender != receiver:
            if isinstance(handler, str):
                workers[handler].sync.handler(message.sender, message.topic, json.dumps(message.data))
            else:
                handler(message.data)
            log = _log_topics.get(message.topic, _logger.info)
            log(f"[Pubsub] {json.dumps(['', message.sender, receiver, message.topic, str(message.data)[:32]])}")
            return True

    def process_queue(self):
        for key, message in list(self.queue.items()):
            del self.queue[key] # remove the message from the queue
            handled = False
            for subscriber in self.subscribers:
                if self.match(message, *subscriber):
                    handled = True
            if not handled:
                self.queue[key] = message # put back the message onto the queue

    def add_to_queue(self, message):
        self.queue[f"{_name}-{time.time()}"] = message

    def publish(self, sender, receiver, topic, data):
        self.add_to_queue(_Message(sender, receiver, topic, data))
        if show_publish:
            _logger.info(f"[Pubsub] {json.dumps(['publish', sender, receiver, topic, str(data)[:32]])}")
        self.process_queue()

    def subscribe(self, name, topic, handler):
        self.subscribers.append([name, topic, handler])
        self.process_queue()


_messenger = _PubSub()
subscribe = _messenger.subscribe
publish = _messenger.publish
    
def worker_publish(sender, receiver, topic, data):
    try:
        data = json.loads(data)
    except Exception as e:
        _logger.error(f"Cannot publish message {receiver}|{topic} for worker {sender}. Error: {e}. Data={data}")

    publish(sender, receiver, topic, data)

def register_worker(name, worker):
    workers[name] = worker
    worker.sync.subscribe = subscribe
    worker.sync.publish = worker_publish
