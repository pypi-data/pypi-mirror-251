# SharedMemoryQueue

SharedMemoryQueue is a Python library for interacting with a shared memory queue via a C++ DLL. It allows the creation of multiple queue instances, each identified by a unique name, enabling more flexible and scalable inter-process communication.

## Installation

You can install SharedMemoryQueue using pip:

```
pip install SharedMemoryQueue
```

## Usage

Here's a basic example of how to use the SharedMemoryQueue library:

```
from SharedMemoryQueue import enqueue_message, dequeue_message

# Enqueue messages into different queues
enqueue_message('Queue1', 'Message for Queue 1')
enqueue_message('Queue2', 'Message for Queue 2')

# Dequeue messages from the queues
message1 = dequeue_message('Queue1')
message2 = dequeue_message('Queue2')
print(f'Received from Queue1: {message1}')
print(f'Received from Queue2: {message2}')

```

## Links

[PyPi](https://pypi.org/project/SharedMemoryQueue/)