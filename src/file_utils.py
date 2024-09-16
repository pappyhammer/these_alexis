import pandas as pd


def from_csv_to_df(csv_file, verbose=False, encoding="utf-8", remove_quotes=False):
    try:
        if remove_quotes:
            # in case you get this error:
            #  pandas.errors.ParserError: Error tokenizing data. C error: Expected 2 fields in line 7, saw 3
            # https://stackoverflow.com/questions/43891391/pandas-dataframe-read-skipping-line-xxx-expected-x-fields-saw-y
            # And the reason for that is the existence of a double quote in one of the fields which is causing
            #  Pandas to get confused so need to tell it not to look out for strings/quotes
            df = pd.read_csv(csv_file, encoding=encoding, low_memory=False, error_bad_lines=False, quoting=csv.QUOTE_NONE)
        else:
            df = pd.read_csv(csv_file, encoding=encoding, low_memory=False)  # , sep=';'
        n_entries = df.shape[0]
        columns = list(df)
    except pd.errors.ParserError:
        columns = [""]
    if len(columns) == 1:
        if remove_quotes:
            df = pd.read_csv(csv_file, encoding=encoding, low_memory=False, sep=';',
                             error_bad_lines=False, quoting=csv.QUOTE_NONE)
        else:
            df = pd.read_csv(csv_file, encoding=encoding, low_memory=False, sep=';')
        n_entries = df.shape[0]
        columns = list(df)
    if verbose:
        print(f"N entries {n_entries} in csv file")
        print(f"columns manual_db {len(columns)} {columns}")

    return df