import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('data/rtu_dangjin.csv', index_col=0, parse_dates=True, skiprows=2)
