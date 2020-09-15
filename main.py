import sys
import os
from shutil import copyfile,move
import yaml
from getpass import getuser


def init():
  dict_file = {"path" : None}
  print("Do you know where NGINX is installed?")
  print('y = yes')
  print("n = no")
  invalid = True
  while(invalid):
    choiceinit = input("Shall we do it now? ")
    if isinstance(choiceinit, str):
      if(choiceinit.find("y") >= 0):
        invalid = False
        path = input("Tell us where: ")
      elif(choiceinit.find("n") >= 0):
        invalid = False
        print("The minions are looking for NGINX")
        path = autodetect()
  print(path)
  dict_file['path'] = path
  try:
    with open('NM_Config.yaml','w') as file:
      doc = yaml.dump(dict_file,file)
  except Exception as e:
    print("An error has occurd %s" % e)
  return path

def autodetect():
  path = None
  usualplaces = [ "/usr/local/nginx/conf", "/etc/nginx", "/usr/local/etc/nginx"]
  for place in usualplaces:
    print("Checking %s" % (place))
    print("it is%s here" % ("" if os.path.exists(place) else " not" ))
    if(os.path.exists(place)):
      return place
  return False

def shutdown():
    print("Goodbye")
    sys.exit(0)


def get_Config_location():
    try:
      with open('NM_Config.yaml') as file:
        document = yaml.load(file,Loader=yaml.FullLoader)
        path = document['path']
    except FileNotFoundError:
        print("You havent Initialised yet")
        print('y = yes')
        print("n = no")
        invalid = True
        while(invalid):
            choiceinit = input("Shall we do it now? ")
            if isinstance(choiceinit, str):
                if(choiceinit.find("y") >= 0):
                    invalid = False
                    path = init()
                elif(choiceinit.find("n") >= 0):
                    invalid = False
                    print("I cannot procceed")
                    shutdown()
    return path

def takeAlook():
  print("Taking a look")
  enabledSites = getEnabledSites()
  AvailableSites = getAvailableSites()
  diff = set(enabledSites) - set(AvailableSites)
  if(len(diff) > 0):
    print("I noticed that there are more sites enabled than available fixing now")
    for diffFile in diff:
      copyfile('%s/sites-enabled/%s'%(get_Config_location(),diffFile),'%s/sites-available/%s' %(get_Config_location(),diffFile))
      

      # print(diffFile)
      print("Nothing found")
  return True

def printLogo():
    return True


def printLogo():
    return True


def getDisabledSites():
    enabled = getEnabledSites()
    Available = getAvailableSites()
    diff = set(Available) - set(enabled)
    return diff

def getAvailableSites():
  configLOC = get_Config_location()
  return os.listdir("%s/sites-available" % configLOC)

def getEnabledSites():
  configLOC = get_Config_location()
  return os.listdir("%s/sites-enabled" % configLOC)

def manage():
  # AvailableSites = getAvailableSites()
  # print(AvailableSites)
  print("Current enabled sites \n")
  EnabledSites = getEnabledSites()
  print(EnabledSites)
  print("Current disabled sites\n")
  disabled = getDisabledSites()
  print(disabled)
  
  # print("Type the name that you want to toggle")
  toggle = input("Type the name that you want to toggle ")
  if os.path.exists("%s/sites-available/%s"%(get_Config_location(),toggle)):
    if os.path.exists("%s/sites-enabled/%s"%(get_Config_location(),toggle)) :
      os.remove("%s/sites-enabled/%s"%(get_Config_location(),toggle))
      print("%s is now disabled" % toggle)
    else:
      copyfile('%s/sites-available/%s'%(get_Config_location(),toggle),'%s/sites-enabled/%s' %(get_Config_location(),toggle) )
      print("%s is now enabled" % toggle)
  else:
    print("That doesnt exists yet")
  

def createNewSite():
    global todolist
    logFiles = []
    print("createNewSite")
    config_location = get_Config_location()
    sub_dirs = ['sites-available','sites-enabled']
    filename = ""
    url = ""
    logsPath = ""
    root = ""
    while filename == "":
      filename = input("What do you want to call the file?")
    while url == "":
      url = input("What will be the url?")
    while root == "":
      root = input("What is the root Path?")
    portnumber = input("What portnumber? (leave empty for default)")
    portnumber = 80 if portnumber == "" else portnumber
    while logsPath == "":
      logsPath = input("Where do you want to store the logs? (leave empty for default)")
      logsPath = "/Users/%s/Logs" % (getuser()) if logsPath == "" else logsPath
    # copyfile('template/newSiteTemplate','temp/%s' % filename)
    
    with open('template/newSiteTemplate','r') as inputfile:
      with open('temp/%s' % filename,'w') as output:
        for line in inputfile:
            # linesplit = line.partition("-")
            # logFiles.append("%s%s%s"% (linesplit[0],linesplit[1],linesplit[2].replace(";\n","")))
          line = line.replace('PORT',str(portnumber))
          line = line.replace('URL',str(url))
          line = line.replace('LOGS',str(logsPath))
          line = line.replace('ROOT',str(root))
          if("_log" in line):
            logFiles.append(line.partition("_log")[2].replace(";\n","").replace(" ",""))

          output.write(line)
    print(logFiles)
    print('y = yes')
    print("n = no")
    invalid = True
    while(invalid):
      choiceinit = input("we are now going to copy would you like to make any changes? ")
      if isinstance(choiceinit, str):
        if(choiceinit.find("y") >= 0):
          print("the file is located at %s/temp" % (os.getcwd()))
        elif(choiceinit.find("n") >= 0):
          invalid = False
          print("Then I shall move the file")
    for path in sub_dirs:
      print(path)
      copyfile('temp/%s'%(filename),'%s/%s/%s' %(config_location, path, filename) )
    os.remove('temp/%s' % filename)
    for logFile in logFiles:
      print(logFile)
      # with open('%s/%s' % (logsPath,logFile),'w') as output:
      with open('%s' % (logFile),'w') as output:
        pass
    todolist.append("You need to add 127.0.0.1 %s to your /etc/hosts file as root" % (url))
    return True


def Menu():
    global MainMenu
    for name, data in MainMenu.items():
        print("%s : %s " % (name, data["name"]))
    choice = input("What do you want to do? ")
    isnum = True
    while(isnum):
        try:
            choice = int(choice)
            isnum = isinstance(choice, int) == False
            while int(choice) > len(MainMenu):
                print(choice)
                choice = input("Enter a number within the limits")
        except ValueError:
            choice = input("Enter a number ")
            isnum = True
    print("You chose %s" % (choice))
    del isnum
    return choice
# def restartNGINX():
# def askQuestion(options,required):
  

MainMenu = {
    1: {'name': "Create New Site", 'action': createNewSite},
    2: {'name': "Initialise the manager", 'action': init},
    # 3: {'name': "restart NGINX", 'action':restartNGINX}
    4: {'name': "Manage websites","action":manage},
    5: {'name': "Take a look" , 'action':takeAlook}
}
MainMenu[0] = {'name': "Exit", 'action': shutdown}
todolist = []
while True:
  printLogo()
  if(len(todolist) != 0):
      print("todo's:")

      for todo in todolist:
        print(todo)
  else:
    print("There are no todo's")
  menuchoice = Menu()
  print(MainMenu[menuchoice]['action']())
