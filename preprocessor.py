import pandas as pd

def process(df,region_df):
    df = pd.read_csv('olympics_dataset.csv')
    region_df = pd.read_csv('noc_regions.csv')
    df = df[df['Season'] == 'Summer']
    df = df.merge(region_df, on="NOC", how='left')
    df.drop_duplicates(inplace=True)

    # Create dummy variables
    medal_dummies = pd.get_dummies(df['Medal'])

    # Ensure all 3 medal types exist
    for medal in ['Gold', 'Silver', 'Bronze']:
        if medal not in medal_dummies.columns:
            medal_dummies[medal] = 0

    df = pd.concat([df, medal_dummies], axis=1)

    return df
