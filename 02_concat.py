import pandas as pd
import glob

data_path = glob.glob('./data32mb/reviews*.csv')
print(data_path)

df = pd.DataFrame()

for path in data_path:
    df_temp = pd.read_csv(path)
    df_temp.dropna(inplace=True) #none drop
    df = pd.concat([df, df_temp], ignore_index=True)

df.drop_duplicates(inplace=True)
df.info()
df.to_csv('./reviews_32mb.csv', index=False)

