import pandas as pd
import matplotlib.pyplot as plt

# Define the budget details with adjusted amounts
budget_data = {
    "Development Costs": [
        ("Software Development Team Salaries", 80000),
        ("Development Tools and Software Licenses", 2000),
        ("Cloud Services (if applicable)", 500),
        ("Hardware (if needed)", 28000),
        ("Miscellaneous Development Expenses", 1000)
    ],
    "Testing and Quality Assurance": [
        ("Testing Team Salaries", 48000),
        ("Testing Tools and Software Licenses", 3000),
        ("Quality Assurance Measures", 2500),
        ("Test Environments", 1000)
    ],
    "Deployment Expenses": [
        ("Server Hosting Fees", 5000),
        ("Domain Registration", 1000),
        ("SSL Certificate (if required)", 5000),
        ("Content Delivery Network (CDN) Costs", 7000),
        ("Deployment Tools and Software", 6000)
    ],
    "User Training and Documentation": [
        ("Training Materials Development", 15000),
        ("Trainer Fees", 18000),
        ("Training Venue Costs (if applicable)", 12000),
        ("Documentation Design and Printing", 6000)
    ],
    "Contingency Fund": [
        ("Unforeseen Expenses", 10000),
        ("Changes in Requirements", 5000),
        ("Emergency Support", 10000)
    ],
    "Vendor Selection and External Services": [
        ("External Development or Consulting Services", 20000),
        ("Vendor Fees for Third-Party Tools", 8000),
        ("Integration Costs", 5000)
    ],
    "Return on Investment (ROI) Assessment": [
        ("Cost-Benefit Analysis Tools", 7000),
        ("Economic and Social Impact Assessment", 12000),
        ("Evaluation Consultations", 15000)
    ],
    "Ongoing Maintenance and Support": [
        ("Maintenance Team Salaries", 30000),
        ("Support Tools and Software", 6000),
        ("Bug Fixes and Updates", 8000),
        ("Server Maintenance Costs", 10000)
    ],
    "Scalability Considerations": [
        ("Future Development Costs", 15000),
        ("Infrastructure Scaling Costs", 7000),
        ("Additional Licensing Fees", 5000)
    ],
    "Transparent Financial Structure": [
        ("Financial Reporting Tools", 10000),
        ("Accounting and Audit Services (if required)", 12000),
        ("Internal Communication Tools", 1000)
    ],
    "Monitoring and Evaluation": [
        ("Monitoring Tools and Software", 10000),
        ("Evaluation Services", 12000),
        ("Reporting Infrastructure", 8000)
    ]
}

# Allocate a budget limit
allocated_budget = 500000

# Create a list to store dictionaries
data_list = []

# Populate the list
subtotal_list = []
for category, expenses in budget_data.items():
    subtotal = sum(cost for _, cost in expenses)
    first_expense = True
    for expense, cost in expenses:
        if first_expense:
            data_list.append({"Category": category, "Expense": expense, "Cost": cost})
            first_expense = False
        else:
            data_list.append({"Category": "", "Expense": expense, "Cost": cost})
    data_list.append({"Category": "", "Expense": "Subtotal", "Cost": subtotal})
    subtotal_list.append(subtotal)

# Calculate the grand total
grand_total = sum(subtotal_list)

# Add the grand total row
data_list.append({"Category": "", "Expense": "Grand Total", "Cost": grand_total})

# Create a DataFrame
final_df = pd.DataFrame(data_list)

# Check if the total budget exceeds the allocated amount
if grand_total > allocated_budget:
    excess_amount = grand_total - allocated_budget
    print(f"Warning: The total budget ({grand_total} Ksh.) exceeds the allocated budget ({allocated_budget} Ksh.) by {excess_amount} Ksh.")

# Plot the budget table with improved formatting
fig, ax = plt.subplots(figsize=(12, 8))
ax.axis('off')  # Turn off the axis
table = ax.table(cellText=final_df.values, colLabels=final_df.columns, cellLoc='center', loc='center', colColours=['#f2f2f2']*3)
table.auto_set_font_size(False)  # Set font size manually
table.set_fontsize(10)
table.scale(1.2, 1.2)  # Adjust table size

# Save the budget table as a PNG file
plt.savefig('bursary_mashinani_budget.png', bbox_inches='tight')
plt.show()

