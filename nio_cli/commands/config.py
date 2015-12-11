"""The config command."""


from .base import Base


class Config(Base):
    """ Get basic nio info """

    def run(self):
        print("You're using nio: config")
