import platform, subprocess
from . import configmodule
import configparser
from pathlib import Path
from os.path import dirname

def defaultTraceFilePath():
   """
   Outputs the default file path for trace in this library
   """
   match configmodule.platform:
      case "Windows":
         path = fr"{configmodule.librarydirectory}\flashlog.txt"
      case "Linux" | "Darwin":
         path = f"{configmodule.librarydirectory}/flashlog.txt"
   return path

def defaultTraceFilePath_Flash(versionOverride:bool=False,overrideSystem:str=None,overrideVersion:str=None):
   """
   Outputs the defualt file path for trace as defined by https://web.archive.org/web/20180227100916/helpx.adobe.com/flash-player/kb/configure-debugger-version-flash-player.html
   Since anything earlier than Windows 7 isn't supported by python 3, you normally wouldn't be able to get the file path for these systems but I have included an optional parameter to force this function to return it.
   """
   match configmodule.platform:
      case "Linux" | "Darwin":
         from os import getuid
         from pwd import getpwuid
         username = getpwuid(getuid())[0]
      case "Windows":
         from os import getlogin
         username = getlogin()
   if versionOverride == True:
      match overrideSystem:
         case "Linux":
            return fr"/home/{username}/.macromedia/Flash_Player/Logs/flashlog.txt"
         case "Darwin":
            return fr"/Users/{username}/Library/Preferences/Macromedia/Flash Player/Logs/flashlog.txt"
         case "Windows ":
            match overrideVersion:
               case "95" | "98" | "ME" | "XP":
                  return fr"C:\Documents and Settings\{username}\Application Data\Macromedia\Flash Player\Logs\flashlog.txt"
               case "Vista" | "7" | "8" | "8.1" | "10" | "11":
                  return fr"C:\Users\{username}\AppData\Roaming\Macromedia\Flash Player\Logs\flashlog.txt"
   else:
      match configmodule.platform:
         case "Linux":
            return fr"/home/{username}/.macromedia/Flash_Player/Logs/flashlog.txt"
         case "Windows":
            return fr"C:\Users\{username}\AppData\Roaming\Macromedia\Flash Player\Logs\flashlog.txt"
         case "Darwin":
            return fr"/Users/{username}/Library/Preferences/Macromedia/Flash Player/Logs/flashlog.txt"

def sm_x11():
   """
   Gets and returns screen width, screen height, refresh rate, and color depth on x11
   """
   xr = f'{subprocess.check_output("xrandr --current", shell=True)}'.split("\\n")
   for option in xr:
      if option.find("*") != -1:
         curop = option.split(" ")
         break
      else:
         continue
   ops = []
   for i in curop:
      if i == "":
         continue
      else:
         ops.append(i)
   ops.pop(0)
   for i in ops:
      if i.find("*") != -1:
         temprr = i.replace("*","").replace("+","")
         break
      else:
         continue
   cdp = f'{subprocess.check_output("xwininfo -root | grep Depth", shell=True)}'.replace("\\n","").replace("b'","").replace(" ","").replace("'","").split(":")[1]
   tempwidth = f'{subprocess.check_output("xwininfo -root | grep Width", shell=True)}'.replace("\\n","").replace("b'","").replace(" ","").replace("'","").split(":")[1]
   tempheight = f'{subprocess.check_output("xwininfo -root | grep Height", shell=True)}'.replace("\\n","").replace("b'","").replace(" ","").replace("'","").split(":")[1]
   return int(tempwidth),int(tempheight),float(temprr),int(cdp)

def sm_wayland():
   configpath = f"{configmodule.librarydirectory}/wayland.cfg"
   if Path(configpath).exists() == True:
      with open(configpath, 'r') as f:
         configwithheader = f.read()
      config = configparser.ConfigParser()
      config.read_string(configwithheader)
      actual_config = config["Screen"]
      existing_options = ["screenwidth" in actual_config,"screenheight" in actual_config,"refreshrate" in actual_config,"colordepth" in actual_config]
      if existing_options[0] == True:
         sw = int(actual_config["screenwidth"])
      else:
         sw = 1600
      if existing_options[1] == True:
         sh = int(actual_config["screenheight"])
      else:
         sh = 900
      if existing_options[2] == True:
         rr = float(actual_config["refreshrate"])
      else:
         rr = 60.00
      if existing_options[3] == True:
         cd = int(actual_config["colordepth"])
      else:
         cd = 8
   else:
      print("(The things that these answers controls is not implemented yet) This seems to be your first time using the module as3lib. Since you are using wayland, some things could not be automatically detected. Please input them in the fields bellow. This information is a part of the flash display module, if you aren't planning to use that, you can put in whatever you want. This information can be configured later in the file <library directory>/wayland.cfg")
      sw = input("Maximum width (px), or -1 for no limit: ")
      sh = input("Maximum height (px), or -1 for no limit: ")
      rr = input("Refresh rate (Hz): ")
      cd = input("Color depth (bits): ")
      with open(f"{configmodule.librarydirectory}/wayland.cfg", "w") as cfg:
         cfg.write(f"[Screen]\nscreenwidth={int(sw)}\nscreenheight={int(sh)}\nrefreshrate={float(rr)}\ncolordepth={int(cd)}")
   return int(sw), int(sh), float(rr), int(cd)

