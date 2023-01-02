import pandas as pd
from sklearn.tree import DecisionTreeClassifier

oriDataset: pd.DataFrame = pd.read_csv("E:\School Stuffs\Bachelor in Computer Science\Year 2\Sem 1\Artificial intelligence\Group assignment\Species_clustering_classification.csv")

healthDict: dict = oriDataset[["health", "health_number"]].set_index("health").to_dict()["health_number"]
speciesDict: dict = oriDataset[["species", "species_number"]].set_index("species").to_dict()["species_number"]

dataset: pd.DataFrame = oriDataset.copy()
dataset.drop(["health", "species"], axis=1, inplace=True)

inputCols: list[str] = ["Area", "species_number", "height", "crown_width", "dbh"]
outputCols: str = "health_number"

X: pd.DataFrame = dataset[inputCols]
y: pd.Series = dataset[outputCols]

dTree: DecisionTreeClassifier = DecisionTreeClassifier()
dTree = dTree.fit(X, y)

# Predict will only take 2d list.
def Predict(inputVals: list[list])->int:
    predResult: int = dTree.predict(inputVals)[0]
    return predResult

def GetKeyVal(dictionary: dict, val: float)->str:
    if val in dictionary.values():
        key: str = [k for k,v in dictionary.items() if v == val]
        return key[0]
    else:
        return None

def GetValKey(dictionary: dict, key: str)->float:
    if key in dictionary.keys():
        val: float = dictionary[key]
        return val
    else:
        return None