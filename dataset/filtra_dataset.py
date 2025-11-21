import pandas as pd

df = pd.read_csv(r"C:\INFORMATICA\Magistrale\1-ANNO\OSM-[IOT]\opsd-household_data-2020-04-15\opsd-household_data-2020-04-15\household_data_1min_singleindex.csv")

house3 = df.filter(like="residential3")

house3["timestamp"] = df["utc_timestamp"]

house3 = house3.interpolate().fillna(0)

house3.to_csv("house3.csv", index=False)

print("CSV filtrato salvato come 'house3.csv'")
