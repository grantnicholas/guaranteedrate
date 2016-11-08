from collections import namedtuple


FileInfo = namedtuple("FileInfo", ["file_path", "delimiter"])


class Person(namedtuple("Person", ["FirstName", "LastName", "Gender", "FavoriteColor", "DateOfBirth"])):
    """
    A Person class; value object except that it knows how to output itself smartly (with __str__ and __repr__)
    """
    def __str__(self):
        return "Person(FirstName='{0}', LastName='{1}', Gender='{2}', FavoriteColor='{3}', DateOfBirth='{4}')".format(
            self.FirstName, self.LastName, self.Gender, self.FavoriteColor, self.DateOfBirth.strftime("%m/%d/%Y")
        )

    def __repr__(self):
        return str(self)
