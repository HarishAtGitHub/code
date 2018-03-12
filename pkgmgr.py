class Graph:
    def __init__(self, V, item_to_index_map, index_to_item_map):
        self.V = V
        self.adjList = [[] for i in range(V)]
        self.item_to_index_map = item_to_index_map
        self.index_to_item_map = index_to_item_map

    def addEdge(self, src, dest):
        self.adjList[item_to_index_map[src]].append(item_to_index_map[dest])

items = set()
is_dependency_graph_ready = False
edges = set()
dependecy_graph = None
counter=-1
item_to_index_map = {}
index_to_item_map = {}

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
            reverseedge = Edge(item, dependency)
            if reverseedge in edges:
                print("   {} depends on {}. Ignoring command.".format(dependency, item))
            else:
                edges.add(Edge(dependency, item))

    elif components[0] == 'INSTALL':
        # laxy graph forming
        if not dependecy_graph:
            form_dependecy_graph(edges, len(items))
            print("graph formed")
        print(input)

    elif components[0] == 'REMOVE':
        print(input)
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
'''
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
'''
