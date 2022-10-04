import pandas as pd

data = pd.read_csv("C:\\Users\\jcy37\\PycharmProjects\\LidarEvaluation\\test2.csv")
print(data['GT'][0])

print(data['GT'][0][0:5])