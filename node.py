"""Implementation of the Node class for running distributed GHS Algorithm"""
import sys
from modules.utils import State, EdgeStatus, Edge, Message

INF = sys.maxsize


class Node:
    def __init__(self, edges, name, msg_q):
        """Ctor for the Node class
        
        Arguments:
            edges {List} -- List of queues for each edge to the current node
            name {Float} -- Fragment Name to which the Node belongs
            msg_q {Multiprocessing Queue} -- Queue from which Node will read
        """
        # Required for GHS operation
        self.state = State.sleep
        self.name = name
        self.msg_q = msg_q
        self.level = 0

        self.father = -1  # Index of the edge along the father of the node
        self.edges = edges
        self.num_neighbors = len(edges)

        # Temporary variables
        self.rec = 0
        self.test_edge = -1
        self.best_edge = -1
        self.best_weight = INF

    def __change_level(self, level):
        """Change level of current node
        
        Arguments:
            level {Integer} -- Updated level of the node
        """
        self.level = level

    def __change_state(self, state):
        """Change the state of the current node
        
        Arguments:
            state {State} -- Updated state of the node
        """
        self.state = state

    def __change_edge_status(self, edge_index, status):
        """Change the status of the edge with given index
        
        Arguments:
            edge_index {Integer} -- index of the edge, whose status is to be
                                    changed
            status {EdgeStatus} -- Updated status of the edge
        """
        self.edges[edge_index].change_status(status)

    def __edge_stub(self,
                    edge_index,
                    message,
                    payload=[],
                    sender_edge=edge_index):
        """Act as a stub to write to the given edge

        Arguments:
            edge_index {Integer} -- Index of the edge on which message is to be 
                                    written, if -1 write to self queue
            message {Message} -- Message
            payload {List} -- Attached Payload
            sender_edge {Integer} -- Edge index through which the message is set
                                     to be read
        """
        if edge_index == -1:
            self.msg_q.write(message, payload, sender_edge)
        else:
            self.edges[edge_index].write(message, payload)

    def __test(self):
        """Execute the test operation"""
        # Find the minimal outgoing non-tree acceptable edge
        min_wt = min_index = -1
        for _in in range(self.num_neighbors):
            edge = self.edges[_in]
            if edge.status() == EdgeStatus.basic:
                if min_wt == -1 or min_wt > edge.weight():
                    min_index = _in
                    min_wt = edge.weight()

        if min_index != -1:
            # Send test message (to percolate the search)
            self.test_edge = min_index
            _pl = [self.level, self.name]
            self.__edge_stub(min_index, Message.test, _pl)
        else:
            # No test edge available further - report it
            self.test_edge = -1
            self.__report()

    def __report(self):
        """Execute  the report operation"""
        # Count the number of sons in the current MST
        count = 0
        for _in in range(self.num_neighbors):
            edge = self.edges[_in]
            if edge.status == EdgeStatus.branch and _in != self.father:
                count += 1

        if self.rec == count and self.test_edge == -1:
            # Received report from all kids
            self.__change_state(State.found)
            self.__edge_stub(self.father, Message.report, [self.best_weight])

    def __changeroot(self):
        """Execute the changeroot operation"""
        if self.edges[self.best_edge].status() == EdgeStatus.branch:
            self.__edge_stub(self.best_edge, Message.changeroot)
        else:
            # changeroot received by father node
            self.__edge_stub(self.best_edge, Message.connect, [self.level])
            self.__change_edge_status(self.best_edge, EdgeStatus.branch)

    def wakeup(self):
        """Wake up function"""
        # Find least weight edge from node
        min_wt = min_edge = -1
        for _in in range(self.num_neighbors):
            edge = self.edges[_in]
            if min_wt == -1 or min_wt > edge.weight():
                min_edge = _in
                min_wt = edge.weight()

        self.__change_level(0)
        self.__change_state(State.found)
        self.rec = 0
        self.__change_edge_status(min_edge, EdgeStatus.branch)

        # Send connect message to the least weight edge
        self.__edge_stub(min_edge, Message.connect, [self.level])

    def process_connect(self, edge_index, level):
        """Execute receipt of connect message
        
        Arguments:
            edge_index {Integer} -- Index of the edge on which message was
                                    received in the edges list
            level {Integer} -- Level of the connecting fragment
        """
        if level < self.level:
            # A lower fragment is requesting absorption
            self.__change_edge_status(edge_index, EdgeStatus.branch)
            _pl = [self.level, self.name, self.state]
            self.__edge_stub(edge_index, Message.initiate, _pl)
        else:
            if self.edges[edge_index].status() == EdgeStatus.basic:
                # Send back to queue for processing
                self.__edge_stub(-1, Message.connect, [level],
                                 self.edges[edge_index].id())
            else:
                # Core Edge reached - send initiate to the connecting node
                edge_weight = self.edges[edge_index].weight()
                _pl = [self.level + 1, edge_weight, State.find]
                self.__edge_stub(edge_index, Message.initiate, _pl)

    def procecss_initiate(self, edge_index, level, name, state):
        """Execute receipt of initiate message
        
        Arguments:
            edge_index {Integer} -- Index of the edge on which message was
                                    received in the edges list
            level {Integer} -- Level
            name {Float} -- Updated fragment name
            state {State} -- Updated node State
        """
        self.name = name
        self.__change_state(state)
        self.__change_level(level)
        self.father = edge_index

        self.best_edge = -1
        self.best_weight = INF

        # Percolate the update in the fragment down the tree
        for _in in range(self.num_neighbors):
            if _in == edge_index: continue
            # Send initiate message to all children
            edge = self.edges[_in]
            if edge.status() == EdgeStatus.branch:
                _pl = [level, name, state]
                self.__edge_stub(_in, Message.test, _pl)

        # If state has been updated to test, start finding
        if self.state == State.find:
            self.rec = 0
            self.__test()

    def procecss_test(self, edge_index, level, name):
        """Execute receipt of test message
        
        Arguments:
            edge_index {Integer} -- Index of the edge on which message was
                                    received in the edges list
            level {Integer} -- Level from where test command has been issued
            name {Float} -- Name of the fragment
        """
        if level > self.level:
            # Send back to queue
            self.__edge_stub(-1, Message.test, [level, name],
                             self.edges[edge_index].id())
        else:
            # Check whether testing node is not internal
            if name == self.name:
                if self.edges[edge_index].status() == EdgeStatus.basic:
                    self.__change_edge_status(edge_index, EdgeStatus.reject)
                # Send reject if not already sent to the node for testing
                if edge_index != self.test_edge:
                    self.__edge_stub(edge_index, Message.reject)
                else:
                    self.__test()
            else:
                self.__edge_stub(edge_index, Message.accept)

    def process_accept(self, edge_index):
        """Execute receipt of accept message
        
        Arguments:
            edge_index {Integer} -- Index of the edge on which message was
                                    received in the edges list
        """
        self.test_edge = -1
        edge_weight = self.edges[edge_index].weight()
        if edge_weight < self.best_weight:
            self.best_weight = edge_weight
            self.best_edge = edge_index

        # Found the best edge at this node - report it
        self.__report()

    def process_reject(self, edge_index):
        """Execute receipt of reject message
        
        Arguments:
            edge_index {Integer} -- Index of the edge on which message was
                                    received in the edges list
        """
        if self.edges[edge_index].status() == EdgeStatus.basic:
            self.__change_edge_status(edge_index, EdgeStatus.reject)
        self.__test()

    def process_report(self, edge_index, weight):
        """Execute reeipt of report message
        
        Arguments:
            edge_index {Integer} -- Index of the edge on which message was
                                    received in the edges list
            weight {Float} -- Best weight found by the child at edge_index
        """
        if edge_index != self.father:
            # Send back the reply for the initiate search message
            if weight < self.best_weight:
                self.best_weight = weight
                self.best_edge = edge_index
            self.rec += 1
        else:
            # Received report from core edge - finish the search for best edge
            if self.state == State.find:
                # Node is still finding the best edge. Send back to the queue
                self.__edge_stub(-1, Message.report, [weight], edge_index)
            else:
                if weight > self.best_weight:
                    # The other core node must update its father
                    self.__changeroot()
                elif weight == INF and self.best_weight == INF:
                    # Tree complete
                    self.__complete()

    def process_changeroot(self):
        """Execute receipt of changeroot message"""
        self.__changeroot()
