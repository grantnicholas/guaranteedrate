import pandas as pd
from personapi.models.models import Person
from StringIO import StringIO


def parse_date(str):
    """
    Parse a date --> assuming m-d-Y format
    :param str: string
    :return: datetime
    """
    return pd.datetime.strptime(str, '%m-%d-%Y')


def ingest_string(string, delimiter, header=True):
    string_io = StringIO(string)
    return ingest_file(string_io, delimiter=delimiter, header=header)


def ingest_file(file_path, delimiter, header=True):
    """
    Ingest a single file to a dataframe assuming DateofBirth is the only datecolumn
    :param file_path: filepath
    :param delimiter: the delimiter that tells you how to read the file
    :return: dataframe
    """
    return (
        pd.read_csv(file_path, delimiter=delimiter, parse_dates=["DateOfBirth"], date_parser=parse_date) if header
        else pd.read_csv(file_path, delimiter=delimiter, parse_dates=[4], date_parser=parse_date, header=None)
    )


def df_to_persons(df, header=True):
    """
    Dataframe -> [Person];
    note we only ingest the columns of the dataframe that are in the Person object
    extra columns are ignored, but can be added by adding the correct column header to the person object
    :param df: Pandas dataframe containing the ingested person files
    :return: [Person]
    """
    col_mapping = {
        col: index
        for index, col in enumerate(df.columns)
    }

    # If we have a header, then we can ingest the data by the header name
    # Otherwise assume that the data is in the correct order
    attrs = [col_mapping[attr] for attr in Person._fields] if header else [index for index in range(len(df.columns))]
    persons = [
        Person(*[row[attr] for attr in attrs])
        for i, row in df.iterrows()
    ]

    return persons


def concat_persons(persons_list):
    """
    Flattens the [[Person]] -> [Person]
    :param persons_list: [[Person]]
    :return: [Person]
    """
    return [p for lst in persons_list for p in lst]


def ingest_files(file_infos):
    """
    Converts a list of fileinfos to a list of persons
    :param file_infos: [FileInfo]
    :return: [Person]
    """
    persons = concat_persons([
        df_to_persons(ingest_file(file_path=file_info.file_path, delimiter=file_info.delimiter))
        for file_info in file_infos
    ])
    return persons



