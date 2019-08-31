import pandas as pd

data = pd.ExcelFile('iabbd_8010_v1_gender.xls')


# Now define a function for doing the reshape
def reshape_func(excel_obj, j):
    """ Takes in an excel file object with multiple tabs in a wide format,
    and a specified index of the tab to be parsed and reshaped. Returns a
    data frame of the specified tab reshaped to long format"""

    tabnames = data.sheet_names
    assert j < len(tabnames), "Your tab index exceeds the number of available tabs, try a lower number"

    host_country_list = []
    for y in tabnames[1:]:
        host_country_list.append(data.parse(str(y)).columns[0])

    df = excel_obj.parse(tabnames[j+1])
    # # make a list of the header row and strip up to the 4th letter. This is the location and year information

    my_iter = iter(df.columns)
    for i in range(0, len(df.columns)):
        next_item = next(my_iter)
        if i in [1, 4, 7, 10, 13, 16, 19]:
            df = df.drop([next_item], axis=1)
    df = df.drop([0, 1, 2])

    df = df.iloc[1:, :].rename(columns={
        list(df)[0]: 'country_birth',
        'Unnamed: 2': '1980-M',
        'Unnamed: 3': '1980-F',
        'Unnamed: 5': '1985-M',
        'Unnamed: 6': '1985-F',
        'Unnamed: 8': '1990-M',
        'Unnamed: 9': '1990-F',
        'Unnamed: 11': '1995-M',
        'Unnamed: 12': '1995-F',
        'Unnamed: 14': '2000-M',
        'Unnamed: 15': '2000-F',
        'Unnamed: 17': '2005-M',
        'Unnamed: 18': '2005-F',
        'Unnamed: 20': '2010-M',
        'Unnamed: 21': '2010-F'
    }
    )

    # Engineer a new column for the country, grab this name from the excel tab name
    df['country_host'] = host_country_list[j]

    # # Then pivot the dataset based on this multi-level index
    idx = ['country_birth', 'country_host']
    multi_indexed_df = df.set_index(idx)

    # Stack the columns to achieve the baseline long format for the data
    stacked_df = multi_indexed_df.stack(dropna=False)

    # Now do a reset to disband the multi-level index, we only needed it to pivot our data during the reshape
    long_df = stacked_df.reset_index()

    # Make series of lists which split year from target age-group
    # the .str attribute is how you manipulate the data frame objects and columns with strings in them
    col_str = long_df.level_2.str.split("-")

    # engineer the columns we want, one columns takes the first item in col_str and another columns takes the second
    long_df['year'] = [x[0] for x in col_str]
    long_df['gender'] = [x[1] for x in col_str]
    long_df['quantity'] = long_df[0] # rename this column

    # drop the now redundant columns
    df_final = long_df.drop(['level_2', 0], axis=1)

    return df_final


dfs_list = [reshape_func(data, i) for i in range(20)]
concat_dfs = pd.concat(dfs_list)
concat_dfs.to_excel("reshaping_result_long_format.xls")
