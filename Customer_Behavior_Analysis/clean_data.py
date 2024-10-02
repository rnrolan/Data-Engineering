import pandas as pd

df = pd.read_csv("/Users/razel/Python_Projects/Customer_Purchase_Behavior.csv")
print(df.info())
print(df.isnull().sum())
print(df.head())

df['Add-ons Purchased'] = df['Add-ons Purchased'].fillna('None')
df['Gender'] = df['Gender'].fillna(df['Gender'].mode()[0])

df.to_csv('Customer_Behavior_Cleaned.csv', index=False)

