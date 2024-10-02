import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv('Customer_Behavior.csv')

# Ensure 'Purchase Date' is in datetime format
df['Purchase Date'] = pd.to_datetime(df['Purchase Date'])

# Calculate the total revenue for each customer
customer_revenue = df.groupby('Customer ID')['Total Price'].sum().reset_index()
customer_revenue.columns = ['Customer ID', 'Total Revenue']

# Calculate the number of transactions for each customer
customer_transactions = df.groupby('Customer ID')['Purchase Date'].count().reset_index()
customer_transactions.columns = ['Customer ID', 'Total Transactions']

# Calculate the recency for each customer (days since last purchase)
latest_date = df['Purchase Date'].max()
customer_recency = df.groupby('Customer ID')['Purchase Date'].max().reset_index()
customer_recency['Recency'] = (latest_date - customer_recency['Purchase Date']).dt.days
customer_recency = customer_recency[['Customer ID', 'Recency']]

# Merge all metrics into one DataFrame
customer_clv = customer_revenue.merge(customer_transactions, on='Customer ID')
customer_clv = customer_clv.merge(customer_recency, on='Customer ID')

# Calculate the average value per transaction
customer_clv['Avg Transaction Value'] = customer_clv['Total Revenue'] / customer_clv['Total Transactions']

# Assuming an average customer lifespan of 5 years (can be adjusted)
average_customer_lifespan = 5

# Estimate CLV: Total Revenue * Average Lifespan
customer_clv['CLV'] = customer_clv['Total Revenue'] * average_customer_lifespan

# Sort by CLV to identify high-value customers
customer_clv_sorted = customer_clv.sort_values(by='CLV', ascending=False)

# Visualization of top 10 customers by CLV
plt.figure(figsize=(14, 7))
top_10_customers = customer_clv_sorted.head(10)

# Create a bar plot with Customer ID on the x-axis and CLV on the y-axis
sns.barplot(x='Customer ID', y='CLV', data=top_10_customers, palette='viridis', order=top_10_customers['Customer ID'])
plt.title('Top 10 Customers by Customer Lifetime Value (CLV)')
plt.xlabel('Customer ID')
plt.ylabel('Customer Lifetime Value (CLV)')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.grid()
plt.show()

# Visualization of Customer Lifetime Value (CLV) Distribution
plt.figure(figsize=(14, 7))
sns.histplot(customer_clv['CLV'], bins=30, kde=True)
plt.title('Distribution of Customer Lifetime Value (CLV)')
plt.xlabel('Customer Lifetime Value (CLV)')
plt.ylabel('Frequency')
plt.axvline(customer_clv['CLV'].mean(), color='red', linestyle='--', label='Mean CLV')
plt.axvline(customer_clv['CLV'].median(), color='orange', linestyle='--', label='Median CLV')
plt.xlim(left=0)
plt.legend()
plt.grid()
plt.show()