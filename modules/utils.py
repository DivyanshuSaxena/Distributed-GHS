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
    halt = 8


class Edge:
    def __init__(self, edge_id, node1, node2, weight, queue):
        self.weight = weight
        self.status = EdgeStatus.basic
        self.queue = queue
        self.id = edge_id
        self.node1 = node1
        self.node2 = node2

    def __str__(self):
        """Print the edge instance for the output
        
        Returns:
            String -- Print edge
        """
        string = '(' + str(self.node1) + ', ' + str(self.node2) + ', ' + str(
            self.weight) + ')'
        return string

    def get_id(self):
        """Getter method for the id of the edge instance
        
        Returns:
            Integer -- Edge Id
        """
        return self.id

    def get_weight(self):
        """Getter method for the weight of the Edge class
        
        Returns:
            Float -- Weight of the edge
        """
        return self.weight

    def get_status(self):
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

    def write(self, message, payload):
        """Write to the given edge by the node specified in the arguments
        
        Arguments:
            node {Integer} -- Node id of the sender node
            message {Message} -- Message to be sent
            payload {List} -- List of arguments sent along with message
        """
        # Find the queue to write to
        obj = {'sender': self.get_id(), 'message': message, 'pl': payload}
        self.queue.put(obj)

    def copy(self, another):
        """Copy the status of another edge into current Edge instance
        
        Arguments:
            another {Edge}
        """
        if self.id == another.get_id():
            print ('Changing status')
            self.status = another.get_status()
        else:
            print('Edge instances not compatible for copy')
