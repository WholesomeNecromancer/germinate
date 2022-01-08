# germinate.py
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

import sys                      # path
import shutil                   # .copy(), .copytree()
import os                       # os.mkdir()
import PyInstaller.__main__

from tryst import Tryst
from tryst import Option
from tryst import JSONHelper

SUMMARY = "germinate freezes Python scripts into executable binaries.\n"
SUMMARY += "Usage: python germinate.py <targetfile>\n"

# Whether to output "info" level logging from PyInstaller or ERROR only
INFO = False

# When given the command germinate somefile.py, germinate will look for a
# somefile-confyg.json in the same directory with its configuration specification
CONFIG_SUFFIX = "-confyg.json"
EXE_EXT = ".exe"

CONFIG_KEYS = [
    "onefile",
    "create-dirs",
    "copy-dirs",
    "copy-files",
    "output-dir",
    "app-name"
]

DEFAULT_CONFIG = {
    "onefile": "false",
    "create-dirs": [],
    "copy-dirs": [],
    "copy-files": [],
    "output-dir": "output",
    "app-name": ""                  # "" indicates no desired override # absence does as well
}

mytryst = None

#--------------------------------------------------------------------------------
# Uses pyinstaller to create a single .exe or a nested dir with .exe
def run_pyinstaller(config):
    pyinstaller_args = []
    _onefile = "--onefile"
    _loglevel = "--log-level"
    _level = ""
    if INFO:
        _level += "INFO"
    else:
        _level += "ERROR"
    mytryst.debug("_loglevel desired is " + _loglevel)

    pyinstaller_args.append(_loglevel)
    pyinstaller_args.append(_level)
    pyinstaller_args.append(str(config["target-file"]))

    if config["onefile"] == "true": 
        pyinstaller_args.append(str(_onefile))
    
    mytryst.debug("pyinstaller_args: " + str(pyinstaller_args))
    for arg in pyinstaller_args:
        mytryst.debug("arg: " + str(arg) + " | type: " + str(type(arg)))

    PyInstaller.__main__.run(pyinstaller_args)
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
def cleanup_pyinstaller(config):
    output_extension = ""               # no extension for bash, etc.
    mytryst.debug("sys.platform = " + str(sys.platform))
    if sys.platform.lower() == "win32":
        output_extension = EXE_EXT      # .exe for PowerShell
    mytryst.debug("cleaning up...")
    # Rather than renaming folders, we should simply cleanup.
    # Copy contents of dist into the specified output-dir; 
    app_name = config["target-file-trimmed"]
    if config.get("app-name") != None:
        config_app_name = config["app-name"]
        if config_app_name != "":
            app_name = config["app-name"]

    dist_root = "dist"
    source_exe_file = config["target-file-trimmed"] + output_extension
    dest_exe_file = app_name + output_extension
    config["dest-exe-file"] = dest_exe_file
    dist_dir = config["target-file-trimmed"]
    output_dir = config.get("output-dir", os.getcwd())
    mytryst.debug("output-dir = " + str(output_dir))
    final_output_dir = os.path.join(output_dir, app_name)
    mytryst.debug("final-output-dir = " + str(final_output_dir))
    config["final-output-dir"] = final_output_dir

    # Check to see if output dir exists; if not, create it
    if not os.path.isdir(output_dir):
        # ./foo-output/
        os.mkdir(output_dir)

    if config["onefile"] == "true":
        if not os.path.isdir(final_output_dir):
            os.mkdir(final_output_dir)
        mytryst.debug("dist_root = " + dist_root)
        mytryst.debug("source_exe_file = " + source_exe_file)
        mytryst.debug("final_output_dir = " + final_output_dir)
        mytryst.debug("dest_exe_file = " + dest_exe_file)
        # Move target_file_trimmed + output_extension into output-dir
        shutil.copyfile(os.path.join(dist_root, source_exe_file), os.path.join(final_output_dir, dest_exe_file))
    else:
        if os.path.isdir(os.path.join(output_dir, dist_dir)):
            shutil.rmtree(os.path.join(output_dir, dist_dir))
        # Move the folder target_file_trimmed into output-dir
        shutil.copytree(os.path.join(dist_root, dist_dir), os.path.join(output_dir, dist_dir))
    
    mytryst.debug("removing build/ & dist/...")
    # Remove PyInstaller's build/ & dist/ working directories
    shutil.rmtree("build")
    shutil.rmtree("dist")
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
def create_dirs(config):
    destdir = config["final-output-dir"]
    # mkdir copy_destination/target-file/foo/
    for create_dir in config["create-dirs"]:
        new_dir = os.path.join(destdir, create_dir)
        mytryst.debug("making dir... " + str(new_dir))
        os.mkdir(new_dir)
#----------------------------------------

