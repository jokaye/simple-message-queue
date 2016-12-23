# -*- coding: UTF-8 -*-
import json

# The queue prefix in redis key.
QUEUE_PREFIX = 'msg_u'

# Max messages count to limited per user.
MAX_QUEUE_SIZE = 1000


# Use singleton to make sure only one Queue instance in our system,
# and not abuse the redis connections. 
class Singleton(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance[cls]


class MessageQueue(object):
    __metaclass__ = Singleton

    def __init__(self, redis_ins):
        self.queue_ins = redis_ins
    
    def user_key(self, user_id):
        return '%s_%s' % (QUEUE_PREFIX, user_id)

    def get_messages(self, user_id, page_size):
        data = self.queue_ins.lrange(self.user_key(user_id), 0, page_size - 1)
        return [json.loads(d) for d in data]

    def push_message(self, user_id, message):
        """
        The step of push message to queue:
          First:  Push message to user message queue.
          Second: Check the queue size has or not over limit max queue size,
                  otherwise trim the queue.
        """
        self.queue_ins.rpush(self.user_key(user_id), json.dumps(message))

        current_queue_size = self.queue_ins.llen(self.user_key)
        over_size = current_queue_size - MAX_QUEUE_SIZE
        if over_size > 0:
            self.queue_ins.ltrim(self.user_key, over_size, -1)
        return True

    def ack_messages(self, user_id, last_position, msg_id):
        """
        Through position and msg_id to check exactly position last messages return.
        If the message is found, remove the before position messages as read.
        """
        data = self.queue_ins.lrange(self.user_key(user_id), last_position - 1, last_position - 1)
        if data:
            message = json.loads(data[0])
            if 'msg_id' in message and message['msg_id'] == msg_id:
                self.queue_ins.ltrim(self.user_key(user_id), last_position, -1)
                return True
        return False
