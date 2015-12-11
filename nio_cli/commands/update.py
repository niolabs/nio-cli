"""The update command."""


from .base import Base


class Update(Base):
    """ Get basic nio info """

    def run(self):
        print("You're using nio: update")
