# -*- coding: utf-8 -*-
import csv 
from net.infos import NodeInfo

class NetParser():
    def __init__(self, path):
        try:
            self.file = open(path, newline = '', encoding='utf-8')
            self.reader = csv.reader(self.file, delimiter = ',')

        except Exception as e:
            print("[ERROR | NetParser/__init__] {}".format(e))

    def process_file(self):
        res = list()
        l_added = list()
        for row in self.reader:
            if len(row) >= 2: # each node must have at least two entries, NAME-NODE and TAG-NODE
                n_toadd = NodeInfo(row[0])
                n_toadd.add_prop('type', row[1])

                for idx in range(len(row)-2):
                    split_nbr = row[idx+2].split('_')
                    try:
                        if len(split_nbr) == 1:
                            n_toadd.add_con(split_nbr[0], 1.0)
                        elif len(split_nbr) == 2:
                            n_toadd.add_con(split_nbr[0], float(split_nbr[1]))
                    except Exception as e:
                        print("[ERROR | NetParser/process_file] split_nbr: {}, {}".format(split_nbr, e))
                l_added.append(row[0])
                res.append(n_toadd)
        return res, l_added





