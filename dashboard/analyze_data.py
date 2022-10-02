from dash import Dash, dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

app = Dash(__name__)

# Code reorganization
    # Key functionality
        # Clean import data
        # Append data to ledger
        # Merges ledger with types
    # Web app functionality
        # Allows importing data and appending
        # Histogram of analysis and viewing ledger
        # Editing and adding types
        # Data storage, ledger and types
    # Development
        # Code reorganization. Page > Tabs > Content > Callbacks?
        # The objective is to make tabs their own folder keep callbacks and content next to each other
        # this would make it possible to develop each tab independently. Ideally allow importing each tab




# Imports credit card data and categorization
# Will need to mess around with indexes
# credit_ledger_df = pd.read_csv("dashboard/data/credit_ledger.csv")
# credit_ledger_df["Date"] = pd.to_datetime(credit_ledger_df["Date"])

# Fidelity and Bank of America credit transactions
# credit_FDT_df = pd.read_csv("download.csv")
# credit_BAC_df = pd.read_csv("June2022_8641.csv")


# Imports type categorization
# Checks for any duplicate types
# type_df = pd.read_csv("types.csv")
# type_duplicates_df = type_df[type_df.duplicated()]
# type_duplicates_df.to_csv("type_duplicates.csv")

def clean_import(import_df):
    '''
    Evaluates if imported data is from Fidelity or Bank of America. \n
    Cleans the imported data into a standard format. [Date, Name, ID, Amount, Source]. \n
    '''

    if import_df.columns[0] == 'Date':
        return clean_FDT(import_df)
    elif import_df.columns[0] == 'Posted Date':
        return clean_BAC(import_df)


def clean_FDT(FDT_data):
    FDT_data = FDT_data.rename(columns={"Memo" : "Id"})
    FDT_data = FDT_data[FDT_data["Transaction"] == "DEBIT"]
    FDT_data = FDT_data.drop("Transaction", axis=1)
    FDT_data["Date"] = pd.to_datetime(FDT_data["Date"])
    FDT_data["Source"] = "Fidelity"

    return FDT_data

def clean_BAC(BAC_data):
    BAC_data = BAC_data.rename(columns={"Posted Date": "Date", "Reference Number": "Id", "Payee": "Name"})
    BAC_data = BAC_data[BAC_data["Name"] != "BA ELECTRONIC PAYMENT"]
    BAC_data = BAC_data.drop("Address", axis=1)
    BAC_data["Date"] = pd.to_datetime(BAC_data["Date"])
    BAC_data["Source"] = "Bank of America"

    return BAC_data

def append_ledger(ledger_df, new_df):
    added_df = new_df[~new_df['Id'].isin(ledger_df['Id'])]
    ledger_df = pd.concat([ledger_df, added_df])
    return ledger_df, added_df

def add_types(ledger_df, type_df):
    ledger_categorized_df = ledger_df.merge(type_df, how= "left", on= "Name")
    
    uncategorized_df = ledger_categorized_df[ledger_categorized_df["Type"].isna()][["Name", "Type"]]
    uncategorized_df = uncategorized_df[~uncategorized_df["Name"].duplicated()]

    return ledger_categorized_df, uncategorized_df


# Merges with type to categorize all entries
# credit_categorized_df = credit_ledger_df.merge(type_df, how= "left", on= "Name")

# # Selects uncategorized. Removes duplicates and returns csv of names needing categorization
# uncategorized_df = credit_categorized_df[credit_categorized_df["Type"].isna()][["Name", "Type"]]
# uncategorized_df = uncategorized_df[~uncategorized_df["Name"].duplicated()]
# uncategorized_df.to_csv("uncategorized.csv", index=False)

# credit_categorized_df.to_csv("credit_categorized.csv", index= False)
