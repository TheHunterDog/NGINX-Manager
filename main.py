import sys
import os
from shutil import copyfile,move
import yaml
from getpass import getuser
import requests

todolist = []

def init():
  dictFile = {"path" : None}
  print("Do you know where NGINX is installed?")
  print('y = yes')
  print("n = no")
  invalid = True
  while(invalid):
    choiceInit = input("Shall we do it now? ")
    if isinstance(choiceInit, str):
      if(choiceInit.find("y") >= 0):
        invalid = False
        path = input("Tell us where: ")
      elif(choiceInit.find("n") >= 0):
        invalid = False
        print("The minions are looking for NGINX")
        path = autodetect()
  if(isinstance(path,bool)):
    print("we were unsuccessful to locate NGINX")
  print(path)
  dictFile['path'] = path
  try:
    with open('NMConfig.yaml','w') as file:
      yaml.dump(dictFile,file)
  except Exception as e:
    print("An error has occurd %s" % e)
  return path

def autodetect():
  usualPlaces = [ "/usr/local/nginx/conf", "/etc/nginx", "/usr/local/etc/nginx"]
  for place in usualPlaces:
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
      with open('NMConfig.yaml') as file:
        document = yaml.load(file,Loader=yaml.FullLoader)
        path = document['path']
    except FileNotFoundError:
        print("You havent Initialised yet")
        print('y = yes')
        print("n = no")
        invalid = True
        while(invalid):
            choiceInit = input("Shall we do it now? ")
            if isinstance(choiceInit, str):
                if(choiceInit.find("y") >= 0):
                    invalid = False
                    path = init()
                elif(choiceInit.find("n") >= 0):
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
    print("ExceptBytes - Nginx Manager")
    return True

def getDisabledSites():
    enabled = getEnabledSites()
    Available = getAvailableSites()
    diff = set(Available) - set(enabled)
    return diff

def getAvailableSites():
  configLocation = get_Config_location()
  return os.listdir("%s/sites-available" % configLocation)

def getEnabledSites():
  configLocation = get_Config_location()
  return os.listdir("%s/sites-enabled" % configLocation)

def manage():
  # AvailableSites = getAvailableSites()
  # print(AvailableSites)
  print("Current enabled sites \n")
  enabledSites = getEnabledSites()
  print(enabledSites)
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
  

def createNewSite(**kwargs):
    logFiles = []
    print("createNewSite")
    configLocation = get_Config_location()
    subDirs = ['sites-available','sites-enabled']
    fileName = kwargs.get("fileName", "")
    url = kwargs.get("url", "")
    logsPath = ""
    root = kwargs.get("root", "")
    while fileName == "":
      fileName = input("What do you want to call the file?")
    while url == "":
      url = input("What will be the url?")
    while root == "":
      root = input("What is the root Path?")
    portNumber = input("What portNumber? (leave empty for default)")
    portNumber = 80 if portNumber == "" else portNumber
    while logsPath == "":
      logsPath = input("Where do you want to store the logs? (leave empty for default)")
      logsPath = "/Users/%s/Logs" % (getuser()) if logsPath == "" else logsPath
    with open('template/newSiteTemplate','r') as inputfile:
      with open('temp/%s' % fileName,'w') as output:
        for line in inputfile:
          line = line.replace('PORT',str(portNumber))
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
      choiceInit = input("we are now going to copy would you like to make any changes? ")
      if isinstance(choiceInit, str):
        if(choiceInit.find("y") >= 0):
          print("the file is located at %s/temp answer with n if you are done" % (os.getcwd()))
        elif(choiceInit.find("n") >= 0):
          invalid = False
          print("Then I shall move the file")
    for path in subDirs:
      print(path)
      copyfile('temp/%s'%(fileName),'%s/%s/%s' %(configLocation, path, fileName) )
    os.remove('temp/%s' % fileName)
    try:
      for logFile in logFiles:
        print(logFile)
        with open('%s' % (logFile),'w') as output:
          pass
      todolist.append("You need to add 127.0.0.1 %s to your /etc/hosts file as root" % (url))
    except FileNotFoundError:
      print("Error while creating the log file's");
      return False
    return True


def Menu(menu,printOptions=True):
    # global mainMenu
    if(printOptions):
      for name, data in menu.items():
        print("%s : %s " % (name, data["name"]))
    choice = input("What do you want to do? ")
    isNum = True
    while(isNum):
        try:
            choice = int(choice)
            isNum = isinstance(choice, int) == False
            while int(choice) > len(menu) or int(choice) <= 0:
                print(choice)
                choice = input("Enter a number within the limits")
        except ValueError:
            choice = input("Enter a number ")
            isNum = True
    del isNum
    return choice



def verifyInstallation():
  print("Verifying installation")
  if(os.path.isfile("template/newSiteTemplate")):
    print("Template: OK")
  else:
    print("Template: Failed")
    if(len(os.listdir("template")) == 0):
      print("No templates found")
      print('y = yes')
      print("n = no")
      invalid = True
      while(invalid):
        choiceInit = input("Do you want to download a default template? ")
        if isinstance(choiceInit, str):
          if(choiceInit.find("y") >= 0):
            invalid = False
            print("Downloading from our website?")
            r = requests.get("https://exceptbytes.com/NginxManager/Templates/default/newSiteTemplate")
            open("template/newSiteTemplate",'wb').write(r.content);
          elif(choiceInit.find("n") >= 0):
            invalid = False
    else:
      print("Other templates found")

def download():
  r = requests.get("https://exceptbytes.com/NginxManager/Templates/default/newSiteTemplate")
  open("template/newSiteTemplate",'wb').write(r.content);

def settings():
  mn={}
  mnList= []
  with open('NMConfig.yaml','r') as file:
    document = yaml.full_load(file)
    i = 0
    for item,doc in document.items():
      i+=1
      mn[item] = doc
      print("%s : %s = %s" % (i,item,doc))
    mn[len(mn) + 1] = "exit"
    print("%s : %s" % (len(mn),"exit"))
    mnList = list(mn)
    try:
      choice = Menu(mn,False)
      if(choice != len(mn)):
        mn[mnList[choice-1]] = input("What should %s be?" % (mnList[choice-1]))
        SaveSettings(mn)
        file.close()
      else:
        file.close()
        return True
    except KeyboardInterrupt:
      file.close()
      shutdown()
  return True

def SaveSettings(dict):
  with open('NMConfig.yaml','w') as file:
    doc = yaml.dump(dict,file)


def Main():
  verifyInstallation()
  mainMenu = {
      1: {'name': "Create New Site", 'action': createNewSite},
      2: {'name': "Initialise the manager", 'action': init},
      3: {'name': "Manage websites","action":manage},
      4: {'name': "Check for inconsistencies" , 'action':takeAlook},
      5: {'name': "Download default template" , 'action':download},
      6: {'name': "Settings","action":settings}
      }
  mainMenu = {**mainMenu}

  mainMenu[len(mainMenu) + 1] = {'name': "Exit", 'action': shutdown}
  sortedMenu = {k: v for k, v in sorted(mainMenu.items(), key=lambda item: item[0])}
  try:
    while True:
      printLogo()
      if(len(todolist) != 0):
          print("todo's:")
          for todo in todolist:
            print(todo)
      else:
        print("There are no todo's")
      menuChoice = Menu(sortedMenu)
      res = mainMenu[menuChoice]['action']()
      if(isinstance(res,bool)):
        if(res):
          print("Succes")
        else:
          print("Something has gone wrong")
      else:
        print("%s" % (res))
  except KeyboardInterrupt:
    shutdown()
Main()