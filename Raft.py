import random
import time
import threading

class RaftNode:
    def __init__(self, node_id, total_nodes):
        self.node_id = node_id
        self.total_nodes = total_nodes
        self.state = 'follower'
        self.term = 0
        self.votes_received = 0
        self.log = []
        self.leader_id = None
        self.timeout = random.randint(150, 300) / 1000
        self.last_heartbeat = time.time()

    def send_message(self, target_node, message):
        print(f"Node {self.node_id} sends message to Node {target_node.node_id}: {message}")
        target_node.receive_message(self, message)

    def receive_message(self, sender_node, message):
        if message == 'heartbeat':
            self.handle_heartbeat(sender_node)
        elif message == 'vote_request':
            self.handle_vote_request(sender_node)
        elif message == 'vote_grant':
            self.handle_vote_grant(sender_node)
        elif message.startswith('log_entry'):
            self.handle_log_entry(message)

    def handle_heartbeat(self, sender_node):
        self.state = 'follower'
        self.leader_id = sender_node.node_id
        self.last_heartbeat = time.time()

    def handle_vote_request(self, sender_node):
        if self.state == 'follower' and self.term <= sender_node.term:
            self.votes_received += 1
            self.send_message(sender_node, 'vote_grant')
    
    def handle_vote_grant(self, sender_node):
        self.votes_received += 1

    def handle_log_entry(self, message):
        self.log.append(message)
        print(f"Node {self.node_id} logs: {message}")

    def election(self):
        self.state = 'candidate'
        self.term += 1
        self.votes_received = 1
        print(f"Node {self.node_id} starts election for term {self.term}")
        for node in nodes:
            if node != self:
                self.send_message(node, 'vote_request')
        
        while self.votes_received <= self.total_nodes // 2:
            if time.time() - self.last_heartbeat > self.timeout:
                print(f"Node {self.node_id} timed out and starts a new election")
                self.election()
                return
            time.sleep(0.1)
        
        self.state = 'leader'
        self.leader_id = self.node_id
        print(f"Node {self.node_id} becomes leader for term {self.term}")

    def start_heartbeat(self):
        while self.state == 'leader':
            for node in nodes:
                if node != self:
                    self.send_message(node, 'heartbeat')
            time.sleep(1)

    def propose_log_entry(self, entry):
        if self.state == 'leader':
            self.log.append(entry)
            for node in nodes:
                if node != self:
                    self.send_message(node, f'log_entry {entry}')
            print(f"Node {self.node_id} proposed log entry: {entry}")
        else:
            print(f"Node {self.node_id} cannot propose log entry, not a leader")

nodes = [RaftNode(node_id=i, total_nodes=5) for i in range(5)]

def simulate():
    for node in nodes:
        if random.random() < 0.5:
            node.election()
    
    leader_node = next((node for node in nodes if node.state == 'leader'), None)
    if leader_node:
        threading.Thread(target=leader_node.start_heartbeat).start()

    if leader_node:
        leader_node.propose_log_entry("New Log Entry")

simulate()
