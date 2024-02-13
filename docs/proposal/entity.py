import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout

# Create an empty directed graph
G = nx.DiGraph()

# Add entities and relationships to the graph
entities = {'Applicant': 'ellipse', 'Bursary': 'box', 'ApplicationStatus': 'diamond', 'Institution': 'box', 'Committee': 'box'}
relationships = [('Applicant', 'submits', 'BursaryApplication'),
                  ('BursaryApplication', 'has', 'ApplicationStatus'),
                  ('BursaryApplication', 'applies_to', 'Institution'),
                  ('BursaryApplication', 'reviewed_by', 'Committee'),
                  ('Bursary', 'provides_funds_for', 'BursaryApplication')]  # New relationship

# Extract source and target nodes from relationships
source_nodes, edge_labels, target_nodes = zip(*relationships)

# Add nodes and edges to the graph with specified node shapes
for entity, shape in entities.items():
    G.add_node(entity, shape=shape)

G.add_nodes_from(source_nodes)
G.add_nodes_from(target_nodes)
G.add_edges_from(zip(source_nodes, target_nodes))

# Draw the graph with graphviz_layout for better positioning
pos = graphviz_layout(G, prog='dot')
nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=2000, node_color="skyblue", font_size=10, font_color="black", edge_color="gray", width=2)

# Add edge labels
edge_labels_dict = {(source, target): label for (source, label, target) in relationships}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels_dict)

# Save the graph as a PNG file
plt.savefig('bursary_mashinani_erd.png', format='png', bbox_inches='tight')

# Optionally, display the graph
plt.show()

