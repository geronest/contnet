# -*- coding: utf-8 -*-
import parsers.NetParser as netp
import networkx as nx
import matplotlib.pyplot as plt
from net.infos import *
import numpy as np


if __name__ == "__main__":
    np1 = netp.NetParser("./ipts/sample.csv")
    nodes, ns, dp_added = np1.process_file()

    print(nodes)

    DG = nx.DiGraph()
    
    nodes_person = dp_added['랏인']
    nodes_proj = dp_added['플젝']
    nodes_pres = dp_added['발표']
    
    net = Net(nodes)
    
    print("net cons: \n{}\n\n".format(net.cons))

    num_nbrs = int(np.random.random() * len(ns))
    # ncs = np.random.choice(ns, num_nbrs, replace = False) # nodes chosen
    vals_init = list()
    # for nc in ncs:
        # vals_init.append([nc, 1.])
    for n in ns:
        if n in nodes_person: vals_init.append([n, 1.])

    print("vals_init : {}".format(vals_init))
    net.propagate_values(vals_init)

    print("\n\nvals_node\n{}\n\nvals_edge\n{}".format(net.vals_node['total'], net.vals_edge))

    for i in range(len(ns)):
        for j in range(len(ns)):
            if net.vals_edge[i,j] > 0.: DG.add_edge(ns[i], ns[j], weight = net.vals_edge[i, j])

    # plt.subplot(121)

    pos = nx.spring_layout(DG)
    nx.draw_networkx_nodes(DG, pos, nodelist = nodes_person, node_color='g', node_size = 500, alpha = 0.8)
    nx.draw_networkx_nodes(DG, pos, nodelist = nodes_proj, node_color='r', node_size = 500, alpha = 0.8)
    nx.draw_networkx_nodes(DG, pos, nodelist = nodes_pres, node_color='b', node_size = 500, alpha = 0.8)
    nx.draw_networkx_edges(DG, pos, width = 3, alpha = 0.8, edge_color='k')

    dic_labels = dict()

    for i in range(len(ns)):
        dic_labels[ns[i]] = net.vals_node['total'][i]
    nx.draw_networkx_labels(DG, pos, dic_labels, font_color='y')
    # nx.draw(DG, with_labels = True, font_weight = 'bold')
    plt.show()
    plt.savefig('test_np1.png')