import datetime
import pandas as pd
import glob



data_paths = glob.glob('./crawling_data/20*.csv')
print(data_paths)

df = pd.DataFrame()

for path in data_paths:
    df_temp = pd.read_csv(path)
    df_temp.dropna(inplace=True)
    df_temp.drop_duplicates(inplace=True)
    df = pd.concat([df, df_temp], ignore_index=True)
df.drop_duplicates(inplace=True)
df.info()

df.to_csv('./crawling_data/reviews_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d')), index=False)
