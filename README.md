#Simple Message Queue
----------
Push in O(1). GET in O(N),  N is the number of messages in the specified range to get. ACK in O(N), where N is the number of messages to be acked and removed by the operation.

## How to use:

    # First, get your redis db
    >>> r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    
    >>> queue = MessageQueue(r)
    
    # push message to queue, 'msg_id' is required.
    >>> message1 = {'text': 'hello world!', 'msg_id': '2ebd68'}
    >>> message2 = {'text': 'hi world!', 'msg_id': '4dce26'}
    >>> queue.push_to_queue(user_id, message1)
    True

    >>> queue.push_to_queue(user_id, message2)
    True
    
    # get messages from queue, specific user_id and page_size.
    >>> queue.get_messages(user_id, page_size)
    [{'text': 'hello world!'}, {'text': 'hi world!'}]
    
    # ack messages, msg_id should be unique.
    >>> queue.ack_messages(user_id, msg_id, last_position)
    True
    # If msg_id in a wrong last position.
    False
