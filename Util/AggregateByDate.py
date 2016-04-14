"""
A script to aggregate the tweets by day and hour for future analysis
"""

from Util.Import import *
import datetime

files = get_files("../Twitter")

count = 0
df = pd.DataFrame()
for file in files:
    loaded = load_original_file(file)

    Titles = []
    for i in loaded.index:
        Date = loaded.iloc[i].date.date()
        Title = str(str(Date) + ".txt")

        #Time = loaded.iloc[i].date.time().hour
        #Title = str(str(Date) + "-" + str(Time) + ".txt")


        Titles.append(Title)

    loaded["Titles"] = Titles


    for T in loaded.Titles.unique():
        dfTemp = loaded[loaded.Titles == T]
        dfTemp.reset_index()
        count+=len(dfTemp)
        print(count)
        try:
            dfTemp2 = load_new_file('../DataByDay/' + T)
            dfTemp = pd.merge([dfTemp2, dfTemp])
            dfTemp.to_json('../DataByDay/' + T, orient= "index")
        except:
            dfTemp.to_json('../DataByDay/' + T, orient= "index")





