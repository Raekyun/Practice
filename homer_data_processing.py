import pandas as pd

df = pd.read_csv('NHCH.csv', index_col=0, parse_dates=True)
df = df.resample('H').sum()
print(df.head(3))

df.to_csv('NHCH_1H.csv')
