from collections import deque

class Graph:
    def __init__(self, V, item_to_index_map, index_to_item_map):
        self.V = V
        self.adjList = [[] for i in range(V)]
        self.item_to_index_map = item_to_index_map
        self.index_to_item_map = index_to_item_map
        self.visited = [False] * V
        self.result = deque([])

    def addEdge(self, src, dest):
        self.adjList[item_to_index_map[src]].append(item_to_index_map[dest])

    def dfs(self, src):
        self.visited = [False] * len(self.adjList)
        self.result =  deque([])
        self.dfsInternal(src)
        return self.result

    def dfsInternal(self, src):
        self.visited[src] = True
        children = self.adjList[src]
        for child in children:
            if not self.visited[child]:
                self.dfsInternal(child)
        self.result.append(src)

    def isThereAnyIncomingEdgeTo(self, node):
        for i in range(0, self.V):
            children = self.adjList[i]
            if node in set(children):
                return True
        return False

items = set()
is_dependency_graph_ready = False
edges = set()
dependecy_graph = None
counter=-1
item_to_index_map = {}
index_to_item_map = {}
installed_items = set()

def form_dependecy_graph(edges, V):
    global  dependecy_graph
    for k, v in item_to_index_map.items():
        index_to_item_map[v] = k

    dependecy_graph = Graph(V, item_to_index_map, index_to_item_map)
    for edge in edges:
        dependecy_graph.addEdge(edge.u, edge.v)

class Edge:
    def __init__(self, u, v):
        self.u = u
        self.v = v

    def __eq__(self, other):
        return self.u == self.u and self.v == other.v

    def __hash__(self):
        return hash(str(self.u) + "-->" + str(self.v))

    def __str__(self):
        return str(self.u) + "-->" + str(self.v)

def index_value(value):
    global counter
    if value not in items:
        counter += 1
        items.add(value)
        item_to_index_map[value] = counter

def execute(input):
    components = input.split()
    global dependecy_graph
    global item_to_index_map
    if components[0] == 'DEPEND':
        ### print
        print(input)
        ### get item and index them so that it is used in adjlist
        item = components[1]
        index_value(item)

        ### get dependecies and index them so that it is used in adjlist
        dependencies = components[2:]
        for dependency in dependencies:
            index_value(dependency)
            reverseedge = Edge(dependency, item)
            if reverseedge in edges:
                print("   {} depends on {}. Ignoring command.".format(dependency, item))
            else:
                edges.add(Edge(item, dependency))

    elif components[0] == 'INSTALL':
        print(input)
        # laxy graph forming
        if not dependecy_graph:
            form_dependecy_graph(edges, len(items))
        item = components[1]
        if item in items:
            order = dependecy_graph.dfs(item_to_index_map[item])
            if order:
                for index in order:
                    if index_to_item_map[index] not in installed_items:
                        print("   Installing {}".format(index_to_item_map[index]))
                        installed_items.add(index_to_item_map[index])

        else:
            print("   Installing {}".format(item) )

    elif components[0] == 'REMOVE':
        ## we should not blindly remove
        ## rather we should see in graph is there is any incoming edge to it
        ## if so do not delete
        print(input)
        item = components[1]
        if dependecy_graph.isThereAnyIncomingEdgeTo(item_to_index_map[item]):
            print('   {} is still needed.'.format(item))
        else:
            installed_items.remove(item)
            print('   Removing {}'.format(item))

    elif components[0] == 'LIST':
        print(input)
    elif components[0] == 'END':
        return
    else:
        print('invalid command')

execute('DEPEND TELNET TCPIP NETCARD')
execute('DEPEND TCPIP NETCARD')
execute('DEPEND NETCARD TCPIP')
execute('DEPEND DNS TCPIP NETCARD')
execute('DEPEND  BROWSER       TCPIP HTML')

execute('INSTALL NETCARD')
execute('INSTALL TELNET')
execute('INSTALL foo')
execute('REMOVE NETCARD')
execute('INSTALL BROWSER')
execute('INSTALL DNS')
execute('LIST')
execute('REMOVE TELNET')
execute('REMOVE NETCARD')
execute('REMOVE DNS')
execute('REMOVE NETCARD')
execute('INSTALL NETCARD')
execute('REMOVE TCPIP')
execute('REMOVE BROWSER')
execute('REMOVE TCPIP')
execute('LIST')
execute('END')

