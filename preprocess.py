import pandas as pd

melon = pd.read_excel('./static/data/melondata.xlsx', engine='openpyxl')

# Drop the 'lyrics' and 'comments' columns
melon = melon.drop(columns=['lyrics', 'comments'])
melon.to_csv('./static/data/melondata_edited.csv')