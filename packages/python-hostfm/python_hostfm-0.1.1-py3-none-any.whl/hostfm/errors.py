class Base(Exception):
    """Base class"""

    def __init__(self, *args: object) -> None:
        if not args:
            # super().__init__(" ".join((self.__doc__, *args)))
            super().__init__(self.__doc__)
        else:
            super().__init__(*args)



class InvalidHostEntry(Base):
    """IP address or domain name is not given or in incorrect format."""

class InvalidIPAdrees(Base):
    """IP address is not in correct format."""


class InvalidDomain(Base):
    """Domain name is not in correct foramt"""

