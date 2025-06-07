import pandas as pd

# Load the CSV files into Pandas DataFrames
circuits_df = pd.read_csv("circuits.csv")
races_df = pd.read_csv("races.csv")
results_df = pd.read_csv("results.csv")

# Display the first few rows of each DataFrame
circuits_df.head(), races_df.head(), results_df.head()
