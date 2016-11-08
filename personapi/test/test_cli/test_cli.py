from personapi.cli.person_ingester import main, parseargs
from personapi.models.models import FileInfo
import pytest
from argparse import ArgumentTypeError


def test_parseargs_success():
    mock_args = ["-f", "a.txt", "b.txt", "c.txt", "-d", ",", "|", "space", "-t", "1"]
    transform_option, file_infos = parseargs(mock_args)

    print transform_option, file_infos

    assert transform_option == 1
    assert file_infos == [
        FileInfo(file_path="a.txt", delimiter=","),
        FileInfo(file_path="b.txt", delimiter="|"),
        FileInfo(file_path="c.txt", delimiter=" ")
    ]


def test_parseargs_nofiles():
    mock_args = ["-d",",","|","space","-t","1"]

    with pytest.raises(SystemExit) as e_info:
        transform_option, file_infos = parseargs(mock_args)


def test_tofileinfos_files_donot_match_delimiters():
    mock_args = ["-f", "a.txt", "b.txt", "-d", "|", "-t", "1"]
    with pytest.raises(ArgumentTypeError) as e_info:
        transform, fileinfos = parseargs(mock_args)


def test_invalid_transform():
    mock_args = ["-f", "a.txt", "b.txt", "-d", "|", ",", "-t", "4"]
    with pytest.raises(SystemExit) as e_info:
        transform, fileinfos = parseargs(mock_args)


def test_no_transform_option():
    mock_args = ["-f", "a.txt", "b.txt", "-d", "|", ","]
    with pytest.raises(SystemExit) as e_info:
        transform, fileinfos = parseargs(mock_args)


def test_main_integration(capsys, filepipepath, filecommapath, filewhitespacepath):
    mock_args = ["-f", filepipepath, filecommapath, filewhitespacepath, "-d", "|", ",", "space", "-t", "1"]
    main(mock_args)
    out, err = capsys.readouterr()

    expected_out = "[Person(FirstName='Sally', LastName='Mae', Gender='F', FavoriteColor='Blue', DateOfBirth='06/01/1990'), Person(FirstName='Sally', LastName='Mae', Gender='F', FavoriteColor='Blue', DateOfBirth='06/01/1990'), Person(FirstName='Sally', LastName='Mae', Gender='F', FavoriteColor='Blue', DateOfBirth='06/01/1990'), Person(FirstName='Grant', LastName='Nicholas', Gender='M', FavoriteColor='Purple', DateOfBirth='07/06/1993'), Person(FirstName='Grant', LastName='Nicholas', Gender='M', FavoriteColor='Purple', DateOfBirth='07/06/1993'), Person(FirstName='Grant', LastName='Nicholas', Gender='M', FavoriteColor='Purple', DateOfBirth='07/06/1993')]"

    assert out.strip() == expected_out.strip()
