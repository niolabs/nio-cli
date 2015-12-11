"""The new command."""


from .base import Base


class New(Base):
    """ Get basic nio info """

    def run(self):
        print("You're using nio: new")
