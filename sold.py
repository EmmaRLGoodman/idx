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
null_df = sold_df.isnull().sum().to_frame()
null_df.columns=['Sum']
null_df['NullPercent'] = (null_df['Sum'] / 397603) * 100
null_df = null_df.sort_values(by="NullPercent", ascending=False)
print(null_df)
#generates csv with missing sums for each column of the sold df (uploaded seperately on github)
#Some key takeaways - equal number of missing latfilled and lonfilled, presumably always both present or missing
#Some columns have very few occurences of missing data, such as PostalCode and ClosePrice - presumably data entry error
#FireplacesTotal, TaxAnnualAmount, TaxYear, CoveredSpaces, and BuisnessType all competely missing - some make sense for resdiential, but should fireplaces be completely gone?
#Of the not completely missing ones, BuildingAreaTotal, BuilderName, BasementYN, WaterfrontYN, MiddleorJuniorSchool, LotSizeDimensions,
#OriginatingSystemName, OriginatingSystemSubName, BuyerAgencyCompensationType, BuyerAgencyCompensation, and CoBuyerAgentFirstName all have low percentages of appearance
sold_df = sold_df.drop(columns=["TaxYear", "FireplacesTotal", "TaxAnnualAmount", "AboveGradeFinishedArea", "ElementarySchoolDistrict", "CoveredSpaces", "MiddleOrJuniorSchoolDistrict", "BusinessType", "WaterfrontYN", "BelowGradeFinishedArea", "BasementYN", "LotSizeDimensions", "BuilderName", "BuildingAreaTotal", "CoBuyerAgentFirstName", "OriginatingSystemName", "OriginatingSystemSubName"])
#cuts out all the cols with over 90% missing
print(sold_df['ClosePrice'].max()) #989500000
print(sold_df['LivingArea'].max()) #17021321
print(sold_df['DaysOnMarket'].max()) #12430
print(sold_df['ClosePrice'].min()) #0
print(sold_df['LivingArea'].min()) #0
print(sold_df['DaysOnMarket'].min()) #-288
print(sold_df['ClosePrice'].quantile([.25, .75])) #575000, 1300000
print(sold_df['LivingArea'].quantile([.25, .75])) #1247, 2217
print(sold_df['DaysOnMarket'].quantile([.25, .75])) #8, 48
print(sold_df['ClosePrice'].mean()) #1185616.36
print(sold_df['LivingArea'].mean()) #1904.35
print(sold_df['DaysOnMarket'].mean()) #37.34
print(sold_df['ClosePrice'].median()) #820000
print(sold_df['LivingArea'].median()) #1641
print(sold_df['DaysOnMarket'].median()) #19

url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"
mortgage_df = pd.read_csv(url, parse_dates=['observation_date'])
mortgage_df.columns = ['date', 'rate_30yr_fixed']
mortgage_df['monthly'] = mortgage_df['date'].dt.to_period('M')
mortgage_df = mortgage_df.groupby('monthly')['rate_30yr_fixed'].mean().reset_index()
sold_df['monthly'] = pd.to_datetime(sold_df['CloseDate']).dt.to_period('M')
sold_rate_df = sold_df.merge(mortgage_df, on='monthly', how='left')
print(sold_rate_df['rate_30yr_fixed'].isnull().sum())
#prints 0 as expected.
print(sold_rate_df[['CloseDate', 'monthly', 'rate_30yr_fixed']].head())

#week 4/5

sold_df['CloseDate'] = pd.to_datetime(sold_df['CloseDate'])
sold_df['ListingContractDate'] = pd.to_datetime(sold_df['ListingContractDate'])
sold_df['PurchaseContractDate'] = pd.to_datetime(sold_df['PurchaseContractDate'])
sold_df['listing_after_close_flag'] = (sold_df['ListingContractDate']>sold_df['CloseDate'])
sold_df['purchase_after_close_flag'] = (sold_df['PurchaseContractDate']>sold_df['CloseDate'])
sold_df['purchase_after_listing_flag'] = (sold_df['PurchaseContractDate']<sold_df['ListingContractDate'])
sold_df['negative_timeline_flag'] = (sold_df['listing_after_close_flag'] | sold_df['purchase_after_close_flag'] | sold_df['purchase_after_listing_flag'])
print(sold_df[sold_df['negative_timeline_flag']].shape) #501 flagged rows
print(sold_df.shape) #397603 before transform
sold_df = sold_df[(sold_df['ClosePrice']>0) & (sold_df['LivingArea']>0) & (sold_df['DaysOnMarket']>=0) & (sold_df['BathroomsTotalInteger']>=0) & (sold_df['BedroomsTotal']>=0)]
print(sold_df.shape) #397123 after transform
sold_df['null_geo_flag'] = ((sold_df['Latitude'] == 0) | (sold_df['Latitude'] is None) | (sold_df['Longitude'] == 0) | (sold_df['Longitude'] is None))
sold_df['invalid_long_flag'] = sold_df['Longitude'] > 0
print(sold_df[sold_df['null_geo_flag']].shape) #25 flagged rows
print(sold_df[sold_df['invalid_long_flag']].shape) #29 flagged rows
sold_df = sold_df[(~sold_df['negative_timeline_flag']) & (~sold_df['null_geo_flag']) & (~sold_df['invalid_long_flag'])]
print(sold_df.shape) #396569 rows after removing flagged rows
sold_df = sold_df.drop(columns=['negative_timeline_flag', 'null_geo_flag', 'invalid_long_flag', 'listing_after_close_flag', 'purchase_after_close_flag', 'purchase_after_listing_flag'])

