# SDN
ryu+mininet实现最短路径规划
-----
## topo的构建
topo主要应用了随机图算法，随机生成Link  
再使用bfs筛选，防止交换机链接成环造成广播风暴  
`关键代码如下`：<br>
```
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
```
部分topo:  
.<img src="https://github.com/smartysl/SDN/blob/master/SDNpic/%E6%8D%95%E8%8E%B72.PNG" width="300" height="100" />
## 最短路径规划
1.获取交换机的链接topo  
2.获取流信息  
3.如果src不在网络拓扑中则建立链接  
4.如果dst在网络拓扑中则根据最短路算法规划下一跳端口  
5.对于已确定的路径加入流  
`关键代码如下`:  
```
if src not in self.net:

            self.net.add_node(src)

            self.net.add_edge(dpid,src,port=in_port)

            self.net.add_edge(src,dpid)

        if dst in self.net:
        
            path=nx.shortest_path(self.net,src,dst)  
	    print(path)
            next=path[path.index(dpid)+1]
            out_port=self.net[dpid][next]['port']

        else:

            out_port = ofproto.OFPP_FLOOD
```
部分学习到的路径  
.<img src="https://github.com/smartysl/SDN/blob/master/SDNpic/%E6%8D%95%E8%8E%B71.PNG" width="300" height="450" />

