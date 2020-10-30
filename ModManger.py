from os.path import dirname, basename, isfile, join
from os import listdir
import glob
import importlib

from os import walk

f = []
mods = []
def importMods(size):
  menuItems = {}
  modules = glob.glob(join("%s/mods" % (dirname(__file__)), "*.py"))
  __all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
  for mod in __all__:
    try:
      print ("Importing %s" % mod)
      imported = importlib.import_module("mods.%s" % mod,'.')
      # print(imported)
      size = ++size
      menuItems[size + len(menuItems)] = imported.menuItem()
      if imported.testing() is not True :
        print("Error %s has failed to import" % mod)
    except Exception as e:
      print("There was an error while importing %s" % mod)
      print(e)
  # print(__all__)
  # print(menuItems)
  return menuItems