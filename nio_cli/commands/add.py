"""The add command."""


from .base import Base


class Add(Base):
    """ Get basic nio info """

    def run(self):
        print("You're using nio: add")
