#!/usr/bin/python

# Simple script to generate a .codeintel/config file for a buildout directory.
# The buildout must use collective.recipe.omelette to generate a parts/omelette
# directory. This will be used as the Python path

import os.path
import sys

path = "parts/omelette"
buildout = "bin/buildout"
python = sys.executable

if len(sys.argv) > 1:
    path = sys.argv[1]
path = os.path.abspath(path)

if len(sys.argv) > 2:
    python = sys.argv[2]

if not os.path.exists(path):
    print "Cannot find path", path
    sys.exit(1)

if not os.path.exists(python):
    print "Cannot find interpreter", python
    sys.exit(1)

if os.path.exists(buildout):
    hashbang = open(buildout, 'r').readline()
    if hashbang.startswith("#!"):
        hashbang = hashbang[2:]
        python = hashbang.strip()

if not os.path.exists(".codeintel"):
    os.mkdir(".codeintel")

open(os.path.join(".codeintel", "config"), "w").write("""\
{
"Python": {
"python": "%s",
"pythonExtraPaths": [
"%s"
]
}
}
""" % (python, path))
