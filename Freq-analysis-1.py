import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_excel('Outfile-28-01.xlsx')

# Verify the column names
print("Columns in the DataFrame:", df.columns.tolist())

# Calculate the frequency of each vulnerability
vulnerability_frequency = df['VulnerabilityID'].value_counts().reset_index()
vulnerability_frequency.columns = ['VulnerabilityID', 'Frequency']  # Correcting column names

# Check the column names after renaming
print("Column names in vulnerability_frequency after renaming:", vulnerability_frequency.columns.tolist())

# Aggregate the total last week pulls for each vulnerability
vuln_last_wk_pulls = df.groupby('VulnerabilityID')['Last_wk_Pull'].sum().reset_index()

# Check the column names in vuln_last_wk_pulls
print("Column names in vuln_last_wk_pulls:", vuln_last_wk_pulls.columns.tolist())

# Merge this with the vulnerability frequency data
vulnerability_insights = vulnerability_frequency.merge(vuln_last_wk_pulls, on='VulnerabilityID')

# Sort by Frequency to get the top vulnerabilities
vulnerability_insights = vulnerability_insights.sort_values(by='Frequency', ascending=False)

# Select the top 10 vulnerabilities for a clearer plot
top_vulnerabilities = vulnerability_insights.head(10)

# Set up the matplotlib figure
plt.figure(figsize=(12, 6))

# Create a bar plot for the frequencies
sns.barplot(x='VulnerabilityID', y='Frequency', data=top_vulnerabilities, color='blue', label='Frequency')

# Create a line plot for the last week's pulls on a secondary y-axis
ax2 = plt.gca().twinx()
sns.lineplot(x='VulnerabilityID', y='Last_wk_Pull', data=top_vulnerabilities, color='red', marker='o', ax=ax2, label='Last Week Pulls')

# Improve the formatting of the plot
plt.xticks(rotation=45, ha='right')
plt.title('Top 10 Vulnerabilities by Frequency and Last Week\'s Pulls')
plt.xlabel('Vulnerability ID')
plt.ylabel('Frequency')
ax2.set_ylabel('Total Last Week Pulls')

# Show the legend
plt.legend(loc='upper left')
ax2.legend(loc='upper right')

# Show the plot
plt.tight_layout()  # Adjust the plot to ensure everything fits without overlapping
plt.show()
