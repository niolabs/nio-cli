import subprocess, re

from .base import Base
import os


class NewBlock(Base):

    def __init__(self, options, *args, **kwargs):
        super().__init__(options, *args, **kwargs)
        self._block = self.options['<block-name>']

    def run(self):
        clone = (
            "git clone git://github.com/{}/{}.git {}"
        ).format('nio-blocks', 'block_template', self._block)
        subprocess.call(clone, shell=True)

        # rename block file
        block_parent_path = os.path.abspath(".")
        block_root_path = os.path.join(block_parent_path, self._block)
        os.chdir(block_root_path)
        os.rename(os.path.join(block_root_path, "example_block.py"),
                  os.path.join(block_root_path,
                               "{0}_block.py".format(self._block)))

        # rename readme
        os.remove(os.path.join(block_root_path, "README.md"))
        os.rename(os.path.join(block_root_path, "BLOCK_README.md"),
                  os.path.join(block_root_path, "README.md"))

        # rename test file
        block_tests_path = os.path.join(block_root_path, "tests")
        os.chdir(block_tests_path)
        os.rename(os.path.join(block_tests_path, "test_example_block.py"),
                  os.path.join(block_tests_path,
                               "test_{0}_block.py".format(self._block)))

        # subsequent calls assume being on block's parent folder
        os.chdir(block_parent_path)
        self.rename_block_class(self._block)
        self.rename_test_class(self._block)
        self.rename_test_imports(self._block)

        reinit_repo = (
            'cd ./{} '
            '&& git remote remove origin '
            '&& git add -A'
            '&& git commit --amend --reset-author -m "Initial commit"'
        ).format(self._block)
        subprocess.call(reinit_repo, shell=True)

    def rename_block_class(self, block):
        camel_block_name = self.camelize_block_name(block)

        with open('./{0}/{0}_block.py'.format(block)) as f:
            file_string = f.read()
        file_string = re.sub('Example', camel_block_name, file_string)

        with open('./{0}/{0}_block.py'.format(block), 'w') as f:
            f.write(file_string)

    def rename_test_class(self, block):
        camel_block_name = 'Test' + self.camelize_block_name(block)

        with open('./{0}/tests/test_{0}_block.py'.format(block)) as f:
            file_string = f.read()
        file_string = re.sub('TestExample', camel_block_name, file_string)

        with open('./{0}/tests/test_{0}_block.py'.format(block), 'w') as f:
            f.write(file_string)

    def rename_test_imports(self, block):
        camel_block_name = self.camelize_block_name(block)

        with open('./{0}/tests/test_{0}_block.py'.format(block)) as f:
            file_string = f.read()
        file_string = re.sub('Example', camel_block_name, file_string)
        file_string = re.sub(
            '..example_block', '..{}_block'.format(block), file_string)

        with open('./{0}/tests/test_{0}_block.py'.format(block), 'w') as f:
            f.write(file_string)

    @staticmethod
    def camelize_block_name(block):
        camel_block_name = block
        if '_' in block:
            camel_block_name = ''
            camel_block_array = block.split('_')
            for word in camel_block_array:
                capitalized = word.title()
                camel_block_name += capitalized
        else:
            camel_block_name = camel_block_name.title()
        return camel_block_name
