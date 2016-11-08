from personapi.lib.file_ingester import ingest_file, df_to_persons, parse_date, ingest_files, concat_persons
from personapi.models.models import Person, FileInfo
import pandas as pd
from pandas.util.testing import assert_frame_equal
import datetime


expected_df = pd.DataFrame({
    "LastName": ["Nicholas", "Mae"],
    "FirstName": ["Grant", "Sally"],
    "Gender": ["M", "F"],
    "FavoriteColor": ["Purple", "Blue"],
    "DateOfBirth": [
        datetime.datetime(year=1993, month=7, day=6, hour=0, minute=0),
        datetime.datetime(year=1990, month=6, day=1, hour=0, minute=0)
    ]
}, columns=[
    "LastName", "FirstName", "Gender", "FavoriteColor", "DateOfBirth"
])


def test_date_parse():
    str = "07-06-1993"
    date = parse_date(str)
    assert date == datetime.datetime(year=1993, month=7, day=6, hour=0, minute=0)


def test_ingest_pipe_file(filepipepath):
    df = ingest_file(file_path=filepipepath, delimiter='|')

    assert_frame_equal(df, expected_df)
    assert type(df["DateOfBirth"][0]) == pd.tslib.Timestamp


def test_ingest_comma_file(filecommapath):
    df = ingest_file(file_path=filecommapath, delimiter=',')

    assert_frame_equal(df, expected_df)
    assert type(df["DateOfBirth"][0]) == pd.tslib.Timestamp


def test_ingest_whitespace_file(filewhitespacepath):
    df = ingest_file(file_path=filewhitespacepath, delimiter=' ')

    assert_frame_equal(df, expected_df)
    assert type(df["DateOfBirth"][0]) == pd.tslib.Timestamp


def test_df_to_persons():
    expected_persons = [
        Person(FirstName="Grant", LastName="Nicholas", Gender="M",
               FavoriteColor="Purple", DateOfBirth=datetime.datetime(year=1993, month=7, day=6, hour=0, minute=0)),
        Person(FirstName="Sally", LastName="Mae", Gender="F",
               FavoriteColor="Blue", DateOfBirth=datetime.datetime(year=1990, month=6, day=1, hour=0, minute=0))
    ]

    persons = df_to_persons(expected_df)

    assert expected_persons == persons


def test_concat_persons():
    persons = [
        Person(FirstName="Grant", LastName="Nicholas", Gender="M",
               FavoriteColor="Purple", DateOfBirth=datetime.datetime(year=1993, month=7, day=6, hour=0, minute=0)),
        Person(FirstName="Sally", LastName="Mae", Gender="F",
               FavoriteColor="Blue", DateOfBirth=datetime.datetime(year=1990, month=6, day=1, hour=0, minute=0))
    ]
    person_inputs  = [persons for _ in xrange(3)]
    person_outputs = persons * 3
    persons = concat_persons(person_inputs)

    assert persons == person_outputs


def test_ingest_three_files(filepipepath, filecommapath, filewhitespacepath):
    expected_persons = [
        Person(FirstName="Grant", LastName="Nicholas", Gender="M",
               FavoriteColor="Purple", DateOfBirth=datetime.datetime(year=1993, month=7, day=6, hour=0, minute=0)),
        Person(FirstName="Sally", LastName="Mae", Gender="F",
               FavoriteColor="Blue", DateOfBirth=datetime.datetime(year=1990, month=6, day=1, hour=0, minute=0))
    ]*3

    persons = ingest_files([
        FileInfo(file_path=filepipepath, delimiter='|'),
        FileInfo(file_path=filecommapath, delimiter=','),
        FileInfo(file_path=filewhitespacepath, delimiter=' ')
    ])

    assert persons == expected_persons





