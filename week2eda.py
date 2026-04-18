import pandas as pd
import matplotlib.pyplot as pl

#note all analysis is done already filtering for residential
sold_df = pd.read_csv("combinedsold.csv")
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