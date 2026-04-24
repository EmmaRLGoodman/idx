import pandas as pd
import matplotlib.pyplot as pl

#WEEK 1

sold_df = pd.read_csv("CRMLSSold202401.csv")
sold_line_count = sold_df.shape[0]
combined_sold_count = 0
for year in {"2024", "2025", "2026"}:
    for month in {"01", "02", "03",  "04", "05", "06", "07", "08",  "09", "10", "11", "12"}:
        if (not (year == "2026" and month not in {"01", "02", "03"})) and not (year=="2024" and month=="01"):
            csv_file = "CRMLSSold" + year + month + ".csv"
            temp_df = pd.read_csv(csv_file)
            sold_line_count += temp_df.shape[0]
            sold_df = pd.concat([sold_df, temp_df])
combined_sold_count = sold_df.shape[0]
print(sold_line_count) #591733
print(combined_sold_count) #591733
sold_df = sold_df[sold_df['PropertyType']=='Residential']
filtered_sold_count = sold_df.shape[0]
print(filtered_sold_count) #397603
#sold_df.to_csv("combinedsold.csv", index=False)

#WEEK 2/3

#note all analysis is done already filtering for residential
print(sold_df['ClosePrice'].mean())
print(sold_df['ClosePrice'].median())
#Rounding to integer values, mean close price is $1185616 and median is $820000 (right tailed distribution)
print(sold_df.shape)
#Shape is 397603, 84 (rows, columns)
rise_df = sold_df[sold_df['ClosePrice'] > sold_df['ListPrice']]
print(rise_df.shape)
print(rise_df['ClosePrice'].mean())
print(rise_df['ClosePrice'].median())
#159483 properties experienced a rise in price from listing to sale, meaning 238120 stayed the same or dropped.
#As would likely be expected, properties that had a higher closing price compared to listing had higher median and mean compared to general property.
sold_df.hist('BathroomsTotalInteger', bins=8)
#similar code can be used to generate all the histograms - notable outlier in ClosePrice going up to a billion on the x axis in its hist, put up on github.
#bathrooms integer also has a clear outlier causing the chart to go to 150.
pl.show()
sold_df.isnull().sum().to_csv("nullsums.csv")
#generates csv with missing sums for each column of the sold df (uploaded seperately on github)
#Some key takeaways - equal number of missing latfilled and lonfilled, presumably always both present or missing
#Some columns have very few occurences of missing data, such as PostalCode and ClosePrice - presumably data entry error
#FireplacesTotal, TaxAnnualAmount, TaxYear, CoveredSpaces, and BuisnessType all competely missing - some make sense for resdiential, but should fireplaces be completely gone?
#Of the not completely missing ones, BuildingAreaTotal, BuilderName, BasementYN, WaterfrontYN, MiddleorJuniorSchool, LotSizeDimensions,
#OriginatingSystemName, OriginatingSystemSubName, BuyerAgencyCompensationType, BuyerAgencyCompensation, and CoBuyerAgentFirstName all have low percentages of appearance

url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"
mortgage_df = pd.read_csv(url, parse_dates=['observation_date'])
mortgage_df.columns = ['date', 'rate_30yr_fixed']
mortgage_df['monthly'] = mortgage_df['date'].dt.to_period('M')
mortgage_df = mortgage_df.groupby('monthly')['rate_30yr_fixed'].mean().reset_index()
sold_df['monthly'] = pd.to_datetime(sold_df['CloseDate']).dt.to_period('M')
sold_rate_df = sold_df.merge(mortgage_df, on='monthly', how='left')
print(sold_rate_df['rate_30yr_fixed'].isnull().sum()) #prints 0 as expected