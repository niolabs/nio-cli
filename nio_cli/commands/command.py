"""The command command."""

from .base import Base


class Command(Base):
    """ Get basic nio info """

    def run(self):
        print("You're using nio: command")
