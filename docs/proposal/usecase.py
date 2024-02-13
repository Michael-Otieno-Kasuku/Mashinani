import pygraphviz as pgv

# Create a new graph
graph = pgv.AGraph(strict=True, directed=True, rankdir='LR', compound=True)

# Add nodes for different use cases with standardized symbols
graph.add_node("Applicant", shape="actor", style="filled", color="skyblue", fontsize=12)
graph.add_node("Bursary Mashinani Portal", shape="rectangle", style="filled", color="lightgreen", fontsize=12)
graph.add_node("NG-CDF Program", shape="rectangle", style="filled", color="lightgreen", fontsize=12)

# Add edges to represent interactions between use cases
graph.add_edge("Applicant", "Bursary Mashinani Portal", label="Initiates Bursary Application", fontsize=10)
graph.add_edge("Bursary Mashinani Portal", "NG-CDF Program", label="Sends Funding Request", fontsize=10)
graph.add_edge("NG-CDF Program", "Bursary Mashinani Portal", label="Approves Funding", fontsize=10)
graph.add_edge("Bursary Mashinani Portal", "Applicant", label="Provides Application Status", fontsize=10)

# Save the graph as a PNG file
graph.draw("bursary_mashinani_use_case_diagram.png", format="png", prog="dot")