def sm_windows():
   pass

def sm_darwin():
   pass

def indexOf_String(string:str, find:str):
   try:
      return string.index(find)
   except:
      return -1

def getSeparator():
   match configmodule.platform:
      case "Windows":
         return "\\"
      case "Linux" | "Darwin":
         return "/"

def getUserDir():
   match configmodule.platform:
      case "Windows":
         return f"{subprocess.check_output('echo %HOMEDRIVE%%HOMEPATH%',shell=True)}"[2:-5]
      case "Linux":
         return f"{subprocess.check_output('echo ~',shell=True)}"[2:-3]
      case "Darwin":
         pass

def getDesktopDir():
   match configmodule.platform:
      case "Windows":
         return fr"{configmodule.userdirectory}\Desktop"
      case "Linux" | "Darwin":
         return fr"{configmodule.userdirectory}/Desktop"

def getDocumentsDir():
   match configmodule.platform:
      case "Windows":
         return fr"{configmodule.userdirectory}\Documents"
      case "Linux" | "Darwin":
         return fr"{configmodule.userdirectory}/Documents"

def getdmname():
   return str(subprocess.check_output("loginctl show-session $(loginctl | grep $(whoami) | awk '{print $1}') -p Desktop",shell=True)).split("=")[1].replace("\\n","")[:-1].lower()

def getCPUAddressSize():
   return platform.architecture()[0][:-3]

def getCPUArchitecture():
   #!support other architectures
   match platform.machine():
      case "x86" | "x86_64" | "AMD64":
            return "x86"

def getManufacturer():
   match configmodule.platform:
      case "Windows":
         return "Adobe Windows"
      case "Linux":
         return "Adobe Linux"
      case "Darwin":
         return "Adobe Macintosh"

def getOperatingSystem():
   #!add others
   match configmodule.platform:
      case "Windows":
         pass
      case "Linux":
         return f"Linux {platform.release()}"
      case "Darwin":
         pass

def getVersion():
   tempfv = configmodule.spoofedFlashVersion
   match configmodule.platform:
      case "Windows":
         return f"Win {tempfv[0]},{tempfv[1]},{tempfv[2]},{tempfv[3]}"
      case "Linux":
         return f"LNX {tempfv[0]},{tempfv[1]},{tempfv[2]},{tempfv[3]}"
      case "Darwin":
         return f"MAC {tempfv[0]},{tempfv[1]},{tempfv[2]},{tempfv[3]}"
      case "Android":
         return f"AND {tempfv[0]},{tempfv[1]},{tempfv[2]},{tempfv[3]}"

def dependencyCheck():
   #!Make checks functional and reliable
   match configmodule.platform:
      case "Linux":
         wmt = str(subprocess.check_output("echo $XDG_SESSION_TYPE",shell=True))[2:].replace("\\n'","")
         if wmt == "wayland":
            x=0
         else:
            if str(subprocess.check_output("xwininfo -version",shell=True))[2:10] != "xwininfo":
               raise Exception("xwininfo is required to use as3lib on xorg")
            if str(subprocess.check_output("xrandr --version",shell=True))[2:8] != "xrandr":
               raise Exception("xrandr is required to use as3lib on xorg")
         if str(subprocess.check_output("bash --version",shell=True))[2:10] != "GNU bash":
            raise Exception("bash is required to use as3lib on linux")
         if str(subprocess.check_output("echo test",shell=True))[2:6] != "test":
            raise Exception("echo is required to use as3lib on linux")
         """
         #grep
         if str(subprocess.check_output("",shell=True))[2:\#] != "":
            raise Exception(" is required to use as3lib on linux")
         """
         if str(subprocess.check_output("awk --version",shell=True))[2:9] != "GNU Awk":
            raise Exception("awk is required to use as3lib on linux")
         if str(subprocess.check_output("whoami --version",shell=True))[2:8] != "whoami":
            raise Exception("whoami is required to use as3lib on linux")
         if str(subprocess.check_output("loginctl --version",shell=True))[2:9] != "systemd":
            raise Exception("loginctl (systemd) is required to use as3lib on linux")
      case "Windows":
         pass
      case "Darwin":
         pass
      #<a href="https://pypi.org/project/numpy">numpy</a>
      #<a href="https://pypi.org/project/Pillow">Pillow</a>
      #<a href="https://pypi.org/project/tkhtmlview">tkhtmlview</a>

