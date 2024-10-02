import pandas as pd
import statsmodels.api as sm

# Load the data
df = pd.read_csv('Customer_Behavior.csv')

# List of categorical columns to encode
categorical_columns = ['Age Group', 'Gender', 'Loyalty Member', 'Product Type', 
                       'SKU', 'Order Status', 'Payment Method', 'Purchase Date', 
                       'Shipping Type']

# One-hot encode categorical columns
df_encoded = pd.get_dummies(df, columns=categorical_columns, drop_first=True)

# Separate the features and target variable
X = df_encoded.drop(['Total Price'], axis=1)  # Features
Y = df_encoded['Total Price']                   # Target variable

# Convert all columns to numeric (in case there are any non-numeric types)
X = X.apply(pd.to_numeric, errors='coerce')

# Check for NaNs and fill them with zero (if necessary)
X.fillna(0, inplace=True)

# Add a constant to the model (intercept)
X = sm.add_constant(X)

# Fit the regression model
model = sm.OLS(Y, X).fit()

# Print the regression results
print(model.summary())
