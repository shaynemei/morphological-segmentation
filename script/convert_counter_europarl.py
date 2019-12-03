import pickle
from collections import Counter

with open("./europarl-v7.de-en.true.de") as f:
    data = f.readlines()

data = [line.lower().replace("\n","") for line in data]
data = " ".join(data)
data = data.split()
count_data = Counter(data)

with open('./freq_europarl', 'wb') as outputfile:
	pickle.dump(count_data, outputfile)