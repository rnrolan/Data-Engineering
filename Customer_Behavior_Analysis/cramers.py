import pandas as pd
import numpy as np
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt

# Function to calculate Cramér's V
def cramers_v(confusion_matrix):
    chi2 = stats.chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    phi2 = chi2 / n
    r, k = confusion_matrix.shape
    return np.sqrt(phi2 / min(k - 1, r - 1))

# Load your dataset
df = pd.read_csv('Customer_Behavior.csv')

# Ensure the columns are categorical and drop any rows with null values
df['Product Type'] = df['Product Type'].astype('category')
df['Shipping Type'] = df['Shipping Type'].astype('category')
df = df.dropna(subset=['Product Type', 'Shipping Type'])

# Create a contingency table
contingency_table = pd.crosstab(df['Product Type'], df['Shipping Type'])

# Initialize a list to store the results
results = []

# Calculate Cramér's V for each combination of Product Type and Shipping Type
for product in df['Product Type'].unique():
    for payment in df['Shipping Type'].unique():
        # Create a 2x2 contingency table for each combination
        sub_table = pd.crosstab(df['Product Type'] == product, df['Shipping Type'] == payment)
        if sub_table.shape[0] == 2 and sub_table.shape[1] == 2:  # Ensure it's a 2x2 table
            cramers_value = cramers_v(sub_table)
            results.append({'Product Type': product, 'Shipping Type': payment, 'Cramér\'s V': cramers_value})

# Convert the results list to a DataFrame
results_df = pd.DataFrame(results)

# Display results
print(results_df)

# Pivot the results DataFrame for heatmap
heatmap_data = results_df.pivot_table(index='Product Type', columns='Shipping Type', values='Cramér\'s V')

# Create a heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(heatmap_data, annot=True, fmt='.2f', cmap='YlGnBu', cbar_kws={'label': "Cramér's V"})
plt.title("Cramér's V Heatmap: Product Type vs Shipping Type")
plt.xlabel("Shipping Type")
plt.ylabel("Product Type")
plt.show()