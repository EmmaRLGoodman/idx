import pandas as pd
sold_df = pd.read_csv("combinedsold.csv")
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