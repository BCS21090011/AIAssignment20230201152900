import pandas as pd
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from matplotlib import pyplot as plt

# Read the file:
oriDataset: pd.DataFrame = pd.read_csv("Dataset.csv")

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
def Predict(inputVals: list)->float:
    vals: list[list] = [inputVals]
    predResult: float = dTree.predict(vals)[0]
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

# Save the tree diagram:
def SaveTreeDiagram(saveFileName: str="TreeDiagram.png"):
    tree.plot_tree(dTree, feature_names=dataset.columns)
    plt.savefig(saveFileName)

if __name__ == "__main__":
    # ----------------Interface----------------

    import tkinter as tk
    from tkinter import messagebox
    from tkinter import ttk

    def Validate(userInput: str)->bool:
        try:
            float(userInput)
            return True
        except ValueError:
            return False

    def ValidateEntry(userInput: str)->bool:
        valid: bool = Validate(userInput)

        if userInput == "":
            valid = True
        else:
            if userInput[0] == '-': # If it is negative:
                valid = userInput[1:]   # Check if the rest is valid.

                if userInput[1:] == "": # If the rest is empty.
                    valid = True

        return valid

    def ValidateComboBox(inVal: str, validInputs: list)->bool:
        return (inVal in validInputs)

    def LabelValid(label: tk.Label, trueText: str, falseText: str, valid: bool):
        if valid == True:
            label["text"] = trueText
        else:
            label["text"] = falseText

    def PredictButton_OnClick():
        AreaInput: str = AreaInputEntry.get()
        speciesInput: str = SpeciesInputComboBox.get()
        HeightInput: str = HeightInputEntry.get()
        CrownWidthInput: str = CrownWidthInputEntry.get()
        DBHInput: str = DBHInputEntry.get()

        AreaInputValid: bool = Validate(AreaInput)
        SpeciesInputValid: bool = ValidateComboBox(speciesInput, speciesKeyList)
        HeightInputValid: bool = Validate(HeightInput)
        CrownWidthInputValid: bool = Validate(CrownWidthInput)
        DBHInputValid: bool = Validate(DBHInput)

        LabelValid(AreaInputLabel, "Area:", "Area:\t[Invalid]", AreaInputValid)
        LabelValid(SpeciesInputLabel, "Species:", "Species:\t[Invalid]", SpeciesInputValid)
        LabelValid(HeightInputLabel, "Height:", "Height:\t[Invalid]", HeightInputValid)
        LabelValid(CrownWidthInputLabel, "Crown width:", "Crown width:\t[Invalid]", CrownWidthInputValid)
        LabelValid(DBHInputLabel, "DBH:", "DBH:\t[Invalid]", DBHInputValid)

        if all(v is not False for v in [AreaInputValid, SpeciesInputValid, HeightInputValid, CrownWidthInputValid, DBHInputValid]):
            userInputs[0] = float(AreaInput)
            userInputs[1] = GetValKey(speciesDict, speciesInput)
            userInputs[2] = float(HeightInput)
            userInputs[3] = float(CrownWidthInput)
            userInputs[4] = float(DBHInput)

            predValFloat: float = Predict(userInputs)
            predValStr: str = GetKeyVal(healthDict, predValFloat)

            messagebox.showinfo(title="Prediction result", message=f"Prediction result: {predValStr:^16}")

    root: tk.Tk = tk.Tk()
    root.geometry("700x500")
    root.title("Predict")

    healthKeyList: list = list(healthDict.keys())
    speciesKeyList: list = list(speciesDict.keys())

    userInputs: list[float] = [0, 0, 0, 0, 0]

    AreaInputLabel: tk.Label = tk.Label(root, text="Area:")
    AreaInputLabel.pack()
    AreaTxtVar: tk.StringVar = tk.StringVar(root)
    AreaTxtVar.set(0)
    AreaInputEntry: tk.Entry = tk.Entry(root, textvariable=AreaTxtVar, justify="center")
    AreaInputEntry.config(validate="key", validatecommand=(AreaInputEntry.register(ValidateEntry), '%P'))
    AreaInputEntry.pack()

    SpeciesInputLabel: tk.Label = tk.Label(root, text="Species:")
    SpeciesInputLabel.pack()
    SpeciesTxtVar: tk.StringVar = tk.StringVar(root)
    SpeciesTxtVar.set(speciesKeyList[0])
    SpeciesInputComboBox: ttk.Combobox = ttk.Combobox(root, values=speciesKeyList, textvariable=SpeciesTxtVar, justify="center")
    SpeciesInputComboBox.pack()

    HeightInputLabel: tk.Label = tk.Label(root, text="Height:")
    HeightInputLabel.pack()
    HeightTxtVar: tk.StringVar = tk.StringVar(root)
    HeightTxtVar.set(0)
    HeightInputEntry: tk.Entry = tk.Entry(root, textvariable=HeightTxtVar, justify="center")
    HeightInputEntry.config(validate="key", validatecommand=(HeightInputEntry.register(ValidateEntry), '%P'))
    HeightInputEntry.pack()

    CrownWidthInputLabel: tk.Label = tk.Label(root, text="Crown width:")
    CrownWidthInputLabel.pack()
    CrownWidthTxtVar: tk.StringVar = tk.StringVar(root)
    CrownWidthTxtVar.set(0)
    CrownWidthInputEntry: tk.Entry = tk.Entry(root, textvariable=CrownWidthTxtVar, justify="center")
    CrownWidthInputEntry.config(validate="key", validatecommand=(CrownWidthInputEntry.register(ValidateEntry), '%P'))
    CrownWidthInputEntry.pack()

    DBHInputLabel: tk.Label = tk.Label(root, text="DBH:")
    DBHInputLabel.pack()
    DBHTxtVar: tk.StringVar = tk.StringVar(root)
    DBHTxtVar.set(0)
    DBHInputEntry: tk.Entry = tk.Entry(root, textvariable=DBHTxtVar, justify="center")
    DBHInputEntry.config(validate="key", validatecommand=(DBHInputEntry.register(ValidateEntry), '%P'))
    DBHInputEntry.pack()

    PredictButton: tk.Button = tk.Button(root, text="Predict", command=PredictButton_OnClick)
    PredictButton.pack()

    root.mainloop()
