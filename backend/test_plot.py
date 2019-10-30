# import seaborn as sns
# import matplotlib.pyplot as plt
import json

labels = ['a', 'b', 'c', 'd', 'e']
heights = [40, 30, 24, 17, 12]
dict_keys = ['label', 'height']
tup = list(zip(labels,heights))

dict_ =[{'label': t[0], 'height': t[1]} for t in tup]

with open('test_data.json', 'w') as f:
    json.dump(dict_, f)



# sns.barplot(x=labels, y=heights)
# plt.xlabel('word')
# plt.ylabel('frequency')
# plt.title('Visualizaiton of word frequencies in tweets of AndrewYang')
# plt.show()