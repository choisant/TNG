def save_data_CSV(df, filename, tngFolder):
    path = "./data/"+tngFolder+"/cutdata/"+filename+".csv"
    f = open(path, "a+") #Create file if it does not already exist.
    df.to_csv(path)