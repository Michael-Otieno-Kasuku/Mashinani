from graphviz import Digraph

# Define a color palette
color_palette = {
    'Applicant': '#87CEEB',  # Light Sky Blue
    'BursaryMashinaniPortal': '#98FB98',  # Pale Green
    'NGCDFProgram': '#FF6347',  # Tomato
    'FundingRequest': '#FFFFE0',  # Light Yellow
}

# Create a new graph
graph = Digraph('BursaryMashinaniClassDiagram', strict=True, format='png', engine='dot')

# Add classes with methods and attributes, applying colors from the palette
graph.node('Applicant', shape='record', color=color_palette['Applicant'], style='filled', fontcolor='black', label='{ Applicant | +ApplicantID\\l+Name\\l+NationalID\\l+StudentRegistrationNumber\\l+ContactInformation\\l| +applyForBursary()\\l }')
graph.node('BursaryMashinaniPortal', shape='record', color=color_palette['BursaryMashinaniPortal'], style='filled', fontcolor='black', label='{ BursaryMashinaniPortal | +PortalID\\l+TechnologyStack\\l+SecurityFeatures\\l+Database\\l| +submitApplication()\\l+checkApplicationStatus()\\l+generateReport()\\l+trackProgress()\\l }')
graph.node('NGCDFProgram', shape='record', color=color_palette['NGCDFProgram'], style='filled', fontcolor='black', label='{ NGCDFProgram | +ProgramID\\l+FundingAllocation\\l+Initiator\\l| +receiveFundingRequest()\\l+allocateFunds()\\l+disburseFunds()\\l }')
graph.node('FundingRequest', shape='record', color=color_palette['FundingRequest'], style='filled', fontcolor='black', label='{ FundingRequest | +RequestID\\l+AmountRequested\\l+Status\\l| +createRequest()\\l+updateStatus()\\l }')

# Add associations between classes
graph.edge('Applicant', 'BursaryMashinaniPortal', label='applies for', color='blue')
graph.edge('BursaryMashinaniPortal', 'NGCDFProgram', label='sends funding request to', color='green')
graph.edge('BursaryMashinaniPortal', 'FundingRequest', label='creates', color='green')
graph.edge('NGCDFProgram', 'FundingRequest', label='receives', color='red')

# Save the graph as a PNG file
graph.render('BursaryMashinaniClassDiagram', format='png', cleanup=True)

