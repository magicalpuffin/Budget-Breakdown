import pandas as pd
import re

# Consider making the utils folder a module
def id_factory(parent_id: str):
    '''
    Function factory. Creates a function to append child-id to parent-id. Used for pages
    in dash due to unique id requirements.
    '''

    # Enables using  __name__. Removes file extension to be used as name
    if re.search(r".py", parent_id):
        parent_id = re.match(r".*(?=\.py)", parent_id).group(0)
    
    def func(child_id: str):
        return f"{parent_id}-{child_id}"
    return func

def clean_import(import_df):
    '''
    Evaluates if imported data is from Fidelity or Bank of America.
    Cleans the imported data into a standard format. [Date, ID, Name, Amount, Source].
    '''

    # Not even sure if there is a point, might be better to have source as a entered in field
    # Data from fidelity uses date while bank of america uses posted date
    # This is used to identify which type of filtering to use
    if import_df.columns[0] == 'Date':
        return clean_FDT(import_df)
    elif import_df.columns[0] == 'Posted Date':
        return clean_BAC(import_df)


def clean_FDT(FDT_data):
    '''
    Converts fidelity data into standard format
    '''
    
    # The structure of fidelity's data changed, should make it better format stuff
    # Using memo as id. Debit transactions are spending money. Payments are excluded
    # Not sure why I used drop instead of just slicing
    # Depending on how this function is used, convertind datetime now might be useless
    FDT_data = FDT_data.rename(columns={"Memo" : "Id"})
    FDT_data = FDT_data[FDT_data["Transaction"] == "DEBIT"]
    FDT_data = FDT_data.drop("Transaction", axis=1)
    
    # Removes excess semicolons in Id. Removes excess spaces
    FDT_data['Id'] = FDT_data['Id'].apply(lambda x: re.split(r";", x)[0])
    FDT_data['Name'] = FDT_data['Name'].apply(lambda x: re.sub(r"\s+", " ", x))
    FDT_data["Date"] = pd.to_datetime(FDT_data["Date"])
    FDT_data["Source"] = "Fidelity"

    return FDT_data

def clean_BAC(BAC_data):
    '''
    Converts bank of america data into a standard format
    '''
    
    # Bank of america requries more renaming
    # Electronic payments ignored, only looking at spending data
    # Will need to determine how to address cashback. Could filter and just make this expenses only
    BAC_data = BAC_data.rename(columns={"Posted Date": "Date", "Reference Number": "Id", "Payee": "Name"})
    BAC_data = BAC_data[BAC_data["Name"] != "BA ELECTRONIC PAYMENT"]
    BAC_data = BAC_data[BAC_data["Name"] != "CASH REWARDS STATEMENT CREDIT"]
    BAC_data = BAC_data.drop("Address", axis=1)
    BAC_data["Date"] = pd.to_datetime(BAC_data["Date"])
    BAC_data["Source"] = "Bank of America"

    return BAC_data

def append_ledger(ledger_df, new_df):
    '''
    Appends the new dataframe to the ledger
    '''

    # This is so simple it might be redundant having it as a function
    # Identifies what are the new data that would be added
    # Requires the data to be consistent
    # Returns the new ledger and what was added
    added_df = new_df[~new_df['Id'].isin(ledger_df['Id'])]
    ledger_df = pd.concat([ledger_df, added_df])
    return ledger_df, added_df

def add_types(ledger_df, type_df):
    '''
    Merges the type to categorize data
    '''

    # Merges the types
    # Identifies the data without a type. Removes duplicates
    ledger_categorized_df = ledger_df.merge(type_df, how= "left", on= "Name")
    
    uncategorized_df = ledger_categorized_df[ledger_categorized_df["Type"].isna()][["Name", "Type"]]
    uncategorized_df = uncategorized_df[~uncategorized_df["Name"].duplicated()]

    return ledger_categorized_df, uncategorized_df
