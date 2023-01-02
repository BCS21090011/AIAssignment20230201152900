import pandas as pd
from sklearn.tree import DecisionTreeClassifier

# Read the file:
oriDataset: pd.DataFrame = pd.read_csv("E:\School Stuffs\Bachelor in Computer Science\Year 2\Sem 1\Artificial intelligence\Group assignment\Species_clustering_classification.csv")

healthDict: dict = oriDataset[["health", "health_number"]].set_index("health").to_dict()["health_number"]   # Contain the values in "health" as key and it's respective "health_number" as value.
speciesDict: dict = oriDataset[["species", "species_number"]].set_index("species").to_dict()["species_number"]  # Contain the values in "species" as key and it's respective "species_number" as value.

dataset: pd.DataFrame = oriDataset.copy()   # Will use this dataset. oriDataset won't be used or affected.
dataset.drop(["health", "species"], axis=1, inplace=True)

inputCols: list[str] = ["Area", "species_number", "height", "crown_width", "dbh"]
outputCols: str = "health_number"

X: pd.DataFrame = dataset[inputCols]
y: pd.Series = dataset[outputCols]

dTree: DecisionTreeClassifier = DecisionTreeClassifier()
dTree = dTree.fit(X.values, y.values)

# Make prediction:
def Predict(inputVals: list)->int:
    vals: list[list] = [inputVals]
    predResult: int = dTree.predict(vals)[0]
    return predResult

# Get the key of value in dictionary:
def GetKeyVal(dictionary: dict, val: float)->str:
    if val in dictionary.values():
        key: str = [k for k,v in dictionary.items() if v == val]
        return key[0]
    else:
        return None

# Get the value of key in dictionary:
def GetValKey(dictionary: dict, key: str)->float:
    if key in dictionary.keys():
        val: float = dictionary[key]
        return val
    else:
        return None
