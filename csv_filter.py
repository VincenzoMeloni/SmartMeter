import pandas as pd

input_path = r"C:\INFORMATICA\Magistrale\1-ANNO\OSM-[IOT]\Progetto_IOT_residential\DataSet\house3.csv"
output_path = r"C:\INFORMATICA\Magistrale\1-ANNO\OSM-[IOT]\Progetto_IOT_residential\DataSet\DATASET.csv"

df = pd.read_csv(input_path)

res3_cols = df.filter(like="residential3")

df["Contatore"] = res3_cols.sum(axis=1)

df["Potenza"] = df["Contatore"].diff() / (1/60) #kW

df["Potenza"].fillna(0, inplace=True)

df_final = df[["timestamp", "Contatore", "Potenza"]]

df_final.to_csv(output_path, index=False, float_format="%.6f")

print("File creato con successo!")
print(f"Output salvato in: {output_path}")
