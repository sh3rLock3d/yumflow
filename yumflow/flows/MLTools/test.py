import pandas as pd
from main import append_data
df = pd.DataFrame([[1, 2], [3, 4]], columns=list('AB'), )
df2 = pd.DataFrame([[5, 6], [7, 8]], columns=list('AB'),)

print(df)
print('1111111111')
print(df2)
res = append_data(df, df2)
print('1111111111')
print(res)