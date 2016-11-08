import pandas as pd
from personapi.models.models import Person


def parse_date(str):
    """
    Parse a date --> assuming m-d-Y format
    :param str: string
    :return: datetime
    """
    return pd.datetime.strptime(str, '%m-%d-%Y')


def ingest_file(file_path, delimiter):
    """
    Ingest a single file to a dataframe assuming DateofBirth is the only datecolumn
    :param file_path: filepath
    :param delimiter: the delimiter that tells you how to read the file
    :return: dataframe
    """
    return pd.read_csv(file_path, delimiter=delimiter, parse_dates=["DateOfBirth"], date_parser=parse_date)


def df_to_persons(df):
    """
    Dataframe -> [Person];
    note we only ingest the columns of the dataframe that are in the Person object
    extra columns are ignored, but can be added by adding the correct column header to the person object
    :param df: Pandas dataframe containing the ingested person files
    :return: [Person]
    """
    person_attrs = Person._fields
    col_mapping = {
        col: index
        for index, col in enumerate(df.columns)
    }
    persons = [
        Person(*[row[col_mapping[attr]] for attr in person_attrs])
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



