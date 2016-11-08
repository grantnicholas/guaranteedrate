import enum


class TransformOptions(enum.Enum):
    GenderThenLastNameAsc = 1
    BirthDateAsc = 2
    LastNameDesc = 3


def get_transform(transform_option):
    """
    Gets the transform function associated with the TransformOption enum value
    :param transform_option: TransformOption enum
    :return: Func([Person] -> [Person])
    """
    if transform_option not in TransformOptions:
        raise ValueError("Unknown transformation option: {}".format(transform_option))

    transformations = {
        TransformOptions.GenderThenLastNameAsc: lambda persons: sorted(persons, key=lambda p: (p.Gender != "F", p.LastName)),
        TransformOptions.BirthDateAsc: lambda persons: sorted(persons, key=lambda p: p.DateOfBirth),
        TransformOptions.LastNameDesc: lambda persons: sorted(persons, key=lambda p: p.LastName, reverse=True),
    }

    return transformations[transform_option]


def transform_persons(persons, transform_option):
    """
    :param persons: [Person]
    :param transform_option: INT | TransformOption enum
    :return: [Person] transformed according to the TransformOption
    """
    transform_option = (
        transform_option if type(transform_option) == TransformOptions
        else TransformOptions(transform_option)
    )
    transform = get_transform(transform_option)
    return transform(persons)
