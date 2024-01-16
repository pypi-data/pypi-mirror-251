import as3lib.toplevel as as3
from as3lib import configmodule as confmod
from typing import Union
from as3lib.flash.events import Event
from tkinter import filedialog
import as3lib.flash.utils as utils

class FileFilter:
   def __init__(self,description:Union[str,as3.String],extension:Union[str,as3.String],macType:Union[str,as3.String]=None):
      self.description = description
      self.extension = extension
      self.macType = macType
   def extensionsToArray(self):
      return as3.listtoarray(self.extension.split(";"))
   def macTypeToArray(self):
      if self.macType != None:
         return as3.listtoarray(self.macType.split(";"))
   def toTkTuple(self):
      return (self.description,self.extension.split(";"))
class FileReference:
   def __init__(self):
      self.__listeners = as3.Array() #Array of Arrays; each Array consists of the event to listen for and the object to call
      #self.creationDate
      #self.creator
      #self.data
      #self.extension
      #self.modificationDate
      #self.name
      #self.permissionStatus
      #self.size
      #self.type
      self._location = None
      pass
   def execEvent(self,event):
      for i in self.__listeners:
         if i[0] == event:
            i[1]() #needs to have some sort of event object as a function parameter
   def addEventListener(self,event,function:callable):
      self.__listeners.push(as3.Array(event,function))
   def browse(self,typeFilter:Union[as3.Array,list,tuple]=None):
      #typeFilter is an Array/list/tuple of FileFilter objects
      if typeFilter != None:
         filetypes = []
         for i in typeFilter:
            filetypes.append(i.toTkTuple())
         filename = filedialog.askopenfilename(title="Select a file to upload",filetypes=filetypes)
      else:
         filename = filedialog.askopenfilename(title="Select a file to upload")
      try:
         return True
      except:
         print("You somhow messed it up")
      finally:
         if filename in (None,()):
            self.execEvent(Event.CANCEL)
         else:
            self.execEvent(Event.SELECT)
   def cancel(self):
      pass
   def dowload(self,request,defaultFileName=None):
      pass
   def load(self):
      pass
   def requestPermission(self):
      pass
   def save(self,data,defaultFileName=None):
      #!add check for blacklisted characters  / \ : * ? " < > | %
      file = defaultFileName.split(".")
      savetype = 0 # 1=UTF-8 2=XML 3=ByteArray
      if data == None:
         as3.ArguementError("Invalid Data")
         return False
      elif type(data) in (str,as3.String):
         #write a UTF-8 text file
         savetype = 1
      #elif type(data) == #XML:
         #Write as xml format text file with format preserved
         #savetype = 2
      elif type(data) == utils.ByteArray:
         #write data to file as is (in byte form)
         savetype = 3
      else:
         #convert to string and save as text file. If it fails throw ArguementError
         try:
            data = str(data)
         except:
            as3.ArguementError("Invalid Data")
            return False
      if len(file) == 1:
         #no extension
         filename = filedialog.asksaveasfilename(title="Select location for download")
      else:
         #extension
         #!doesn't seen to work
         ext = f".{file[-1]}"
         filename = filedialog.asksaveasfilename(title="Select location for download",defaultextension=ext)
      try:
         return True
      except:
         print("You somhow messed it up")
      finally:
         if filename in (None,()):
            self.execEvent(Event.CANCEL)
         else:
            self.execEvent(Event.SELECT)
            self._location = filename
            self.execEvent(Event.COMPLETE)
   def upload(self,request,uploadDataFieldName,testUpload=False):
      pass
   def uploadUnencoded(self,request):
      pass

class InterfaceAddress:
   #address = classmethod()
   #broadcast = classmethod()
   def __getAddrType():
      pass
   #ipVersion = classmethod(fget=__AddrType)
   #prefixLength = classmethod()

class IPVersion:
   IPV4 = "IPv4"
   IPV6 = "IPv6"


class ObjectEncoding:
   AMF0 = 0
   AMF3 = 3
   DEFAULT = 3

class sodata:
   def __init__(self):
      return None
   def __str__(self):
      return f"{vars(self)}"
   def __repr__(self):
      return f"{vars(self)}"
   def toDict(self):
      return dict(vars(self))

class SharedObject:
   def __init__(self):
      self._name = ""
      self._path = ""
      self.data = sodata()
   def clear(self):
      #self._name = ""
      #self._path = ""
      self.data = sodata()
   def close(self):
      pass
   def connect(self):
      pass
   def flush(slef,minDiskSpace=0):
      pass
   def getLocal(self,name,localPath=None,secure=False):
      #gets local shared object; if object exists, set path and load it. if not, just set path
      #!fix separators and make paths "Path" objects
      parent = ""
      directory = f"{confmod.separator}"
      #localPath is the path (without the file name) with the application specific data directory as root
      #   application data directory is configmodule.appdatadirectory and needs to be set manually using toplevel.setDataDirectory(directory)
      #   (implementation specific addition) if the application data directory is not specified, the library directory is used as a default
      #name is the name of the file excluding the extension because it will always be .sol
      if localPath != None:
         directory = localPath
      if confmod.appdatadirectory == None:
         #use confmod.librarydirectory
         parent = confmod.librarydirectory
      else:
         #use confmod.appdatadirectory
         parent = confmod.appdatadirectory
      if parent[-1] == confmod.separator:
         parent = parent[:-1]
      if directory[0] == confmod.separator:
         directory = directory[1:]
      if directory[-1] == confmod.separator:
         directory = directory[:-1]
      self._path = f"{parent}{confmod.separator}{directory}{confmod.separator}{name}.sol"
      self._name = name
      pass
   def getRemote(self,name,remotePath=None,persistance=False,secure=False):
      pass
   def send(self,*arguments):
      pass
   def setDirty(self,propertyName):
      pass
   def setProperty(self,propertyName,value=None):
      pass
class SharedObjectFlushStatus:
   FLUSHED = "flushed"
   PENDING = "pending"

if __name__ == "__main__":
   def eventCancel(event=None):
      print("cancel")
   def eventSelect(event=None):
      print("select")
   def eventComplete(event=None):
      print("complete")
   filter1 = FileFilter("Text File","*.txt")
   filter2 = FileFilter("Shell Script","*.sh")
   filter3 = FileFilter("Files","*.xml;*.exe;*.py")
   fr = FileReference()
   fr.addEventListener(Event.CANCEL,eventCancel)
   fr.addEventListener(Event.SELECT,eventSelect)
   fr.addEventListener(Event.COMPLETE,eventComplete)
   fr.browse([filter1,filter2,filter3])
   fr.save("test","test.txt")