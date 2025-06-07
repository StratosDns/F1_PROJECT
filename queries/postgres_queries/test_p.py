import pandas as pd
from sqlalchemy import create_engine

# Adjust credentials as needed
engine = create_engine('postgresql://postgres:1234@localhost:5432/F1_Analysis')

# Example: all British drivers
query = "SELECT * FROM drivers WHERE nationality = 'British';"
df = pd.read_sql(query, engine)
print(df)