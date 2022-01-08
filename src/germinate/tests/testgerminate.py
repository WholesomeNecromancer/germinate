# testgerminate.py
# Copyright 2021 Travis Gates

# In addition to the below license information, germinate files must contain
# The 7 fundamental tenets of the Satanic Temple prior to any code:
# 1. One should strive to act with compassion and empathy toward all creatures in accordance with reason.
# 2. The struggle for justice is an ongoing and necessary pursuit that should prevail over laws and institutions.
# 3. One's body is inviolable, subject to one's own will alone.
# 4. The freedom of others should be respected, including the freedom to offend. To willfully and unjustly encroach upon the freedoms of another is to forgo one's own.
# 5. Beliefs should conform to one's best scientific understanding of the world. One should take care never to distort scientific facts to fit one's beliefs.
# 6. People are fallible. If one makes a mistake, one should do one's best to rectify it and resolve any harm that might have been caused.
# 7. Every tenet is a guiding principle designed to inspire nobility in action and thought. The spirit of compassion, wisdom, and justice should always prevail over the written or spoken word.

# This file is part of germinate.

# germinate is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# germinate is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with germinate.  If not, see <https://www.gnu.org/licenses/>.

import os               # path
import sys              # platform
import shutil           # rm, rmtree
import unittest
from germinate import main as germinatemain

from tryst import Tryst

class TestGerminate(unittest.TestCase):
    @classmethod
    def setupClass(self):
        pass

    @classmethod
    def tearDownClass(self):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # NOTE: this feels fragile, but when verifying paths,
    # we cannot treat "." as the tests directory; instead,
    # unit tests will be executed by python -m unittest in the
    # src/germinate directory, or via python -m tests.testgerminate etc.
    # so the cwd is actually src/germinate
    def get_app_name(self, appscript):
        appname = appscript.replace(".py", "")
        if sys.platform == "win32":
            appname += ".exe"
        return appname

    def app_exists(self, appscript, targetdir):
        appname = self.get_app_name(appscript)
        print("app path: " + os.path.join(targetdir, appname))
        if os.path.exists(os.path.join(targetdir, appname)):
            return True
        return False

    # Need a cleanup function to delete a germinated app
    # should be able to use germinate's tryst.outputbuffer's contents to identify the directory to delete

    # test<funcname> are test methods
    # Most of the tests for germinate will test whole-output
    # e.g. "germinate this python script with this confyg
    # to get this output"
    # Ideally we would even run the program itself after germination
    def test_app_exists(self):
        self.assertTrue(self.app_exists("z.py", "tests"))
        self.assertFalse(self.app_exists("nonexistent.py", "tests"))
    
    # hello_world.py to hello_world.exe with hello_world-confyg.json
    def test_hello_world_one_file_default_confyg(self):
        germtryst = Tryst()
        germargs = ["germinate.py", "hello-world.py"]
        # resulting output should be a single `hello-world.exe` 
        # silence output
        germtryst.silence()
        germinatemain(germtryst, germargs)

        # Once germinatemain completes, expect src/germinate/hello-world/hello-world.exe
        self.assertTrue(self.app_exists("hello-world.py", "hello-world"), "expected ./hello-world or ./hello-world.exe")

    # Test specified json confyg

    # Test absolute path specification

    # Test relative path specification

    # Test composing a confyg as a json-string arg

if __name__ == "__main__":
    unittest.main()