#----------------------------------------
def copy_dirs(config):
    destdir = config["final-output-dir"]
    # Copy foo/ from . to copy_destination/target-file/foo/
    for copy_dir in config["copy-dirs"]:
        dir_to_copy = os.path.join(config["target-dir"], copy_dir)
        output_dir = os.path.join(destdir, copy_dir)
        mytryst.debug("copying to dir... " + str(output_dir))
        destination = shutil.copytree(dir_to_copy, output_dir)
#----------------------------------------

#----------------------------------------
def copy_files(config):
    destdir = config["final-output-dir"]
    for copy_file in config["copy-files"]:
        file_to_copy = os.path.join(config["target-dir"], copy_file)
        output_file = os.path.join(destdir, copy_file)
        mytryst.debug("copying to... " + str(output_file))
        destination = shutil.copyfile(file_to_copy, output_file)
#----------------------------------------

#----------------------------------------
def handle_confyg_optarg(userconfyg):
    config = {}
    if userconfyg.endswith(".json"):
        config = JSONHelper.load(userconfyg)
    else:
        # Assume userconfyg (the value given with -c=, --confyg=) is a JSON string containing confyg data
        config = JSONHelper.fromstring(userconfyg)
    return config
#----------------------------------------

#--------------------------------------------------------------------------------
def main(sometryst=Tryst(), inputs=None):
    global INFO                             # TODO: handle this better; expose --log-level here in germinate
    global mytryst
    mytryst = sometryst

    appname = "germinate"
    authors = "wholesomenecromancer"
    version = "0.0.1"

    mytryst.initialize(appname, authors, SUMMARY, version)

    info_option = Option("info", "Set PyInstaller's --log-level to INFO; ERROR is default.", "i")

    confyg_optarg = Option("confyg", "Override default *-confyg.json file with a specified confyg file.", "c")
    output_optarg = Option("output-dir", "Output to specified directory.", "o")
    # TODO: add option to accept confyg as a string json arg; maybe confyg changes to --confyg-file, -f?
    # leaving --confyg,-c to be a json string arg?
    # this would make chaining and testing easier
    # TODO: add Option to archive output to a .zip, ./appname.zip; we have code to archive in deploy.py

    mytryst.add_option(info_option)

    mytryst.add_option_argument(confyg_optarg)
    mytryst.add_option_argument(output_optarg)

    mytryst.consort(inputs)

    target_file = ""
    confyg_file = ""

    # Looking for exactly 1 userarg: the script to germinate
    if len(mytryst.userargs) != 1:
        mytryst.show_usage()
        mytryst.quit()

    if info_option in mytryst.useroptions:
        INFO = True

    userconfyg = mytryst.useroptionarguments.get(confyg_optarg)
    useroutput = mytryst.useroptionarguments.get(output_optarg)

    # Suppose it's possible to germinate multiple things but let's not
    for uarg in mytryst.userargs:
        target_file = str(uarg)
        if not target_file.endswith(".py"):
            mytryst.error("Only *.py files can be germinated.")
            mytryst.quit()

        target_file = target_file.replace(".py", "")
        if not userconfyg:
            confygcandidate = target_file + CONFIG_SUFFIX
        else:
            confygcandidate = userconfyg

        config = handle_confyg_optarg(confygcandidate)
        if not config:
            mytryst.debug("Failed to load JSON based on " + confygcandidate)
            mytryst.show_usage()
            mytryst.quit()

        mytryst.debug("loaded confyg:\n" + str(config))

        # With configuration, we can now:
        # 1. Run PyInstaller with the specified arguments
        # 2. Rename workpath and distpath based on configuration
        # 3. Create any requested directories
        # 4. Copy any requested directories
        # 5. Copy any requested files
        # ... Complete!
        config["target-file"] = os.path.normpath(uarg)
        config["target-file-trimmed"] = os.path.normpath(uarg.replace(".py", ""))
        config["target-dir"] = os.path.split(uarg)[0]
        mytryst.debug("config[target-file] = " + config["target-file"])
        mytryst.debug("config[target-file-trimmed] = " + config["target-file-trimmed"])
        mytryst.debug("config[target-dir] = " + config["target-dir"])

        if useroutput:
            config["output-dir"] = useroutput

        mytryst.debug("\n... running PyInstaller...")
        run_pyinstaller(config)

        mytryst.debug("\n... Complete! Cleaning up PyInstaller...")
        cleanup_pyinstaller(config)

        mytryst.debug("\n... Complete! Creating directories...")
        create_dirs(config)

        mytryst.debug("\n... Complete! Copying directories...")
        copy_dirs(config)

        mytryst.debug("\n... Complete! Copying files...")
        copy_files(config)

        mytryst.output(os.path.join(config["final-output-dir"], config["dest-exe-file"]))

        mytryst.write_stdout()
        mytryst.write_stderr()
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
#--------------------------------------------------------------------------------
