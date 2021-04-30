import pandas as pd

#data.to_csv("./data/SAMI/earlies.csv")

morph_key = "morph"
sami = pd.read_csv("./data/SAMI/dr3.csv")

earlies = sami[sami[morph_key] < 1.5]
#lates_strict = sami[sami[morph_key] == 2]
lates = sami[sami[morph_key] >= 2.5]
#indexNames = lates[lates[morph_key] == 3].index #drop irregulars
#lates = lates.drop(indexNames)

#earlies.to_csv("./data/SAMI/earlies.csv")
#lates.to_csv("./data/SAMI/lates.csv")

#print(lates["morph"])

earlies.to_csv("./data/SAMI/earlies_vrot.csv")
lates.to_csv("./data/SAMI/lates_vrot.csv")
#lates_strict.to_csv("./data/SAMI/lates_strict_vrot.csv")