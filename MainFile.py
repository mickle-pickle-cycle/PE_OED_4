import pandas as pd
from datetime import datetime

df = pd.read_csv("all.csv", sep=';', encoding="utf-8-sig")

df['days_gone'] = [date.days for date in datetime.today().replace(tzinfo=None) - pd.to_datetime(df['created_at']).dt.tz_convert(None)]
df.to_csv('all_update.csv', index=False, encoding='utf-8')
df['name'] = df['name'].str.lower().replace('[-,/]', ' ', regex=True).replace('\(.*\)','', regex=True).replace('c', 'с', regex=True)
df['name'] = df['name'].str.strip().replace('\s+', ' ', regex=True)
df['name'] = df['name'].str.replace('(1[СсCc])?.(битрикс|.bitrix)', '1C', regex=True)
df['name'] = df['name'].str.replace('([cс]#)|(net)|(asp)|(core)', 'C#', regex=True)
df['name'] = df['name'].str.replace('([сc][ ]*[+][ ]*[+])', 'C++', regex=True)
df['name'] = df['name'].str.replace('(front[ ]*[-]?[ ]*end)|(js)|(node)|(javascript)|(фронт[ ]*[-]?[ ]*енд)|(react)|(angular)|(vue)', 'JavaScript', regex=True)
df['name'] = df['name'].str.replace('(php)|(пхп)', 'PHP', regex=True)
df['name'] = df['name'].str.replace('(\\bjava\\b)', 'JAVA', regex=True)
df['name'] = df['name'].str.strip().replace('(ios)|(IOS)|(иос)', 'IOS', regex=True)
df['name'] = df['name'].str.strip().replace('(sql)|(oracle)|(postgres)', 'BD', regex=True)
df['name'] = df['name'].str.strip().replace('(android)|(андроид)|(SDK)|(sdk)', 'Android', regex=True)
df['name'] = df['name'].str.strip().replace('(python)|(питон)|(django)|(conda)', 'Python', regex=True)
df['name'] = df['name'].str.strip().replace('(\\bgo\\b)|(golang)', 'GO', regex=True)
df['name'] = df['name'].str.strip().replace('(delphi)', 'Delphi', regex=True)
df['name'] = df['name'].str.strip().replace('(ruby)', 'Ruby', regex=True)
df['name'] = df['name'].str.strip().replace('(unity)', 'Unity', regex=True)
groups = ['1C', 'C#', 'C++', 'JavaScript', 'PHP', 'JAVA', 'IOS', 'BD', 'Android', 'Python', 'GO', 'Delphi', 'Ruby', 'Unity']

def fill_avg_town_salary(df_group):
    city_groups = [_ for _, x in df_group.groupby('area')]
    for city in city_groups:
        min_salary_mean = (df_group.loc[(df_group['area'] == city)])[
            'min_salary'].mean()
        max_salary_mean = (df_group.loc[(df_group['area'] == city)])[
            'max_salary'].mean()
        df_group.loc[(df_group['area'] == city)
                     ]['max_salary'].fillna(max_salary_mean, inplace=True)
        df_group.loc[(df_group['area'] == city)
                     ]['min_salary'].fillna(min_salary_mean, inplace=True)
    return df_group


original_df = []
for idx, group in enumerate(groups):
    name_group = df[(df['name'].str.contains(group, na=False, regex=False))]
    name_group = fill_avg_town_salary(name_group)
    original_df.append(name_group)
    df = df[~df['name'].str.contains(group, na=False, regex=False)]
    name_group.to_csv('groups/'+group+'.csv', index=False, encoding='utf-8')

other = fill_avg_town_salary(df)
other.to_csv('groups/other.csv', index=False, encoding='utf-8')
df = other

df.append(original_df,).to_csv(
    'vacancies_data_updated.csv', index=False, encoding='utf-8')