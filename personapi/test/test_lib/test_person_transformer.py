from personapi.lib.person_transformer import transform_persons, TransformOptions
from personapi.models.models import FileInfo, Person
import datetime
import pytest


persons = [
    Person(FirstName="Grant", LastName="Nicholas", Gender="M",
           FavoriteColor="Purple", DateOfBirth=datetime.datetime(year=1993, month=7, day=6, hour=0, minute=0)),
    Person(FirstName="Sally", LastName="Mae", Gender="F",
           FavoriteColor="Blue", DateOfBirth=datetime.datetime(year=1990, month=6, day=1, hour=0, minute=0)),
    Person(FirstName="Jillian", LastName="Nicholas", Gender="F",
           FavoriteColor="Purple", DateOfBirth=datetime.datetime(year=1992, month=1, day=1, hour=0, minute=0))
]


def test_transform_persons_birthdateasc():
    expected_persons = [
        Person(FirstName="Sally", LastName="Mae", Gender="F",
               FavoriteColor="Blue", DateOfBirth=datetime.datetime(year=1990, month=6, day=1, hour=0, minute=0)),
        Person(FirstName="Jillian", LastName="Nicholas", Gender="F",
               FavoriteColor="Purple", DateOfBirth=datetime.datetime(year=1992, month=1, day=1, hour=0, minute=0)),
        Person(FirstName="Grant", LastName="Nicholas", Gender="M",
               FavoriteColor="Purple", DateOfBirth=datetime.datetime(year=1993, month=7, day=6, hour=0, minute=0))
    ]
    transformed_persons = transform_persons(persons=persons, transform_option=TransformOptions.BirthDateAsc)

    assert  transformed_persons == expected_persons


def test_transform_persons_lastnamedesc():
    expected_persons = [
        Person(FirstName="Grant", LastName="Nicholas", Gender="M",
               FavoriteColor="Purple", DateOfBirth=datetime.datetime(year=1993, month=7, day=6, hour=0, minute=0)),
        Person(FirstName="Jillian", LastName="Nicholas", Gender="F",
               FavoriteColor="Purple", DateOfBirth=datetime.datetime(year=1992, month=1, day=1, hour=0, minute=0)),
        Person(FirstName="Sally", LastName="Mae", Gender="F",
               FavoriteColor="Blue", DateOfBirth=datetime.datetime(year=1990, month=6, day=1, hour=0, minute=0))
    ]
    transformed_persons = transform_persons(persons=persons, transform_option=TransformOptions.LastNameDesc)

    assert  transformed_persons == expected_persons


def test_transform_persons_genderthenlastnameasc():
    expected_persons = [
        Person(FirstName="Sally", LastName="Mae", Gender="F",
               FavoriteColor="Blue", DateOfBirth=datetime.datetime(year=1990, month=6, day=1, hour=0, minute=0)),
        Person(FirstName="Jillian", LastName="Nicholas", Gender="F",
               FavoriteColor="Purple", DateOfBirth=datetime.datetime(year=1992, month=1, day=1, hour=0, minute=0)),
        Person(FirstName="Grant", LastName="Nicholas", Gender="M",
               FavoriteColor="Purple", DateOfBirth=datetime.datetime(year=1993, month=7, day=6, hour=0, minute=0))
    ]
    transformed_persons = transform_persons(persons=persons, transform_option=TransformOptions.GenderThenLastNameAsc)

    assert  transformed_persons == expected_persons


def test_transform_persons_empty():
    assert transform_persons([], TransformOptions.BirthDateAsc) == []


def test_transform_persons_number_matches_enum():
    for opt in TransformOptions:
        assert (
            transform_persons(persons, transform_option=opt) == transform_persons(persons, transform_option=opt.value)
        )


def test_transform_num_out_of_range_raises_valuerror():
    with pytest.raises(ValueError) as e_info:
        transform_persons(persons, transform_option=0)