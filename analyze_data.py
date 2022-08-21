from dash import Dash, dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

app = Dash(__name__)

# Imports credit card data and categorization
credit_ledger_df = pd.read_csv("credit_ledger.csv")
credit_ledger_df["Date"] = pd.to_datetime(credit_ledger_df["Date"])

# Fidelity and Bank of America credit transactions
credit_FDT_df = pd.read_csv("download.csv")
credit_BAC_df = pd.read_csv("June2022_8641.csv")

# Imports type categorization
# Checks for any duplicate types
type_df = pd.read_csv("types.csv")
type_duplicates_df = type_df[type_df.duplicated()]
type_duplicates_df.to_csv("type_duplicates.csv")

# Process Fidelity Data
def append_credit_FDT(credit_ledger_df, credit_FDT_df):
    credit_FDT_df = credit_FDT_df.rename(columns={"Memo" : "Id"})
    credit_FDT_df = credit_FDT_df[credit_FDT_df["Transaction"] == "DEBIT"]
    credit_FDT_df = credit_FDT_df.drop("Transaction", axis=1)
    credit_FDT_df["Date"] = pd.to_datetime(credit_FDT_df["Date"])
    credit_FDT_df["Source"] = "Fidelity"

    # Checks if Id already exists in ledger and appends if not
    new_credit_FDT_df = credit_FDT_df[~credit_FDT_df["Id"].isin(credit_ledger_df["Id"])]
    credit_ledger_df = pd.concat([credit_ledger_df, new_credit_FDT_df])
    
    return credit_ledger_df

def append_credit_BAC(credit_ledger_df, credit_BAC_df):
    credit_BAC_df = credit_BAC_df.rename(columns={"Posted Date": "Date", "Reference Number": "Id", "Payee": "Name"})
    credit_BAC_df = credit_BAC_df[credit_BAC_df["Name"] != "BA ELECTRONIC PAYMENT"]
    credit_BAC_df = credit_BAC_df.drop("Address", axis=1)
    credit_BAC_df["Date"] = pd.to_datetime(credit_BAC_df["Date"])
    credit_BAC_df["Source"] = "Bank of America"

    new_credit_BAC_df = credit_BAC_df[~credit_BAC_df["Id"].isin(credit_ledger_df["Id"])]
    credit_ledger_df = pd.concat([credit_ledger_df, new_credit_BAC_df])
    credit_ledger_df.to_csv("credit_ledger.csv", index=False)

    return credit_ledger_df

# Creates new ledger with new data
credit_ledger_df = append_credit_FDT(credit_ledger_df, credit_FDT_df)
credit_ledger_df = append_credit_BAC(credit_ledger_df, credit_BAC_df)

credit_ledger_df.to_csv("credit_ledger.csv", index=False)

# Merges with type to categorize all entries
credit_categorized_df = credit_ledger_df.merge(type_df, how= "left", on= "Name")

# Selects uncategorized. Removes duplicates and returns csv of names needing categorization
uncategorized_df = credit_categorized_df[credit_categorized_df["Type"].isna()][["Name", "Type"]]
uncategorized_df = uncategorized_df[~uncategorized_df["Name"].duplicated()]
uncategorized_df.to_csv("uncategorized.csv", index=False)

credit_categorized_df.to_csv("credit_categorized.csv", index= False)

# Organizes data for graphing, this part is inefficient
grouped_df = credit_categorized_df.groupby([pd.Grouper(key= "Date", axis= 0, freq= "M"), "Name", "Type"]).sum()
grouped_df = grouped_df.reset_index()

# fig = px.bar(spending_df, x="Date", y="Amount", color="Type")
fig = px.bar(grouped_df, x="Date", y="Amount", color="Type", hover_name= "Name")
fig.show()

table = dbc.Table.from_dataframe(grouped_df, striped=True, bordered=True, hover=True)

app.layout = html.Div(
    [
        html.Div(
            [
                html.H5("Date Grouping"),
                dcc.Graph(figure= fig),
                table
            ]
        )
    ]
)

if __name__ == "__main__":
    app.run_server(debug= True)