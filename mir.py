import pandas as pd

melon = pd.read_csv('./static/data/melondata.csv')

# Drop the 'lyrics' and 'comments' columns
melon = melon.drop(columns=['lyrics', 'comments'])
melon.to_csv('./static/data/melondata_edited.csv')