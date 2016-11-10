from collections import namedtuple


FileInfo = namedtuple("FileInfo", ["file_path", "delimiter"])


class Person(namedtuple("Person", ["LastName", "FirstName", "Gender", "FavoriteColor", "DateOfBirth"])):
    """
    A Person class; value object except that it knows how to output itself smartly (with __str__ and __repr__)
    """
    def __str__(self):
        return "Person(LastName='{0}', FirstName='{1}', Gender='{2}', FavoriteColor='{3}', DateOfBirth='{4}')".format(
            self.LastName, self.FirstName, self.Gender, self.FavoriteColor, self.DateOfBirth.strftime("%m/%d/%Y")
        )

    def __repr__(self):
        return str(self)
