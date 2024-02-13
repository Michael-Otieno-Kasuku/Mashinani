import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta

# Define the key milestones and timeline
milestones = {
    "Requirements Analysis": ["2024-01-08", "2024-01-15", "Gather Functional Requirements and Document in SRS Document"],
    "System Design": ["2024-01-16", "2024-01-30", "Develop detailed system design and Document in SDD Document"],
    "Implementation (Coding) Phase 1": ["2024-01-31", "2024-02-15", "Implement the Bursary application Algorithm"],
    "Implementation (Coding) Phase 2": ["2024-02-16", "2024-03-05", "Implement Bursary Application Tracking Algorithm"],
    "Testing Phase 1": ["2024-03-06", "2024-03-15", "Conduct Testing and bug fixing"],
    "User Training and Documentation": ["2024-03-16", "2024-03-20", "Develop user documentation and conduct training"],
    "Deployment": ["2024-03-21", "2024-03-25", "Deploy system and monitor performance"]
}

# Create a DataFrame for Gantt chart
df = pd.DataFrame(list(milestones.items())[::-1], columns=['Task', 'Date Range'])
df['Start'] = pd.to_datetime(df['Date Range'].apply(lambda x: x[0] + " 00:00:00"))
df['End'] = pd.to_datetime(df['Date Range'].apply(lambda x: x[1] + " 23:59:59"))

# Calculate the duration of each task
df['Duration'] = df['End'] - df['Start']

# Calculate the number of days from the start for each task
df['Days From Start'] = (df['Start'] - df['Start'].min()).dt.days

# Plotting the detailed Gantt chart
fig, ax = plt.subplots(figsize=(12, 8))
for i, task in enumerate(df['Task']):
    ax.barh(task, width=df['Duration'].iloc[i].days, left=df['Days From Start'].iloc[i], label=df['Date Range'].iloc[i])

# Formatting the plot
ax.set_xlabel('Timeline (Days from Start)')
ax.set_ylabel('Tasks')
ax.set_title('Bursary Mashinani Gantt Chart')
ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

# Save the detailed Gantt chart as a PNG file
plt.savefig('bursary_mashinani_gantt_chart.png', bbox_inches='tight')
plt.show()