#WEEK 6
"""
sold_df['PriceRatio'] = sold_df['ClosePrice'] / sold_df['OriginalListPrice']
sold_df['PricePerSqFt'] = sold_df['ClosePrice'] / sold_df['LivingArea']
sold_df['ListingToContract'] = sold_df['PurchaseContractDate'] - sold_df['ListingContractDate']
sold_df['ContractToClose'] = sold_df['CloseDate'] - sold_df['PurchaseContractDate']
print(sold_df[['PriceRatio', 'PricePerSqFt', 'ListingToContract', 'ContractToClose', 'CountyOrParish']].groupby(by='CountyOrParish').describe())
print(sold_df[['PriceRatio', 'PricePerSqFt', 'ListingToContract', 'ContractToClose', 'MLSAreaMajor']].groupby(by='MLSAreaMajor').describe())
print(sold_df[['PriceRatio', 'PricePerSqFt', 'ListingToContract', 'ContractToClose', 'PropertyType']].groupby(by='PropertyType').describe())
print(sold_df[['PriceRatio', 'PricePerSqFt', 'ListingToContract', 'ContractToClose', 'PropertySubType']].groupby(by='PropertySubType').describe())
print(sold_df[['PriceRatio', 'PricePerSqFt', 'ListingToContract', 'ContractToClose', 'ListOfficeName']].groupby(by='ListOfficeName').describe())
print(sold_df[['PriceRatio', 'PricePerSqFt', 'ListingToContract', 'ContractToClose', 'BuyerOfficeName']].groupby(by='BuyerOfficeName').describe())
"""
#WEEK 7

q1 = sold_df['ClosePrice'].quantile(.25)
q3 = sold_df['ClosePrice'].quantile(.75)
iqr = q3 - q1
low = q1 - 1.5 * iqr
high = q3 + 1.5 * iqr
sold_df['ClosePriceHighOutlierFlag'] = sold_df['ClosePrice']>high
sold_df['ClosePriceLowOutlierFlag'] = sold_df['ClosePrice']<low
q1 = sold_df['LivingArea'].quantile(.25)
q3 = sold_df['LivingArea'].quantile(.75)
iqr = q3 - q1
low = q1 - 1.5 * iqr
high = q3 + 1.5 * iqr
sold_df['LivingAreaHighOutlierFlag'] = sold_df['LivingArea']>high
sold_df['LivingAreaLowOutlierFlag'] = sold_df['LivingArea']<low
q1 = sold_df['DaysOnMarket'].quantile(.25)
q3 = sold_df['DaysOnMarket'].quantile(.75)
iqr = q3 - q1
low = q1 - 1.5 * iqr
high = q3 + 1.5 * iqr
sold_df['DaysOnMarketHighOutlierFlag'] = sold_df['DaysOnMarket']>high
sold_df['DaysOnMarketLowOutlierFlag'] = sold_df['DaysOnMarket']<low
print(sold_df.shape) #396569 rows
print(sold_df['ClosePrice'].median()) #820000
print(sold_df['LivingArea'].median()) #1641
print(sold_df['DaysOnMarket'].median()) #19
sold_df = sold_df[(~sold_df['DaysOnMarketHighOutlierFlag']) & (~sold_df['DaysOnMarketLowOutlierFlag']) & (~sold_df['LivingAreaHighOutlierFlag']) & (~sold_df['LivingAreaLowOutlierFlag']) & (~sold_df['ClosePriceHighOutlierFlag']) & (~sold_df['ClosePriceLowOutlierFlag'])]
print(sold_df.shape) #334763 rows (~60k entries removed)
print(sold_df['ClosePrice'].median()) #785000
print(sold_df['LivingArea'].median()) #1568
print(sold_df['DaysOnMarket'].median()) #16