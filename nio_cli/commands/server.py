"""The server command."""


from .base import Base


class Server(Base):
    """ Get basic nio info """

    def run(self):
        print("You're using nio: server")
