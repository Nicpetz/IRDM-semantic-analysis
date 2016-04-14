from Util.Import import get_files, load_original_file
import pandas as pd
import time


files = get_files('./Twitter')[:100]
word = 'Friday Monday'

word = word.split()

tic = time.time()
output = pd.DataFrame()
for file in files:
    df = load_original_file(file)
    #arr = [word[0].lower() in string.lower() or word[1].lower() in string.lower() for string in df.text]
    for w in word:
         arr = [w.lower() in string.lower() for string in df.text]
         df = df[arr]
         output = pd.concat([output, df])
         print(len(output))
    #df = df[arr]
    #output = pd.concat([output, df])


tock = time.time()

print("time: {}".format(tock - tic))
print(output.head())
print(len(output))
