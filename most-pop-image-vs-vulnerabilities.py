import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the DataFrame from your Excel file
df = pd.read_excel('outfile-28-01.xlsx')

# Count the severity of vulnerabilities for each image
severity_counts = df.groupby(['Image', 'Severity'])['VulnerabilityID'].count().reset_index()

# Pivot the table to have 'Image' as rows and 'Severity' as columns
severity_pivot = severity_counts.pivot(index='Image', columns='Severity', values='VulnerabilityID').fillna(0)

# Calculate the total pull counts for each image
total_pull_counts = df.groupby('Image')['Total_Pull'].max()

# Sort images based on total pull counts and select the top 10
top_10_images = total_pull_counts.sort_values(ascending=False).head(10).index
severity_pivot_top_10 = severity_pivot.loc[top_10_images]

# Display the severity counts for each image
print("\nSeverity Counts for Each Image:")
print(severity_pivot_top_10)

# Write severity_pivot to a CSV file
severity_pivot_top_10.to_csv('severity_counts_top_10.csv')

# Plot the bar chart
plt.figure(figsize=(12, 6))
sns.barplot(data=severity_pivot_top_10.reset_index(), x='Image', y='CRITICAL', color='red', label='CRITICAL')
#sns.barplot(data=severity_pivot_top_10.reset_index(), x='Image', y='HIGH', color='orange', label='HIGH')
#sns.barplot(data=severity_pivot_top_10.reset_index(), x='Image', y='MEDIUM', color='yellow', label='MEDIUM')
#sns.barplot(data=severity_pivot_top_10.reset_index(), x='Image', y='LOW', color='green', label='LOW')

# Set labels and title
plt.xlabel('Image')
plt.ylabel('Count')
plt.title('Severity Counts for Top 10 Most Popular Images')

# Rotate x-axis labels for better readability (optional)
plt.xticks(rotation=90)

# Add legend
plt.legend(title='Severity')

# Show the plot
plt.tight_layout()
plt.show()
