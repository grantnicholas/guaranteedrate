import argparse
from personapi.lib.file_ingester import ingest_files
from personapi.models.models import FileInfo
from personapi.lib.person_transformer import transform_persons, TransformOptions
import sys


def to_fileinfos(args):
    """
    Validates and converts the arguments object from argparse into structured info for the app to use
    :param args: Argparsee arguments object
    :return: (TransformOption, [FileInfo])
    """
    if args.files is None or len(args.files) == 0:
        raise  argparse.ArgumentTypeError("Must supply at least one file argument; try `python person-ingester.py -f {filepath} -d {'delimiter'}")
    if args.delimiters is None or len(args.files) != len(args.delimiters):
        raise argparse.ArgumentTypeError("Must supply the same number of arguments for -files and -delimiters")

    # replace the literal 'space' to avoid issues with whitespace and cli parsing
    args.delimiters = [arg if arg != 'space' else ' ' for arg in args.delimiters]

    return args.transform, [
        FileInfo(file_path=file_path, delimiter=delimiter)
        for file_path, delimiter in zip(args.files, args.delimiters)
    ]


def parseargs(sysargv):
    """
    The CLI parser
    :param sysargv: sys.argv values supplied to the python script
    :return: (transform_option, [FileInfo])
    """
    parser = argparse.ArgumentParser(description='')
    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument('-files', metavar='files', type=str, nargs='+', help='-files a.txt b.txt', required=True)
    required_named.add_argument('-delimiters', metavar='delimiters', type=str, nargs='+', help="-delimiters '|' ',' 'space'", required=True)
    required_named.add_argument(
        '-transform', metavar='transform', type=int, choices=[o.value for o in TransformOptions],
        help="choose one way to sort the data: " + ", ".join(
            "{val} -> {name}".format(val=o.value, name=o.name) for o in TransformOptions
        ),
        required=True
    )
    args = parser.parse_args(args=sysargv)
    transform_option, file_infos = to_fileinfos(args)
    return transform_option, file_infos


def main(sysargv):
    #parseargs, ingestfiles, transform persons, then output the persons to stdout
    transform_option, file_infos = parseargs(sysargv)
    persons = ingest_files(file_infos=file_infos)
    transformed_persons = transform_persons(persons=persons, transform_option=transform_option)
    print transformed_persons


if __name__ == "__main__":
    main(sys.argv[1:])






