import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your dataset
df = pd.read_csv('Customer_Behavior.csv')

# Group by Customer ID to calculate total purchases and total spending
loyalty_data = df.groupby('Customer ID').agg(
    Total_Purchases=('SKU', 'count'),   # Count of purchases (or SKU)
    Total_Spending=('Total Price', 'sum')  # Total spending
).reset_index()

# Define loyalty criteria
min_purchases = 4      # Minimum number of purchases to be considered loyal
min_spending = 1000    # Minimum total spending to be considered loyal

# Identify loyal customers
loyal_customers = loyalty_data[
    (loyalty_data['Total_Purchases'] >= min_purchases) & 
    (loyalty_data['Total_Spending'] >= min_spending)
]
print(loyal_customers)
average_spending = loyal_customers['Total_Spending'].mean()
average_purchases = loyal_customers['Total_Purchases'].mean()
print(f"Average Total Spending of Loyal Customers: ${average_spending:.2f}")
print(f"Average Total Purchases of Loyal Customers: {average_purchases:.2f}")

plt.figure(figsize=(14, 7))
sns.histplot(loyal_customers['Total_Spending'], bins=30, kde=True)
plt.title('Distribution of Total Spending Among Loyal Customers')
plt.xlabel('Total Spending ($)')
plt.ylabel('Frequency')
plt.axvline(loyal_customers['Total_Spending'].mean(), color='red', linestyle='--', label='Mean Spending')
plt.legend()
plt.grid()
plt.show()
