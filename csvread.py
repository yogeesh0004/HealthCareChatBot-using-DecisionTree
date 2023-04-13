import pandas as pd
df = pd.read_csv('doctors_dataset.csv', usecols=[0,1,2], names=['colA','colB','colC'])

print(df['colA'])
print(df['colB'])
print(df['colC'])
