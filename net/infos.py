# -*- coding: utf-8 -*-
import numpy as np


class NodeInfo():
    def __init__(self, name):
        self.name = name
        self.properties = dict()
        self.cons = list()

    def add_con(self, name_target, weight_edge = 1.):
        self.cons.append([name_target, weight_edge])

    def add_prop(self, name_prop, item_prop = None):
        self.properties[name_prop] = item_prop

class Nodes():
    def __init__(self, name, nodes):
        self.name = name
        self.nodes = dict()

        for n in nodes:
            self.nodes[n.name] = n.cons


class Net():
    def __init__(self, nodes):
        self.name_nodes = [n.name for n in nodes]
        print(self.name_nodes)
        self.nodes = nodes
        self.num_nodes = len(self.nodes)
        self.cons = np.zeros((self.num_nodes, self.num_nodes))

        self.vals_node = dict()
        self.vals_node['curr'] = np.zeros((self.num_nodes, 1))
        self.vals_node['total'] = np.zeros((self.num_nodes, 1))
        self.vals_edge = np.zeros((self.num_nodes, self.num_nodes))

        for i in range(len(self.nodes)):
            ccons = self.nodes[i].cons # current cons
            for j in range(len(ccons)):
                try:
                    self.cons[i, self.name_nodes.index(ccons[j][0])] = ccons[j][1]
                except Exception as e:
                    print("[ERROR | infos/Net/__init__] {} not in self.name_nodes? {}".format(ccons[j][0], e))

            self.cons[i] /= np.sum(self.cons[i]) + 1e-7

    def propagate_values(self, vals_init, num_iter = 10):
        for v in vals_init:
            self.vals_node['curr'][self.name_nodes.index(v[0]), 0] = v[1]

        for i in range(num_iter):
            self.vals_node['curr'] *= 0.5
            self.vals_node['total'] += self.vals_node['curr']
            self.vals_edge += self.cons * self.vals_node['curr'] 
            self.vals_node['curr'] = np.matmul(np.transpose(self.cons), self.vals_node['curr'])

            print(self.vals_node['total'])

if __name__ == '__main__':
    import networkx as nx
    import matplotlib.pyplot as plt

    DG = nx.DiGraph()
    ns = ['a', 'b', 'c', 'd', 'e', 'f', 'g']

    nodes = list()
    for n in ns:
        DG.add_node(n)
        nn = NodeInfo(n)

        num_nbrs = int(np.random.random() * len(ns))
        for nbr in np.random.choice(ns, num_nbrs, replace = False):
            # print("node {}'s neighbor {} added".format(n, nbr))

            if n != nbr: nn.add_con(nbr)

        print("\n\nNodeInfo {}: cons {}".format(nn.name, nn.cons))

        nodes.append(nn)
    
    net = Net(nodes)
    

    print("net cons: \n{}\n\n".format(net.cons))

    num_nbrs = int(np.random.random() * len(ns))
    ncs = np.random.choice(ns, num_nbrs, replace = False) # nodes chosen
    vals_init = list()
    for nc in ncs:
        vals_init.append([nc, 1.])

    print("vals_init : {}".format(vals_init))
    net.propagate_values(vals_init)

    print("\n\nvals_node\n{}\n\nvals_edge\n{}".format(net.vals_node['total'], net.vals_edge))

    for i in range(len(ns)):
        for j in range(len(ns)):
            if net.vals_edge[i,j] > 0.: DG.add_edge(ns[i], ns[j], weight = net.vals_edge[i, j])

    plt.subplot(121)
    nx.draw(DG, with_labels = True, font_weight = 'bold')
    plt.show()
    plt.savefig('test.png')




    




