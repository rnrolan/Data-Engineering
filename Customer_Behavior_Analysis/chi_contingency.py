import pandas as pd
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt

# Load your dataset
df = pd.read_csv('Customer_Behavior.csv')

# Create a contingency table
contingency_table = pd.crosstab(df['Product Type'], df['Shipping Type'])

# Display the contingency table
print("Contingency Table:")
print(contingency_table)

# Perform the Chi-Square test
chi2, p, dof, expected = stats.chi2_contingency(contingency_table)

# Display the results
print("\nChi-Square Test Results:")
print(f"Chi2 Statistic: {chi2}")
print(f"P-Value: {p}")
print(f"Degrees of Freedom: {dof}")
print("Expected Frequencies:")
print(expected)

# Create a heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(contingency_table, annot=True, fmt='d', cmap='YlGnBu', cbar=True)
plt.title('Contingency Table Heatmap: Product Type vs. Shipping Type')
plt.xlabel('Shipping Type')
plt.ylabel('Product Type')
plt.show()
