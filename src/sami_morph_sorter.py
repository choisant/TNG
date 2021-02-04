import pandas as pd

#data.to_csv("./data/SAMI/earlies.csv")

morph_key = "morph"
sami = pd.read_csv("./data/SAMI/all_data_vrot.csv")

elliptical = sami[sami[morph_key] == 0]
s0 = sami[sami[morph_key] == 1]
sa_sb = sami[sami[morph_key] == 2]
sc_sd_irr = sami[sami[morph_key] == 3]

elliptical.to_csv("./data/SAMI/ellipticals.csv")
s0.to_csv("./data/SAMI/s0.csv")
sa_sb.to_csv("./data/SAMI/sa_sb.csv")
sc_sd_irr.to_csv("./data/SAMI/sc_sd_irr.csv")
#lates_strict.to_csv("./data/SAMI/lates_strict_vrot.csv")