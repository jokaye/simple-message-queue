from simple_message_queue.message_queue import MessageQueue
from simple_message_queue.message_queue import QUEUE_PREFIX
import redis
import unittest
import uuid


class TestLfuCache(unittest.TestCase):

    def setUp(self):
        self.r = redis.StrictRedis(host='127.0.0.1', port=6379, db=11)
        self.queue = MessageQueue(self.r)
        self.u1 = '1'
        self.u2 = '2'

    def gen_message(self):
        return {'text': 'hello world!', 'msg_id':  uuid.uuid4().hex[:6]}

    def test_insert_message(self):
        ret = self.queue.push_message(self.u1, self.gen_message())
        self.assertEqual(ret, True)

        self.queue.push_message(self.u2, self.gen_message())
        self.assertEqual(ret, True)
    
    def test_get_message(self):
        message = self.gen_message()
        self.queue.push_message(self.u1, message)
        ret = self.queue.get_messages(self.u1, 10)
        self.assertEqual(ret[0], message)

        self.queue.push_message(self.u1, self.gen_message())
        ret = self.queue.get_messages(self.u1, 10)
        self.assertEqual(len(ret), 2)

        self.queue.push_message(self.u1, self.gen_message())
        ret = self.queue.get_messages(self.u1, 2)
        self.assertNotEqual(len(ret), 3)
    
    def test_ack_message(self):
        self.queue.push_message(self.u1, self.gen_message())
        self.queue.push_message(self.u1, self.gen_message())
        self.queue.push_message(self.u1, self.gen_message())

        last_message = self.gen_message()
        self.queue.push_message(self.u1, last_message)
        ret = self.queue.get_messages(self.u1, 10)
        self.assertEqual(len(ret), 4)
        
        self.queue.ack_messages(self.u1, 4, last_message['msg_id'])
        ret = self.queue.get_messages(self.u1, 10)
        self.assertEqual(len(ret), 0)

    def tearDown(self):
        for key in self.r.keys('%s*' % QUEUE_PREFIX):
            self.r.delete(key)
