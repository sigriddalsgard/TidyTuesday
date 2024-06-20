import pandas as pd

wwbi_country = pd.read_csv("/Users/sigriddalsgard/Developer/Observablehq/hobby/Sigrid/docs/2024/week-18/wwbi_country.csv")

wwbi_data = pd.read_csv("/Users/sigriddalsgard/Developer/Observablehq/hobby/Sigrid/docs/2024/week-18/wwbi_data.csv")

wwbi_series = pd.read_csv("/Users/sigriddalsgard/Developer/Observablehq/hobby/Sigrid/docs/2024/week-18/wwbi_series.csv")

df_data = pd.DataFrame(wwbi_data)
df_country = pd.DataFrame(wwbi_country)
df_series = pd.DataFrame(wwbi_series)


filtered_data = df_data[df_data['indicator_code'] == 'BI.PWK.PUBS.NO']

merged_df = pd.merge(df_country, filtered_data, on = 'country_code')

selected_columns = ['country_code', 'short_name', 'region', 'year', 'value']
merged_and_filtered = merged_df[selected_columns]

rename_dict = {
    'United States': 'United States of America',
    'Türkiye': 'Turkey',
    'Slovak Republic': 'Slovakia',
    'The Gambia': 'Gambia',
    'Dominican Republic': 'Dominican Rep.',
    'Czech Republic': 'Czechia',
    'Cyprus': 'N. Cyprus',
    'Central African Republic': 'Central African Rep.',
    'Bosnia and Herzegovina': 'Bosnia and Herz.',
    'West Bank and Gaza': 'Palestine'
}

merged_and_filtered['short_name'] = merged_and_filtered['short_name'].replace(rename_dict)

expected_names = [
    'United States of America',
    'Turkey',
    'Slovakia',
    'Gambia',
    'Dominican Rep.',
    'Czechia',
    'N. Cyprus',
    'Central African Rep',
    'Bosnia and Herz.',
    'Palestine'
]

check_df = merged_and_filtered[merged_and_filtered['short_name'].isin(expected_names)]

merged_and_filtered.to_csv('filtered_data.csv', index=False)

