import os
import pandas as pd
#import matplotlib.pyplot as plt

DATA_FOLDER = "data/"
NORMALIZE_COLUMN_NAME_MAPPING = {
    "Initial Approval": "Initial Approvals",
    "Initial Denial": "Initial Denials",
    "Continuing Approval": "Continuing Approvals",
    "Continuing Denial": "Continuing Denials"
}

def load_csv(filename):

    df = pd.read_csv(filename, thousands=",")
    fiscal_year = df["Fiscal Year"][0]
    df.rename(columns=NORMALIZE_COLUMN_NAME_MAPPING, inplace=True)
    df.drop(["NAICS", "Tax ID", "State", "City", "ZIP"], axis = 1, inplace=True)
    df.fillna(0,inplace=True)
    df["Initial Approvals"] = pd.to_numeric(df["Initial Approvals"])
    df["Initial Denials"] = pd.to_numeric(df["Initial Denials"])
    df["Continuing Approvals"] = pd.to_numeric(df["Continuing Approvals"])
    df["Continuing Denials"] = pd.to_numeric(df["Continuing Denials"])
    
    df["Approvals"] = df["Initial Approvals"] + df["Continuing Approvals"]
    df["Denials"] = df["Initial Denials"] + df["Continuing Denials"]

    aggregation_functions = {'Approvals': 'sum', "Denials": 'sum'}
    df = df.groupby(df["Employer"]).aggregate(aggregation_functions)
    df.reset_index(inplace=True)

    #print(df[df["Employer"] == "DELOITTE CONSULTING LLP"])
    #print(sum(df["Approvals"]))
    #print(df.sort_values(by=['Approvals'],ascending=False))
    df["Year"] = fiscal_year
    print(f"Loaded data for FY {fiscal_year}")
    return fiscal_year, df

data_files = os.listdir(DATA_FOLDER)


data_frames = [load_csv(DATA_FOLDER+data_files[i]) for i in range(len(data_files))]
data_by_year = {str(year):df for (year, df) in data_frames}

all_data = pd.concat([df for (year, df) in data_frames])
print(all_data)
print(all_data[all_data["Employer"] == "DELOITTE CONSULTING LLP"])

# 