import shutil
import os
from main import Menu


def testing():
    return True


def menuItem():
    return {'name': "CacheManager", 'action': submenu}


def submenu():
    menu = {
        1: {'name': "Empty mods cache", 'action': emptymods},
        2: {'name': "Empty main cache", 'action': emptymain},
        # 3: {'name': "Empty temp folder", 'action': temp},
        4: {'name': "Empty all cache", 'action':  emptyall}
    }
    menuchoice = Menu(menu)
    print(menu[menuchoice]['action']())
    return True


        
def emptymain():
    try:
        while(os.path.exists("../__pycache__")):
            shutil.rmtree('../__pycache__')
            print("The cache is gone")
        return True
    except(OSError):
        print("There was an system error")


def emptymods():
    try:
        while(os.path.exists("__pycache__")):
            shutil.rmtree('__pycache__')
            print("The cache is gone")
        return True
    except(OSError):
        print("There was an system error")
        
def emptyall():
  emptymain()
  emptymods()
