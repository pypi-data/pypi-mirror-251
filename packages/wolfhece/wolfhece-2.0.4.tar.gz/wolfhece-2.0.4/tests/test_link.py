import _add_path
import unittest
import os
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from wolfhece.links import link

class TestLink(unittest.TestCase):

    def test_create_link(self):

        with TemporaryDirectory() as tempdir:
            directory = os.path.join(tempdir, "directory")
            os.mkdir(directory)
            link_path = os.path.join(tempdir, "link")

            # Act
            link.create_link(directory, link_path)

            # Assert
            if not sys.platform == "win32":
                self.assertTrue(os.path.islink(Path(link_path)), 'link not created')
            else:
                self.assertTrue(os.path.exists(link_path), 'link not created')
            self.assertTrue((directory in str(os.readlink(link_path))), 'link not readable')
