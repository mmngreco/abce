# Copyright 2012 Davoud Taghawi-Nejad
#
# Module Author: Davoud Taghawi-Nejad
#
# ABCE is open-source software. If you are using ABCE for your research you are
# requested the quote the use of this software.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License and quotation of the
# author. You may obtain a copy of the License at
#       http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
import multiprocessing
import networkx as nx
import matplotlib.pyplot as plt


def write_graph(nodes, edges, colors, directory, current_round):
    network = nx.Graph(strict=True, directed=True)
    for node, attributes in nodes:
        network.add_node(node, **attributes)

    for edge in edges:
        network.add_edge(edge[0], edge[1])
    nx.write_gml(network, directory +'/network%i.gml' % current_round)
    pos = nx.spring_layout(network) # positions for all nodes

    plt.figure(1, figsize=(24,20))
    nx.draw_networkx(network,pos,
                       node_color=[colors[node] for node in network.nodes()],
                       alpha=0.8)
    plt.savefig(directory +'/network%i.png' % current_round, dpi=100)
    plt.close()

class AbceLogger(multiprocessing.Process):
    def __init__(self, directory, in_sok):
        multiprocessing.Process.__init__(self)
        self.in_sok = in_sok
        self.directory = directory

    def run(self):
        current_round = 0
        nodes = []
        edges = []
        colors = {}

        while True:
            try:
                command, rnd, msg = self.in_sok.get()
            except KeyboardInterrupt:
                break
            except EOFError:
                break
            if rnd != current_round:
                write_graph(nodes, edges, colors, self.directory, current_round)
                del nodes[:]
                del edges[:]
                current_round = rnd

            if command == 'edges':
                self_name, list_of_edges = msg
                name = '%s %i' %  self_name
                for edge in list_of_edges:
                    edges.append((name, '%s %i' % edge))

            elif command == 'node':
                self_name, color, style, shape = msg
                name = '%s %i' %  self_name
                nodes.append([name, {'label': name, 'color': color, 'style': style, 'shape': shape}])
                colors[name] = color

            elif command == 'close':
                break

            else:
                SystemExit("command not recognized", command, rnd, msg)

