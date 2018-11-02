import json, os, re
from collections import defaultdict
from .base import Base


class BuildReadme(Base):

    def run(self):
        print("DEPRECATED: This method is deprecated in favor of the "
              "\"from_readme\" syntax in the spec.json file")
