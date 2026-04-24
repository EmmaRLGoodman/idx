import pandas as pd

#WEEK 1

listing_df = pd.read_csv("CRMLSListing202401.csv")
listing_line_count = listing_df.shape[0]
combined_listing_count = 0
for year in {"2024", "2025", "2026"}:
    for month in {"01", "02", "03",  "04", "05", "06", "07", "08",  "09", "10", "11", "12"}:
        if (not (year == "2026" and month not in {"01", "02", "03"})) and not (year=="2024" and month=="01"):
            csv_file = "CRMLSListing" + year + month + ".csv"
            temp_df = pd.read_csv(csv_file)
            listing_line_count += temp_df.shape[0]
            listing_df = pd.concat([listing_df, temp_df])
combined_listing_count = listing_df.shape[0]
print(listing_line_count) #852963
print(combined_listing_count) #852963
listing_df = listing_df[listing_df['PropertyType']=='Residential']
filtered_listing_count = listing_df.shape[0]
print(filtered_listing_count) #540183
#isting_df.to_csv("combinedlistings.csv", index=False)

#WEEK 2/3

url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"
mortgage_df = pd.read_csv(url, parse_dates=['observation_date'])
mortgage_df.columns = ['date', 'rate_30yr_fixed']
mortgage_df['monthly'] = mortgage_df['date'].dt.to_period('M')
mortgage_df = mortgage_df.groupby('monthly')['rate_30yr_fixed'].mean().reset_index()
listing_df['monthly'] = pd.to_datetime(listing_df['ListingContractDate']).dt.to_period('M')
listing_rate_df = listing_df.merge(mortgage_df, on='monthly', how='left')
print(listing_rate_df['rate_30yr_fixed'].isnull().sum()) #prints 0 as expected