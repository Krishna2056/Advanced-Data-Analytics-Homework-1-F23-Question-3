import networkx as nx
from util import delPrev, clean, plot_graph, fromgraphtype, sep_hist
import matplotlib.pyplot as plt
import numpy as np
import os


def main():
  input_file = 'Wiki_Data.txt'

  # Creating directed graph
  un_graph = fromgraphtype(input_file, True)
  # Creating undirected graph
  di_graph = fromgraphtype(input_file, False)
  

  # Answer to Q1
  print(f"Number of Nodes: {len(di_graph.nodes)}")
  print(f"Number of Edges: {len(di_graph.edges)}")


  # Answer to Q2
  plot_graph(di_graph, 50, False)


  # Answer to Q3: Creating a symmetric adjacency matrix
  data = np.genfromtxt('cleanWikiData.txt', delimiter=',', skip_header=1, dtype=int)
  max_node_id = np.max(data)
  adjacency_matrix = np.zeros((max_node_id, max_node_id), dtype=int)
  for row in data:
      from_node, to_node = row
      adjacency_matrix[from_node - 1, to_node - 1] = 1
      adjacency_matrix[to_node - 1, from_node - 1] = 1
  adjacency_matrix_50 = adjacency_matrix[:50, :50]
  G = nx.Graph(adjacency_matrix_50)
  pos = nx.spring_layout(G, seed=42) 
  plt.figure(figsize=(10, 10))
  nx.draw(G, pos, with_labels=True, node_size=100, node_color='green', font_size=8, font_color='black')
  plt.title('Undirected Graph for the First 50 Vertices')
  filename = f"adjacency.png"
  path = os.path.join("images", filename)
  plt.savefig(path)
  plt.close()


  # Answer to Q4
  for i in [100, 200, 300, 400, len(un_graph.nodes)]:
    plot_graph(un_graph, i, True)


  #Answer to Q5
  sep_hist(un_graph)

        

if __name__ == "__main__":
    main()

