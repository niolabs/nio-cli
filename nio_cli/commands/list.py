"""The list command."""


from .base import Base


class List(Base):
    """ Get basic nio info """

    def run(self):
        print("You're using nio: list")
