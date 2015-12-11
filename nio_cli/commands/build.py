"""The build command."""


from .base import Base


class Build(Base):
    """ Get basic nio info """

    def run(self):
        print("You're using nio: build")
