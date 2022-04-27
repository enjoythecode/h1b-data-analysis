import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

DATA_FOLDER = "data/"
RESULT_FOLDER = "result/"
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

    df["Year"] = fiscal_year
    print(f"Loaded data for FY {fiscal_year}")
    return fiscal_year, df

data_files = os.listdir(DATA_FOLDER)


data_frames = [load_csv(DATA_FOLDER+data_files[i]) for i in range(len(data_files))]
data_by_year = {str(year):df for (year, df) in data_frames}

all_data = pd.concat([df for (year, df) in data_frames])

####################
count_by_year = all_data.groupby("Year").sum()[:-1]
count_by_year.reset_index(inplace=True)
VISA_CAP = 85000
count_by_year["Expected Lottery Chance"] = VISA_CAP / count_by_year["Approvals"] * 100

fig, ax = plt.subplots(1,1, figsize=(12, 7))
color = "tab:blue"
ax.plot(count_by_year["Year"], count_by_year["Approvals"], color=color)
ax.set_xticks(list(range(2009, 2022)))
ax.set_xlabel("Fiscal Year")
ax.set_ylabel("Number of Approved H-1B Petitions", color=color)

color = 'tab:red'
ax2=ax.twinx()
ax2.plot(count_by_year["Year"], count_by_year["Expected Lottery Chance"], color=color)
ax2.set_ylabel("Expected Lottery Chance", color=color)
ax2.yaxis.set_major_formatter(mtick.PercentFormatter())
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
fig.savefig(RESULT_FOLDER + "approved_petitions_by_year.png")
####################

####################
data_2021 = data_by_year["2021"]
total_approvals_2021 = sum(data_2021["Approvals"])
data_2021["Share of All Approvals"] = data_2021["Approvals"] / total_approvals_2021 * 100

top_10_2021 = data_2021.sort_values(by=['Approvals'],ascending=False)[["Employer", "Approvals", "Share of All Approvals"]][:10]
top_10_2021.to_csv(RESULT_FOLDER + "top_10_employers_2021.csv")

top_10_employers = top_10_2021["Employer"]
####################

# TODO
# plot the number of petitions by the top 5 employers of 2022 across all years