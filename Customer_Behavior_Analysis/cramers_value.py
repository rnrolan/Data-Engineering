import pandas as pd
import numpy as np
import scipy.stats as stats

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
df['Payment Method'] = df['Payment Method'].astype('category')
df = df.dropna(subset=['Product Type', 'Payment Method'])

# Create a contingency table
contingency_table = pd.crosstab(df['Product Type'], df['Payment Method'])

# Calculate Cramér's V
cramers_value = cramers_v(contingency_table)
print(f"Cramér's V between Product Type and Payment Method: {cramers_value:.4f}")
