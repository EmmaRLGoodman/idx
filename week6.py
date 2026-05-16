import pandas as pd
sold_df = pd.read_csv("combinedsold.csv")
sold_df['CloseDate'] = pd.to_datetime(sold_df['CloseDate'])
sold_df['ListingContractDate'] = pd.to_datetime(sold_df['ListingContractDate'])
sold_df['PurchaseContractDate'] = pd.to_datetime(sold_df['PurchaseContractDate'])
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