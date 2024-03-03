import pygraphviz as pgv

def create_system_architecture_diagram():
    # Create a new graph
    graph = pgv.AGraph(directed=True, rankdir='TB')

    # Add nodes
    graph.add_node('LandingPageView', shape='box', style='filled', fillcolor='lightblue')
    graph.add_node('ApplicationFormView', shape='box', style='filled', fillcolor='lightblue')
    graph.add_node('SuccessPageView', shape='box', style='filled', fillcolor='lightblue')
    graph.add_node('ProgressReportView', shape='box', style='filled', fillcolor='lightblue')

    graph.add_node('generate_serial_number', shape='box', style='filled', fillcolor='lightgreen')
    graph.add_node('generate_pdf', shape='box', style='filled', fillcolor='lightgreen')

    graph.add_node('Django Models', shape='box', style='filled', fillcolor='lightcoral')
    graph.add_node('Bank', shape='box', style='filled', fillcolor='lightcoral')
    graph.add_node('Institution', shape='box', style='filled', fillcolor='lightcoral')
    graph.add_node('Account', shape='box', style='filled', fillcolor='lightcoral')
    graph.add_node('Constituency', shape='box', style='filled', fillcolor='lightcoral')
    graph.add_node('Voter', shape='box', style='filled', fillcolor='lightcoral')
    graph.add_node('Student', shape='box', style='filled', fillcolor='lightcoral')
    graph.add_node('FinancialYear', shape='box', style='filled', fillcolor='lightcoral')
    graph.add_node('BursaryApplication', shape='box', style='filled', fillcolor='lightcoral')

    # Add edges
    graph.add_edge('LandingPageView', 'ApplicationFormView')
    graph.add_edge('ApplicationFormView', 'SuccessPageView')
    graph.add_edge('ApplicationFormView', 'generate_serial_number')
    graph.add_edge('ApplicationFormView', 'generate_pdf')
    graph.add_edge('SuccessPageView', 'LandingPageView')
    graph.add_edge('SuccessPageView', 'generate_pdf')
    graph.add_edge('ProgressReportView', 'generate_pdf')

    graph.add_edge('generate_serial_number', 'Django Models')
    graph.add_edge('generate_pdf', 'Django Models')

    graph.add_edge('Bank', 'Django Models')
    graph.add_edge('Institution', 'Django Models')
    graph.add_edge('Account', 'Django Models')
    graph.add_edge('Constituency', 'Django Models')
    graph.add_edge('Voter', 'Django Models')
    graph.add_edge('Student', 'Django Models')
    graph.add_edge('FinancialYear', 'Django Models')
    graph.add_edge('BursaryApplication', 'Django Models')

    # Save as PNG
    graph.draw('system_architecture.png', format='png', prog='dot')

if __name__ == "__main__":
    create_system_architecture_diagram()

