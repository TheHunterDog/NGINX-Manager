from main import Menu, get_Config_location,createNewSite
import os
def menuItem():
  return {'name': "WebManager", 'action': submenu}
def submenu():
  menu = {
    1: {'name': "Initialise WebManger", 'action': init},
    2: {'name': "Open WebManager", 'action': openM}
  }
  menuchoice = Menu(menu)
  print(menu[menuchoice]['action']())
  return True
def init():
  createNewSite(filename="WebManagerConfig",templateloc="%s/webManagerContent/WebManagerConfig" % os.getcwd() ,url="local.webmanager.com",root="%s/webManagerContent/www" % os.getcwd())
def openM():
  return True
def testing():
  return True
