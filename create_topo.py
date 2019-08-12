#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
import random
from collections import defaultdict
SWITCH_NUM=100
HOST_NUM=10
class mytopo(Topo):
    def __init__(self, n=2, **opts):
        Topo.__init__(self, **opts)
	s=[]
	for i in range(HOST_NUM):
	    host = self.addHost('h'+str(i))
	    s.append(host)
        for i in range(SWITCH_NUM):
            switch = self.addSwitch('s%s' % i)
            s.append(switch)
        # print s
	choice=range(SWITCH_NUM+HOST_NUM)
	conn=set()
	graph=defaultdict(list)
	visit=set()
	while(len(conn)<SWITCH_NUM+HOST_NUM):
	    now=random.sample(choice,2)
	    if not tuple(now) in visit:
		visit.add(tuple(now))
		visit.add(tuple([now[0]+now[1]]))
		graph[now[0]].append(now[1])
		graph[now[1]].append(now[0])
		for e in now:
		    conn.add(e)
	edges=self.bfs(graph)
	print(edges)
	for edge in edges:
	    self.addLink(s[edge[0]],s[edge[1]])
    def bfs(self,graph):
	queue=[0]
	visit=set([0])
	edges=[]
	while(queue):
	    s=queue.pop(0)
	    for t in graph[s]:
		if not t in visit:
		    edges.append([s,t])
		    queue.append(t)
		    visit.add(t)
	return edges
class SingleSwitch(Topo):
    "Single switch connected to n hosts."

    def __init__(self, n=2, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)
	h1=self.addHost('h1')
	h2=self.addHost('h2')
	self.addLink(h1,h2)
            # linkopts = dict(bw=10, delay='5ms', loss=10, max_queue_size=1000, use_htb=True)
            # (or you can use brace syntax: linkopts = {'bw':10, 'delay':'5ms', ... } )
            # self.addLink(node1, node2, **linkopts)


def simpleTest(topo):
    "Create and test a simple network"
    net = Mininet(topo)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"
    net.pingAll()
    net.stop()


topos = {'SingleSwitch': SingleSwitch, 'mytopo':mytopo }
tests = {'mytest': simpleTest}

if __name__ == '__main__':
    # Tell mininet to print useful information
    topo=mytopo()
    simpleTest(topo)
