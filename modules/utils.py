"""Util classes to be used in other files"""
import enum


class State(enum.Enum):
    """Enum class for Node Status"""
    sleep = 1
    find = 2
    found = 3


class EdgeStatus(enum.Enum):
    """Enum class for Edge Status"""
    basic = 1
    branch = 2
    reject = 3


class Message(enum.Enum):
    """Enum class for Message types"""
    connect = 1
    initiate = 2
    test = 3
    accept = 4
    reject = 5
    report = 6
    changeroot = 7


class Edge:
    def __init__(self, edge_id, weight, queue):
        self.weight = weight
        self.status = EdgeStatus.basic
        self.queue = queue
        self.id = edge_id

    def get_id(self):
        """Getter method for the id of the edge instance
        
        Returns:
            Integer -- Edge Id
        """
        return self.id

    def weight(self):
        """Getter method for the weight of the Edge class
        
        Returns:
            Float -- Weight of the edge
        """
        return self.weight

    def status(self):
        """Getter method for the status of the Edge class
        
        Returns:
            EdgeStatus -- Status of the edge
        """
        return self.status

    def change_status(self, status):
        """Change the status of the edge
        
        Arguments:
            status {EdgeStatus} -- updated status of the edge
        """
        self.status = status

    def write(self, message, payload, sender=self.id):
        """Write to the given edge by the node specified in the arguments
        
        Arguments:
            node {Integer} -- Node id of the sender node
            message {Message} -- Message to be sent
            payload {List} -- List of arguments sent along with message
        """
        # Find the queue to write to
        obj = {'id': sender, 'msg': message, 'pl': payload}
        queue.put(obj)
