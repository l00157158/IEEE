import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def convert_to_numeric(val):
    if isinstance(val, str):
        if 'K' in val:
            return float(val.replace('K', '')) * 1000
        if 'M' in val:
            return float(val.replace('M', '')) * 1000000
        # Add more conditions if there are other notations
    return float(val)

# Load the data
df = pd.read_excel('outfile-28-01.xlsx')

# Convert 'Total_Pull' and 'Stars' to numeric values
df['Total_Pull'] = df['Total_Pull'].apply(convert_to_numeric)
df['Stars'] = df['Stars'].apply(convert_to_numeric)

# Aggregating vulnerability data per image
vuln_agg = df.groupby('Image').agg({'VulnerabilityID': 'count'})  # Counting the number of vulnerabilities per image
vuln_agg.rename(columns={'VulnerabilityID': 'Vuln_Count'}, inplace=True)

# Aggregating popularity data
popularity_agg = df.groupby('Image').agg({'Total_Pull': 'max', 'Stars': 'max'})  # Assuming max is a suitable aggregator

# Merging the two datasets
merged_data = vuln_agg.merge(popularity_agg, on='Image')

# Calculating correlation
correlation_matrix = merged_data.corr()

# Plotting the heatmap for the correlation matrix
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)

# Adding titles and labels
plt.title('Correlation Matrix Heatmap')
plt.xlabel('Dataset Features')
plt.ylabel('Dataset Features')

# Show the plot
plt.show()
