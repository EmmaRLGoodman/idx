import pandas as pd

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
listing_df.to_csv("combinedlistings.csv", index=False)

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
sold_df.to_csv("combinedsold.csv", index=False)