def initconfig():
   #set up variables needed by mutiple modules
   configmodule.librarydirectory = dirname(__file__)
   configmodule.platform = platform.system()
   dependencyCheck()
   configmodule.separator = getSeparator()
   configmodule.userdirectory = getUserDir()
   configmodule.desktopdirectory = getDesktopDir()
   configmodule.documentsdirectory = getDocumentsDir()
   configmodule.defaultTraceFilePath = defaultTraceFilePath()
   configmodule.defaultTraceFilePath_Flash = defaultTraceFilePath_Flash()
   configmodule.pythonversion = platform.python_version()
   configmodule.cpuAddressSize = getCPUAddressSize()
   configmodule.cpuArchitecture = getCPUArchitecture()
   configmodule.manufacturer = getManufacturer()
   configmodule.os = getOperatingSystem()
   configmodule.version = getVersion()
   match configmodule.platform:
      case "Linux":
         dmtype = str(subprocess.check_output("loginctl show-session $(loginctl | grep $(whoami) | awk '{print $1}') -p Type", shell=True)).split("=")[1].replace("\\n'","")
         configmodule.windowmanagertype = dmtype
         configmodule.dmname = getdmname()
         match configmodule.windowmanagertype:
            case "x11":
               temp = sm_x11()
               configmodule.width = temp[0]
               configmodule.height = temp[1]
               configmodule.refreshrate = temp[2]
               configmodule.colordepth = temp[3]
            case "wayland":
               temp = sm_wayland()
               configmodule.width = temp[0]
               configmodule.height = temp[1]
               configmodule.refreshrate = temp[2]
               configmodule.colordepth = temp[3]
      case "Windows":
         configmodule.initerror.append({"errcode":1,"errdesc":"Error fetching screen properties; Windows; Not Implemented Yet"})
         #configmodule.width = temp[0]
         #configmodule.height = temp[1]
         #configmodule.refreshrate = temp[2]
         #configmodule.colordepth = temp[3]
         pass
      case "Darwin":
         configmodule.initerror.append({"errcode":1,"errdesc":"Error fetching screen properties; Darwin; Not Implemented Yet"})
         #configmodule.width = temp[0]
         #configmodule.height = temp[1]
         #configmodule.refreshrate = temp[2]
         #configmodule.colordepth = temp[3]
         pass
   match configmodule.platform:
      case "Linux" | "Darwin":
         configpath = f"{configmodule.librarydirectory}/mm.cfg"
         if Path(configpath).exists() == True:
            with open(configpath, 'r') as f:
               configwithheader = '[dummy_section]\n' + f.read()
            config = configparser.ConfigParser()
            config.read_string(configwithheader)
            actual_config = config["dummy_section"]
            existing_options = ["ErrorReportingEnable" in actual_config,"MaxWarnings" in actual_config,"TraceOutputFileEnable" in actual_config,"TraceOutputFileName" in actual_config,"ClearLogsOnStartup" in actual_config]
            if existing_options[0] == True:
               configmodule.ErrorReportingEnable = int(actual_config["ErrorReportingEnable"])
            if existing_options[1] == True:
               configmodule.MaxWarnings = int(actual_config["MaxWarnings"])
            if existing_options[2] == True:
               configmodule.TraceOutputFileEnable = int(actual_config["TraceOutputFileEnable"])
            if existing_options[3] == True:
               configmodule.TraceOutputFileName = actual_config["TraceOutputFileName"]
            if existing_options[4] == True:
               configmodule.ClearLogsOnStartup = int(actual_config["ClearLogsOnStartup"])
      case "Windows":
         configpath = fr"{configmodule.librarydirectory}\mm.cfg"
         if Path(configpath).exists() == True:
            with open(configpath, 'r') as f:
               configwithheader = '[dummy_section]\n' + f.read()
            config = configparser.ConfigParser()
            config.read_string(configwithheader)
            actual_config = config["dummy_section"]
            existing_options = ["ErrorReportingEnable" in actual_config,"MaxWarnings" in actual_config,"TraceOutputFileEnable" in actual_config,"TraceOutputFileName" in actual_config,"ClearLogsOnStartup" in actual_config]
            if existing_options[0] == True:
               configmodule.ErrorReportingEnable = int(actual_config["ErrorReportingEnable"])
            if existing_options[1] == True:
               configmodule.MaxWarnings = int(actual_config["MaxWarnings"])
            if existing_options[2] == True:
               configmodule.TraceOutputFileEnable = int(actual_config["TraceOutputFileEnable"])
            if existing_options[3] == True:
               configmodule.TraceOutputFileName = actual_config["TraceOutputFileName"]
            if existing_options[4] == True:
               configmodule.ClearLogsOnStartup = int(actual_config["ClearLogsOnStartup"])
   if configmodule.TraceOutputFileName == "":
      configmodule.TraceOutputFileName = configmodule.defaultTraceFilePath
   if Path(configmodule.TraceOutputFileName).is_dir() == True:
      print("Path provided is a directory, writing to defualt location instead.")
      configmodule.TraceOutputFileName = configmodule.defaultTraceFilePath
   if configmodule.ClearLogsOnStartup == 1:
      if Path(configmodule.TraceOutputFileName).exists() == True:
         with open(configmodule.TraceOutputFileName, "w") as f: 
            f.write("")

   #Tell others that library has been initialized
   configmodule.initdone = True
