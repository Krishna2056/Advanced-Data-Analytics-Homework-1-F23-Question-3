import os
import networkx as nx
import regex as re
import numpy as np
import matplotlib.pyplot as plt
import shutil


def delPrev():
# This function delets the previously ...
# created datasets and image files.
  folder = 'images'
  try: 
    shutil.rmtree(folder)
  except:
    pass
  os.mkdir(folder)


def fromgraphtype(input_file, flag):
   """This function takes in the input files, determine whether
    to use directed (when custom flag is False) or undirected 
    (when custom flag is True) graph and remove isolated node"""
   
   if flag == False:
      graph =  nx.DiGraph()
   else:
      graph = nx.Graph()
   delPrev()
   return clean(input_file, graph)


def clean(input_file, graph):

  """This function removes any isolated nodes that are present in the Wiki_data.txt
      Also, it creates the new file containing cleaned data that are sorted in an ascending order
      It returns the graph of the network at the end."""
  
  # Reading a file to create graph
  with open(input_file, 'r') as file:
    for line in file:
      if not bool(re.match(r'^[0-9]+,[0-9]+',line)):
          continue
      source, target = map(int, line.strip().split(','))
      graph.add_edge(source, target)

      # Removing isolated nodes from the graph
      lst = graph.nodes
      for node in lst:
        try:
          if graph.in_degree(node) + graph.out_degree(node) == 0:
            graph.remove_nodes_from(node)
        except AttributeError:
           if graph.degree(node) == 0:
            graph.remove_nodes_from(node)

  edge_list = list(graph.edges)
  sorted_pairs = sorted(edge_list, key=lambda x: (x[0], x[1]))

  # writing the cleaned and sorted data in the new output file
  output_file = 'cleanWikiData.txt'
  with open(output_file, 'w') as file:
      for s, t in sorted_pairs:
          file.write(f"{s},{t}\n")
  return graph


def plot_graph(graph, n, flag):
    """This function takes out the first n edges sorted according to their indices
       If uniformly distributed, use third argument = True in the function plot_graph"""

    subgraph = graph.copy()
    with open("cleanWikiData.txt", 'r') as file:
      for line in file:
        source, target = map(int, line.strip().split(','))
        # Take the first n modes
        nodes_ = list(subgraph.nodes)
        for i in range(len(nodes_)):
           if nodes_[i] >= n:
              subgraph.remove_node(nodes_[i])
        pos = nx.circular_layout(subgraph)
        if flag == True:
                for i in subgraph.nodes:
                  theta = 2 * np.pi * i / len(subgraph.nodes) + 1
                  node_positions = {i: (np.cos(theta), np.sin(theta)) }
                nx.draw(subgraph, pos , with_labels=True, node_color='green', node_size=100, font_size=6)
        else:
          nx.draw(subgraph, pos , with_labels=True, node_color='green', node_size=100, font_size=6, arrowsize=8)
        plt.title("Directed Subgraph with First {n} Vertices")
        filename = f"subgraph_{n}.png"
        path = os.path.join("images", filename)
        plt.savefig(path)
        plt.close()
        return


def sep_hist(un_graph):
  separation_counts = {(s + 1): 0 for s in range(20)}
  for s_node in un_graph.nodes():
    for t_node in un_graph.nodes():
        if s_node < t_node:
            try:
              separation = nx.shortest_path_length(un_graph, source = s_node, target = t_node)
              if separation <= 20:
                separation_counts[separation] += 1
            except nx.NetworkXNoPath:
               pass

# Step 3: Create a histogram
  separations = list(separation_counts.keys())
  counts = list(separation_counts.values())
  fig = plt.figure(num="Separations Histogram")
  plt.bar(separations, counts, tick_label=separations)
  plt.xlabel("Separation")
  plt.ylabel("Number of Pairs")
  plt.title("Histogram of Separation Lengths")
  filename = f"histogram.png"
  path = os.path.join("images", filename)
  plt.savefig(path)
  plt.close()