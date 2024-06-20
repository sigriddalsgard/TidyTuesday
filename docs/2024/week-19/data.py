import json
import pandas as pd

df = pd.read_csv('rolling_stone.csv')

i = df[df['clean_name'] == 'Various Artists'].index
df.drop(i, inplace=True)

# Retter stavefejl
index = df[df['genre'] == 'Blues/Blues ROck'].index[0]
df.at[index, 'genre'] = 'Blues/Blues Rock'

# Tilfojer 0'er til alle raekker, som ikke har nogle uger
df['weeks_on_billboard'].fillna(0, inplace=True)

# Aendrer disse to kolonner til int i stedet for float
df['weeks_on_billboard'] = df['weeks_on_billboard'].astype(int)
df['debut_album_release_year'] = df['debut_album_release_year'].astype(int)

# Laver en ny csv
# df.reset_index(drop=False, inplace=True)
# df.to_csv('nyRollingStone.csv', index=False)


genre_group = df.groupby('genre')

weeks_list = df.groupby('genre')['weeks_on_billboard'].apply(list)
print(weeks_list)

max_length = weeks_list.apply(len).max()

# Liste af uger paa billboard
weeks = weeks_list.apply(lambda x: x + [0] * (max_length - len(x))).tolist()

# Liste af genrer
genre = df['genre'].unique().tolist()

# Liste af aar
years = df['debut_album_release_year'].unique().tolist()
years = [int(year) for year in years]

data_dict = {
    'weeks': {i: sublist for i, sublist in enumerate(weeks)},
    'genre': {i: item for i, item in enumerate(genre)},
    'years': {i: year for i, year in enumerate(years)}
}
# json_data = json.dumps(data_dict)
# print(json_data)

