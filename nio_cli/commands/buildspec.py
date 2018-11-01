from .base import Base


class BuildSpec(Base):

    def run(self):
        print("DEPRECATED: This method is deprecated in favor of the "
              "\"from_python\" syntax in the spec.json file")
