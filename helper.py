import numpy as np
def medal_tally(df):
    # Remove duplicate medals
    medal_tally = df.drop_duplicates(subset=[
        'Team', 'NOC', 'Year', 'City', 'Sport', 'Event', 'Medal'
    ])

    # Group by region and sum medals
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']]
    medal_tally = medal_tally.sort_values('Gold', ascending=False).reset_index()

    # Add total column
    medal_tally['total'] = (
        medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    )

    # Convert all columns to int
    medal_tally[['Gold', 'Silver', 'Bronze', 'total']] = medal_tally[[
        'Gold', 'Silver', 'Bronze', 'total'
    ]].astype(int)

    # Add Rank column starting at 1
    medal_tally.insert(0, 'Rank', range(1, len(medal_tally) + 1))

    return medal_tally


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')
    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')
    return  years,country


def fetch_medal_tally(df, years, country):
    flag = 0
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    if years == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if years == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if years != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(years)]  # always in string
    if years != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['region'] == country) & (medal_df['Year'] == int(years))]
    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
    x[['Gold', 'Silver', 'Bronze', 'total']] = x[[
        'Gold', 'Silver', 'Bronze', 'total'
    ]].astype(int)
    return x


def data_over_time(df,col):
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns={'Year': 'Edition', 'count': col}, inplace=True)
    return nations_over_time

def most_successful(df,sport):
    temp_df=df.dropna(subset=["Medal"])
    if sport !='Overall':
        temp_df= temp_df[temp_df['Sport']==sport]
    # return temp_df['Name'].value_counts().reset_index()
    x= temp_df['Name'].value_counts().reset_index().head(15).merge(df,left_on='Name',right_on='Name',how='left')[['Name','count','Sport','region']].drop_duplicates('Name').reset_index(drop=True)
    x.index += 1
    x.rename(columns={'Name	':'Name	','count':'Medals'},inplace=True)
    return x

def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    pt=new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt

def most_successful_country(df,country,count):
    temp_df=df.dropna(subset=["Medal"])
    temp_df= temp_df[temp_df['region']==country]
    # return temp_df['Name'].value_counts().reset_index()
    x= temp_df['Name'].value_counts().reset_index().head(10).merge(df,left_on='Name',right_on='Name',how='left')[['Name','count','Sport']].drop_duplicates('Name').reset_index(drop=True)
    x.index+=1
    x.rename(columns={'Name	':'Name	','count':'Medals'},inplace=True)
    if x.shape[0]<10:
        count=x.shape[0]
    return x,count



def men_vs_female(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    final.fillna(0, inplace=True)
    return final

def men_vs_female_total(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    final.fillna(0, inplace=True)
    gender_counts = athlete_df['Sex'].value_counts()

    # Create labels and values
    values = [gender_counts['M'], gender_counts['F']]
    return values