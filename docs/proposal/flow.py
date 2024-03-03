from graphviz import Digraph

def create_data_flow_diagram():
    # Create a new directed graph
    graph = Digraph('DataFlowDiagram', filename='data_flow_diagram', format='png', engine='dot')

    # Define nodes with additional information
    graph.node('User', 'User', shape='ellipse', color='blue', style='filled', fillcolor='lightblue')
    graph.node('Form', 'Application Form', shape='box', color='green', style='filled', fillcolor='lightgreen')
    graph.node('View', 'ApplicationFormView', shape='box', color='green', style='filled', fillcolor='lightgreen')
    graph.node('Database', 'Database', shape='box', color='red', style='filled', fillcolor='lightcoral')
    graph.node('SuccessPage', 'SuccessPageView', shape='box', color='green', style='filled', fillcolor='lightgreen')
    graph.node('PDF', 'PDF Generation', shape='box', color='green', style='filled', fillcolor='lightgreen')
    graph.node('ProgressReport', 'ProgressReportView', shape='box', color='green', style='filled', fillcolor='lightgreen')

    # Define edges with labels
    graph.edge('User', 'Form', label='Submit Application Form')
    graph.edge('Form', 'View', label='Form Submission')
    graph.edge('View', 'Database', label='Save Application Data')
    graph.edge('View', 'SuccessPage', label='Redirect to Success Page')
    graph.edge('SuccessPage', 'User', label='Show Success Message')
    graph.edge('SuccessPage', 'PDF', label='Generate Progress Report PDF')
    graph.edge('PDF', 'User', label='Provide PDF Download Link')
    graph.edge('User', 'ProgressReport', label='Request Progress Report')
    graph.edge('ProgressReport', 'PDF', label='Generate Progress Report PDF')

    # Save as PNG
    graph.render(cleanup=True, format='png', filename='data_flow_diagram', directory='./', view=False)

if __name__ == "__main__":
    create_data_flow_diagram()

