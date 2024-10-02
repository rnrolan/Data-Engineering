import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv('Customer_Behavior.csv')

# Define the products and their add-ons
products = ['Impulse Item', 'Accessory', 'Extended Warranty']
product_types = df['Product Type'].unique()

# Create an empty DataFrame for the binary basket
basket = pd.DataFrame()

# Loop through each product type and create binary columns for each product and add-on
for product in product_types:
    for item in products:
        # Create a binary column for each combination of product type and item
        basket[f'{item} {product}'] = df.apply(
            lambda x: 1 if x[item] > 0 and x['Product Type'] == product else 0,
            axis=1
        )

# Optional: Add Customer ID for reference
basket['Customer ID'] = df['Customer ID']

# Group by Customer ID and sum the values
basket = basket.groupby('Customer ID').sum().reset_index()

# Ensure that the values in the basket are boolean (0 or 1)
basket[basket.columns[1:]] = basket[basket.columns[1:]].clip(lower=0, upper=1)

# Calculate the likelihood of buying each add-on for each product type
likelihood_df = pd.DataFrame(columns=products, index=products)

for product in product_types:
    for item in products:
        # Create the column name for accessing the data correctly
        add_on_column = f'{item} {product}'
        
        # Calculate the total count of the product type purchased
        total_product = basket[add_on_column].sum()
        
        # Calculate the count of customers who bought that product type and the add-on
        total_combined = basket[(basket[add_on_column] == 1) & (basket[add_on_column] == 1)].shape[0]
        
        # Calculate likelihood as a percentage
        likelihood = (total_combined / total_product * 100) if total_product > 0 else 0
        
        # Fill the likelihood DataFrame
        likelihood_df.loc[item, product] = likelihood  # Use correct indexing

# Melt the DataFrame for hierarchical plotting
likelihood_melted = likelihood_df.reset_index().melt(id_vars='index', var_name='Product Type', value_name='Likelihood')
likelihood_melted.columns = ['Add-on', 'Product Type', 'Likelihood']

# Create a bar plot for the likelihood
plt.figure(figsize=(12, 8))
sns.barplot(data=likelihood_melted, x='Product Type', y='Likelihood', hue='Add-on')
plt.title('Likelihood of Buying Add-ons by Product Type')
plt.ylabel('Likelihood (%)')
plt.xlabel('Product Type')
plt.xticks(rotation=45)
plt.legend(title='Add-ons')
plt.tight_layout()
plt.show()
