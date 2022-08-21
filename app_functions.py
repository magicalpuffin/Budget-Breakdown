import pandas as pd

def df_to_excel(df_list, name_list, file_name = "py_excel_output.xlsx"):
    """
    Exports an excel file of all dataframes. Uses file_name for file name and name_list for sheet names. \n
    Arguments: \n
        df_list: List of dataframes to exported to excel. List length for df and name should be the same. \n
        name_list: List of names corresponding to each dataframe. Sheet name of each dataframe. \n
        file_name: Name of the excel file to be exported. Will default to py_excel_output.xlsx \n
    """
    # Uses openpyxl and pandas
    # Loops through, assigning each dataframe to corresponding sheet name
    # This function may be better done using an dictionary
    datatoexcel = pd.ExcelWriter(file_name)
    for df, name in zip(df_list, name_list):
        df.to_excel(excel_writer = datatoexcel, sheet_name = name)
    datatoexcel.save()
    return