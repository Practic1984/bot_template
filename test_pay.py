import pandas as pd
import seaborn as seaborn
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

data = pd.read_csv('polomki.csv', index_col='Магазин')
print(data)
seaborn.heatmap(data)