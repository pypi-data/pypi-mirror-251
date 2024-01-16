import tkinter
import tkhtmlview
import PIL
import math
from io import BytesIO as btio
from as3lib import configmodule as confmod
from as3lib import toplevel as as3
from typing import Union
"""
Temporary interface to get things working. A bit slow when too many things are defined. Even after this module is no longer needed, it will stay for compatibility purposes.
Notes:
- Canvas is not supported yet even though there is an option for it
- When setting commands, they must be accessible from the scope of where they are called
- When grouping windows together, the object that should be used is <windowobject>.children["root"]
- If using xwayland, windows made using tkinter.Tk() will not group with windows made using tkinter.Toplevel()
"""
#Adobe flash minimum size is 262x0 for a window that starts out at 1176x662

confmod.interfaceType = "Tkinter"

def help():
   print("If you are confused about how to use this module, please run this module by itself and look at the test code at the bottom.")

#----------------------------------------------------
#This section contains code that is a modification of code from tkhtmlview
class _ScrolledListbox(tkinter.Listbox):
   #Uses HTMLScrolledText as a base but uses a listbox instead of HTMLText
   def __init__(self, master=None, **kwargs):
      self.frame = tkinter.Frame(master)
      self.vbar = tkinter.Scrollbar(self.frame)

      kwargs["yscrollcommand"] = self.vbar.set
      self.vbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
      self.vbar["command"] = self.yview

      tkinter.Listbox.__init__(self, self.frame, **kwargs)
      self.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

      text_meths = vars(tkinter.Text).keys()
      methods = vars(tkinter.Pack).keys() | vars(tkinter.Grid).keys() | vars(tkinter.Place).keys()
      methods = methods.difference(text_meths)

      for m in methods:
         if m[0] != "_" and m != "config" and m != "configure":
            setattr(self, m, getattr(self.frame, m))
      def __str__(self):
         return str(self.frame)
class ScrolledListbox(_ScrolledListbox):
   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
class HTMLText(tkhtmlview.HTMLScrolledText):
   #Modified to have no borders by default
   def __init__(self, *args, html=None, **kwargs):
      super().__init__(*args, html=None, **kwargs)
      self.configure(borderwidth=0,highlightthickness=0)
   def _w_init(self, kwargs):
      super()._w_init(kwargs)
      self.vbar.pack_forget()
   def fit_height(self):
      super().fit_height()
      self.vbar.pack_forget()
#----------------------------------------------------
class _ComboEntryBox:
   def __init__(self,master,x,y,width,height,anchor,font,textwidth,buttonwidth,text:Union[list,tuple,str,as3.String,as3.Array],buttontext="Ok",rows=1,textalign="w"):
      self._properties = {"x":x,"y":y,"width":width,"height":height,"anchor":anchor,"font":font,"textwidth":textwidth,"buttonwidth":buttonwidth,"text":text,"buttontext":buttontext,"rows":rows,"textalign":textalign}
      self.labels = []
      self.entries = []
      self.frame = tkinter.Frame(master)
      if rows < 1:
         raise Exception(f"ComboEntryBox; rows must be greater than or equal to 1, got {rows}")
      if rows == 1:
         self.frame.place(x=x,y=y,width=width,height=height,anchor=anchor)
         self.frame.configure(borderwidth=0,highlightthickness=0)
         if type(text) in (str,as3.String):
            self.labels.append(tkinter.Label(self.frame,text=text,font=font,anchor=textalign))
         else:
            self.labels.append(tkinter.Label(self.frame,text=text[0],font=font,anchor=textalign))
         self.labels[0].place(x=0-2,y=0,width=textwidth+2,height=height,anchor="nw")
         self.entries.append(tkinter.Entry(self.frame,font=font))
         self.entries[0].place(x=textwidth,y=0,width=width-(textwidth+buttonwidth),height=height,anchor="nw")
         self.button = tkinter.Button(self.frame,text=buttontext,font=font)
         self.button.place(x=textwidth+(width-(textwidth+buttonwidth)),y=0,width=buttonwidth,height=height,anchor="nw")
      else:
         self.frame.place(x=x,y=y,width=width,height=(height*rows),anchor=anchor)
         self.frame.configure(borderwidth=0,highlightthickness=0)
         if type(text) in (str,as3.String):
            for i in range(rows):
               self.labels.append(tkinter.Label(self.frame,text=text,font=font,anchor=textalign))
               self.labels[i].place(x=0-2,y=i*height,width=textwidth+2,height=height,anchor="nw")
         else:
            for i in range(rows):
               self.labels.append(tkinter.Label(self.frame,text=text[i],font=font,anchor=textalign))
               self.labels[i].place(x=0-2,y=i*height,width=textwidth+2,height=height,anchor="nw")
         for i in range(rows):
            self.entries.append(tkinter.Entry(self.frame,font=font))
            self.entries[i].place(x=textwidth,y=i*height,width=width-(textwidth+buttonwidth),height=height,anchor="nw")
         self.button = tkinter.Button(self.frame,text=buttontext,font=font)
         self.button.place(x=textwidth+(width-(textwidth+buttonwidth)),y=(rows-1)*height,width=buttonwidth,height=height,anchor="nw")
   def __resizeandplace(self):
      w = self._properties["width"]
      h = self._properties["height"]
      tw = self._properties["textwidth"]
      bw = self._properties["buttonwidth"]
      r = self._properties["rows"]
      self.frame.place(x=self._properties["x"],y=self._properties["y"],width=w,height=(h*r),anchor=self._properties["anchor"])
      for i in range(r):
         self.labels[i].place(x=0-2,y=i*h,width=tw+2,height=h,anchor="nw")
         self.entries[i].place(x=tw,y=i*h,width=w-(tw+bw),height=h,anchor="nw")
      self.button.place(x=tw+(w-(tw+bw)),y=(r-1)*h,width=bw,height=h,anchor="nw")
   def configure(self,**kwargs):
      k = list(kwargs.keys())
      v = list(kwargs.values())
      for i in range(0,len(k)):
         match k[i]:
            case "x" | "y" | "anchor":
               self._properties[k[i]] = v[i]
               self.frame.place(x=self._properties["x"],y=self._properties["y"],width=self._properties["width"],height=self._properties["height"],anchor=self._properties["anchor"])
            case "width" | "height" | "textwidth" | "buttonwidth":
               self._properties[k[i]] = v[i]
               self.__resizeandplace()
            case "font":
               self._properties["font"] = v[i]
               for j in range(self._properties["rows"]):
                  self.labels[j].configure(font=v[i])
                  self.entrys[j].configure(font=v[i])
               self.button.configure(font=v[i])
            case "text":
               if type(v[i]) in (str,list,tuple,as3.String,as3.Array):
                  self._properties["text"] = v[i]
                  if type(v[i]) in (str,as3.String):
                     for j in range(self._properties["rows"]):
                        self.labels[j].configure(text=v[i])
                  else:
                     for j in range(self._properties["rows"]):
                        self.labels[j].configure(text=v[i][j])
            case "buttontext":
               self._properties["buttontext"] = v[i]
               self.button.configure(text=v[i])
            case "command":
               self.button.configure(command=v[i])
            case "rows":
               print("Changing number of rows not implemented yet.")
            case "textalign":
               print("Changing text alignment not implemented yet.")
            case _:
               for i in (self.frame,self.label,self.entry,self.button):
                  i[k[i]] = v[i]
   def configurePlace(self,**kwargs):
      k = list(set(kwargs.keys()) & {"x","y","width","height","anchor","textwidth","buttonwidth"})
      for i in range(len(k)):
         self._properties[k[i]] = kwargs[k[i]]
      self.__resizeandplace()
   def getEntry(self,number,*args):
      return self.entries[number].get()
   def getEntries(self,*args):
      temp = []
      for i in self.entries:
         temp.append(i.get())
      return temp
   def destroy(self):
      self.frame.destroy()
class ComboEntryBox(_ComboEntryBox):
   #this item is not to be used in the resizable windows, it will not resize well
   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)

class window:
   __slots__ = ("windowproperties","children","childproperties","imagedict","htmlproperties","sbsettings","aboutwindow","menubar")
   def __init__(self,width,height,title="Python",type_="frame",color="#FFFFFF",mainwindow:bool=True,defaultmenu:bool=True,nomenu:bool=None,dwidth=None,dheight=None):
      self.windowproperties = {"oldmult":100,"fullscreen":False,"startwidth":width,"startheight":height,"dwidth":dwidth,"dheight":dheight,"mainwindow":mainwindow,"color":color}
      self.children = {}
      self.childproperties = {}
      self.imagedict = {} # imagename:{"references":numReferences,"oimage":data,"rimage":data,"osize":[width,height]}
      self.imagedict[""] = {"references":0,"oimage":"","rimage":"","osize":[0,0]}
      self.htmlproperties = {} # hstname:{"fg":fgcolor,"bg":bgcolor,"otext":otext,"ftext":ftext,"fontbold":fontbold,"sbsettings":[sbscaling,sbwidth]}
      self.sbsettings = {} # name:[scalingenable:bool,defaultsize:int]
      if mainwindow == True:
         self.aboutwindow = {"open":False,"text":"placeholdertext","objects":{}}
      else:
         self.aboutwindow = None
      if width < 262:
         width = 262
      self.windowproperties["startwidth"] = width
      self.windowproperties["startheight"] = height
      self.menubar = {}
      if mainwindow == True:
         self.children["root"] = tkinter.Tk()
      else:
         self.children["root"] = tkinter.Toplevel()
      if nomenu in (None,False):
         if defaultmenu == True:
            self.menubar["root"] = tkinter.Menu(self.children["root"], bd=1)
            self.menubar["filemenu"] = tkinter.Menu(self.menubar["root"], tearoff=0)
            self.menubar["filemenu"].add_command(label="Quit", font=("Terminal",8), command=self.endProcess)
            self.menubar["root"].add_cascade(label="File", font=("Terminal",8), menu=self.menubar["filemenu"])
            self.menubar["viewmenu"] = tkinter.Menu(self.menubar["root"], tearoff=0)
            self.menubar["viewmenu"].add_command(label="Full Screen", font=("Terminal",8), command=self.togglefullscreen)
            self.menubar["viewmenu"].add_command(label="Reset Size", font=("Terminal",8), command=self.resetSize)
            self.menubar["root"].add_cascade(label="View", font=("Terminal",8), menu=self.menubar["viewmenu"])
            self.menubar["controlmenu"] = tkinter.Menu(self.menubar["root"], tearoff=0)
            self.menubar["controlmenu"].add_command(label="Controls", font=("Terminal",8))
            self.menubar["root"].add_cascade(label="Control", font=("Terminal",8), menu=self.menubar["controlmenu"])
            if mainwindow == True:
               self.menubar["helpmenu"] = tkinter.Menu(self.menubar["root"], tearoff=0)
               self.menubar["helpmenu"].add_command(label="About", font=("Terminal",8), command=self.aboutwin)
            self.menubar["root"].add_cascade(label="Help", font=("Terminal",8), menu=self.menubar["helpmenu"])
            self.children["root"].config(menu=self.menubar["root"])
         else:
            self.menubar["root"] = tkinter.Menu(self.children["root"], bd=1)
            self.children["root"].config(menu=self.menubar["root"])
      self.children["root"].title(title)
      if dwidth == None:
         self.windowproperties["dwidth"] = self.windowproperties["startwidth"]
      else:
         self.windowproperties["dwidth"] = dwidth
      if dheight == None:
         self.windowproperties["dheight"] = self.windowproperties["startheight"]
      else:
         self.windowproperties["dheight"] = dheight
      if confmod.width not in (-1,None) and confmod.height not in (-1,None):
         self.children["root"].maxsize(confmod.width,confmod.height)
      match type_:
         case "canvas":
            self.children["display"] = tkinter.Canvas(self.children["root"], background=self.windowproperties["color"], confine=True)
            self.children["display"].place(anchor="center", width=self.windowproperties["startwidth"], height=self.windowproperties["startheight"], x=self.windowproperties["startwidth"]/2, y=self.windowproperties["startheight"]/2)
         case "frame":
            self.children["display"] = tkinter.Frame(self.children["root"], background=self.windowproperties["color"])
            self.children["display"].place(anchor="center", width=self.windowproperties["startwidth"], height=self.windowproperties["startheight"], x=self.windowproperties["startwidth"]/2, y=self.windowproperties["startheight"]/2)
         case _:
            raise Exception("type_ must be either frame or canvas.")
      self.children["root"].bind("<Configure>",self.doResize)
      self.children["root"].geometry(f"{self.windowproperties['dwidth']}x{self.windowproperties['dheight']}")
      self.children["root"].bind("<Escape>",self.outfullscreen)
   def __getattr__(self, key):
      return self.children[key]
   def resetSize(self):
      self.children["root"].geometry(f"{self.windowproperties['dwidth']}x{self.windowproperties['dheight']}")
   def group(self, object_:object):
      self.children["root"].group(object_)
   def toTop(self):
      self.children["root"].lift()
   def forceFocus(self, child:str):
      self.children[child].focus_force()
   def round(self, num):
      tempStr = "." + f"{num}".split(".")[1]
      if float(tempStr) >= 0.5: #0.85? 0.5? 1?
         return math.ceil(num)
      else:
         return math.floor(num)
   def minimumSize(self,type_:str="b",**kwargs):
      """
      type_ must be either 'w','h',or 'b' (meaning width, height, or both). If nothing is passed, assumed to be 'b' (both)
      kwargs must include width, height, or both depending on what you chose for type_
      if 'w' or 'height' is chosen, the other will be assumed based on the ration of the original size
      """
      match type_:
         case "w":
            if self.windowproperties["mainwindow"] == True:
               self.children["root"].minsize(kwargs["width"],int((kwargs["width"]*self.windowproperties["startheight"])/self.windowproperties["startwidth"]) + 28)
            else:
               self.children["root"].minsize(kwargs["width"],int((kwargs["width"]*self.windowproperties["startheight"])/self.windowproperties["startwidth"]))
         case "h":
            if self.windowproperties["mainwindow"] == True:
               self.children["root"].minsize(int((self.windowproperties["startwidth"]*kwargs["height"])/self.windowproperties["startheight"]) - 52,kwargs["height"])
            else:
               self.children["root"].minsize(int((self.windowproperties["startwidth"]*kwargs["height"])/self.windowproperties["startheight"]),kwargs["height"])
         case "b":
            self.children["root"].minsize(kwargs["width"],kwargs["height"])
         case _:
            as3.trace("Invalid type")
   def minimumSizeReset(self):
      if self.windowproperties["mainwindow"] == True:
         self.children["root"].minsize(262,int((262*self.windowproperties["startheight"])/self.windowproperties["startwidth"]) + 28)
      else:
         self.children["root"].minsize(262,int((262*self.windowproperties["startheight"])/self.windowproperties["startwidth"]))
   def resizefont(self, font:tuple, mult):
      return (font[0],self.round(font[1]*mult/100))
   def mainloop(self):
      if self.windowproperties["mainwindow"] == False:
         print("Can not run mainloop on a child window.")
      else:
         self.resizeChildren(100)
         self.children["root"].mainloop()
   def enableResizing(self):
      self.children["root"].resizable(True,True)
   def disableResizing(self):
      self.children["root"].resizable(False,False)
   def endProcess(self):
      self.children["root"].destroy()
   def closeWindow(self):
      self.children["root"].destroy()
   def togglefullscreen(self):
      match self.windowproperties["fullscreen"]:
         case False:
            self.gofullscreen()
         case True:
            self.outfullscreen()
   def gofullscreen(self):
      self.windowproperties["fullscreen"] = True
      self.children["root"].attributes("-fullscreen", True)
   def outfullscreen(self, useless=""):
      self.windowproperties["fullscreen"] = False
      self.children["root"].attributes("-fullscreen", False)
   def setAboutWindowText(self, text):
      if self.aboutwindow != None:
         self.aboutwindow["text"] = text
         if "label" in self.aboutwindow["objects"]:
            self.aboutwindow["objects"]["label"].configure(text=text)
   def aboutwin(self):
      if self.aboutwindow != None:
         if self.aboutwindow["open"] == False:
            self.aboutwindow["objects"]["window"] = tkinter.Toplevel()
            self.aboutwindow["objects"]["window"].geometry("350x155")
            self.aboutwindow["objects"]["window"].resizable(False,False)
            self.group(self.aboutwindow["objects"]["window"])
            self.aboutwindow["objects"]["window"].configure(background=self.windowproperties["color"])
            self.aboutwindow["objects"]["label"] = tkinter.Label(self.aboutwindow["objects"]["window"], font=("TkTextFont",9), justify="left", text=self.aboutwindow["text"], background=self.windowproperties["color"])
            self.aboutwindow["objects"]["label"].place(anchor="nw", x=7, y=9)
            self.aboutwindow["objects"]["okbutton"] = tkinter.Button(self.aboutwindow["objects"]["window"], text="OK", command=self.closeabout, background=self.windowproperties["color"])
            self.aboutwindow["objects"]["okbutton"].place(anchor="nw", width=29, height=29, x=299, y=115)
            self.aboutwindow["open"] = True
         else:
            self.aboutwindow["objects"]["window"].lift()
   def closeabout(self):
      if self.aboutwindow != None:
         for i in self.aboutwindow["objects"]:
            try:
               self.aboutwindow["objects"][i].destroy()
            except:
               continue
         self.aboutwindow["open"] = False
         self.aboutwindow["objects"].clear()
   def addButton(self, master:str, name:str, x, y, width, height, font, anchor:str="nw"):
      if master == "root":
         master = "display"
      if as3.isXMLName(master) == False:
         as3.trace("Invalid Master")
         pass
      elif as3.isXMLName(name) == False:
         as3.trace("Invalid Name")
         pass
      else:
         self.children[name] = tkinter.Button(self.children[master])
         self.children[name].place(x=x,y=y,width=width,height=height,anchor=anchor)
         self.childproperties[name] = [None,"Button",x,y,width,height,font,anchor]
         self.resizeChild(name, self.windowproperties["oldmult"])
   def addLabel(self, master:str, name:str, x, y, width, height, font, anchor:str="nw"):
      if master == "root":
         master = "display"
      if as3.isXMLName(master) == False:
         as3.trace("Invalid Master")
         pass
      elif as3.isXMLName(name) == False:
         as3.trace("Invalid Name")
         pass
      else:
         self.children[name] = tkinter.Label(self.children[master])
         self.children[name].place(x=x,y=y,width=width,height=height,anchor=anchor)
         self.childproperties[name] = [None,"Label",x,y,width,height,font,anchor]
         self.resizeChild(name, self.windowproperties["oldmult"])
   def addnwhLabel(self, master:str, name:str, x, y, font, anchor:str="nw"):
      if master == "root":
         master = "display"
      if as3.isXMLName(master) == False:
         as3.trace("Invalid Master")
         pass
      elif as3.isXMLName(name) == False:
         as3.trace("Invalid Name")
         pass
      else:
         self.children[name] = tkinter.Label(self.children[master])
         self.children[name].place(x=x,y=y,anchor=anchor)
         self.childproperties[name] = [None,"nwhLabel",x,y,None,None,font,anchor]
         self.resizeChild(name, self.windowproperties["oldmult"])
   def addFrame(self, master:str, name:str, x, y, width, height, anchor:str="nw"):
      if master == "root":
         master = "display"
      if as3.isXMLName(master) == False:
         as3.trace("Invalid Master")
         pass
      elif as3.isXMLName(name) == False:
         as3.trace("Invalid Name")
         pass
      else:
         self.children[name] = tkinter.Frame(self.children[master])
         self.children[name].place(x=x,y=y,width=width,height=height,anchor=anchor)
         self.childproperties[name] = [None,"Frame",x,y,width,height,None,anchor]
         self.resizeChild(name, self.windowproperties["oldmult"])
   def addHTMLScrolledText(self, master:str, name:str, x, y, width, height, font, anchor:str="nw", sbscaling:bool=True, sbwidth:int=12):
      if master == "root":
         master = "display"
      if as3.isXMLName(master) == False:
         as3.trace("Invalid Master")
         pass
      elif as3.isXMLName(name) == False:
         as3.trace("Invalid Name")
         pass
      else:
         self.children[name] = tkhtmlview.HTMLScrolledText(self.children[master])
         self.children[name].place(x=x,y=y,width=width,height=height,anchor=anchor)
         self.htmlproperties[name] = {"fg":'#000000',"bg":'#FFFFFF',"otext":"","ftext":"","fontbold":False,"sbsettings":[sbscaling,sbwidth]}
         self.childproperties[name] = [None,"HTMLScrolledText",x,y,width,height,font,anchor]
         self.resizeChild(name, self.windowproperties["oldmult"])
   def addHTMLText(self, master:str, name:str, x, y, width, height, font, anchor:str="nw"):
      if master == "root":
         master = "display"
      if as3.isXMLName(master) == False:
         as3.trace("Invalid Master")
         pass
      elif as3.isXMLName(name) == False:
         as3.trace("Invalid Name")
         pass
      else:
         self.children[name] = HTMLText(self.children[master])
         self.children[name].place(x=x,y=y,width=width,height=height,anchor=anchor)
         self.htmlproperties[name] = {"fg":'#000000',"bg":'#FFFFFF',"otext":"","ftext":"","fontbold":False,"sbsettings":None}
         self.childproperties[name] = [None,"HTMLText",x,y,width,height,font,anchor]
         self.resizeChild(name, self.windowproperties["oldmult"])
   def prepareHTMLST(self, child:str, text:str):
      if self.htmlproperties[child]["otext"] == text:
         self.HTMLUpdateText(child, True)
      else:
         self.htmlproperties[child]["otext"] = text
         self.HTMLUpdateText(child)
   def HTMLUpdateText(self, child:str, rt=False):
      self.children[child]["state"] = "normal"
      font = self.childproperties[child][6]
      if rt == False:
         self.htmlproperties[child]["ftext"] = self.htmlproperties[child]["otext"].replace("\t","    ")
      text = f"<pre style=\"color: {self.htmlproperties[child]['fg']}; background-color: {self.htmlproperties[child]['bg']}; font-size: {int(font[1]*self.windowproperties['oldmult']/100)}px; font-family: {font[0]}\">{self.htmlproperties[child]['ftext']}</pre>"
      if self.htmlproperties[child]["fontbold"]:
         text = f"<b>{text}</b>"
      self.children[child].set_html(text)
      self.children[child]["state"] = "disabled"
   def addImage(self, image_name:str, image_data, size:tuple=None):
      """
      size - the target (display) size of the image before resizing
      if size is not defined it is assumed to be the actual image size
      """
      if image_name == "":
         trace("interfacetkError","image_name can not be empty string",isError=True)
         pass
      self.imagedict[image_name] = {"references":0,"oimage":image_data}
      if size != None:
         self.imagedict[image_name]["osize"] = [size[0],size[1]]
      else:
         ims = PIL.Image.open(btio(image_data)).size
         self.imagedict[image_name]["osize"] = [ims[0],ims[1]]
      self.resizeImage((self.imagedict[image_name]["osize"][0],self.imagedict[image_name]["osize"][1]), image_name)
   def addImageLabel(self, master:str, name:str, x, y, width, height, anchor:str="nw", image_name:str=""):
      if master == "root":
         master = "display"
      if as3.isXMLName(master) == False:
         as3.trace("Invalid Master")
         pass
      elif as3.isXMLName(name) == False:
         as3.trace("Invalid Name")
         pass
      else:
         self.children[name] = tkinter.Label(self.children[master])
         self.children[name].place(x=x,y=y,width=width,height=height,anchor=anchor)
         self.children[name]["image"] = self.imagedict[image_name]["rimage"]
         self.imagedict[image_name]["references"] += 1
         self.childproperties[name] = [None,"ImageLabel",x,y,width,height,None,anchor,image_name]
         self.resizeChild(name, self.windowproperties["oldmult"])
   def addScrolledListbox(self, master:str, name:str, x, y, width, height, font, anchor:str="nw", sbscaling:bool=True, sbwidth:int=12):
      if master == "root":
         master = "display"
      if as3.isXMLName(master) == False:
         as3.trace("Invalid Master")
         pass
      elif as3.isXMLName(name) == False:
         as3.trace("Invalid Name")
         pass
      else:
         self.sbsettings[name] = [sbscaling,sbwidth]
         self.children[name] = ScrolledListbox(self.children[master])
         self.children[name].place(x=x,y=y,width=width,height=height,anchor=anchor)
         self.childproperties[name] = [None,"ScrolledListbox",x,y,width,height,font,anchor]
         self.resizeChild(name, self.windowproperties["oldmult"])
   def slb_Insert(self, child:str, position, item):
      self.children[child].insert(position,item)
   def slb_Delete(self, child:str, start, end):
      self.children[child].delete(start, end)
   def resizeImage(self, size:tuple, image_name):
      if image_name != "":
         img = PIL.Image.open(btio(self.imagedict[image_name]["oimage"]))
         img.thumbnail(size)
         self.imagedict[image_name]["rimage"] = PIL.ImageTk.PhotoImage(img)
   def resizeChildren(self, mult):
      nm = mult/100
      for i in self.imagedict:
         self.resizeImage((int(self.imagedict[i]["osize"][0]*nm),int(self.imagedict[i]["osize"][1]*nm)),i)
      for i in self.childproperties:
         if i in ("display","root"):
            continue
         cl = self.childproperties[i]
         if cl[1] == "nwhLabel":
            self.children[i].place(x=cl[2]*nm,y=cl[3]*nm,anchor=cl[7])
         else:
            self.children[i].place(x=cl[2]*nm,y=cl[3]*nm,width=cl[4]*nm,height=cl[5]*nm,anchor=cl[7])
         match cl[1]:
            case "HTMLScrolledText":
               if self.htmlproperties[i]["sbsettings"][0] == True:
                  self.children[i].vbar["width"] = self.htmlproperties[i]["sbsettings"][1]*nm
               self.HTMLUpdateText(i,True)
            case "HTMLText":
               self.HTMLUpdateText(i,True)
            case "ScrolledListbox":
               if self.sbsettings[i][0] == True:
                  self.children[i].vbar["width"] = self.sbsettings[i][1]*nm
               self.children[i]["font"] = self.resizefont(cl[6],mult)
            case "ImageLabel":
               self.children[i]["image"] = self.imagedict[cl[8]]["rimage"]
            case _:
               if cl[1] != "Frame":
                  self.children[i]["font"] = self.resizefont(cl[6],mult)
   def resizeChild(self, child:str, mult):
      if child not in self.children or child in ("display","root"):
         pass
      nm = mult/100
      cl = self.childproperties[child]
      match cl[1]:
         case "nwhLabel":
            self.children[child].place(x=cl[2]*nm,y=cl[3]*nm,anchor=cl[7])
         case _:
            self.children[child].place(x=cl[2]*nm,y=cl[3]*nm,width=cl[4]*nm,height=cl[5]*nm,anchor=cl[7])
      match cl[1]:
         case "HTMLScrolledText":
            if self.htmlproperties[child]["sbsettings"][0] == True:
               self.children[child].vbar["width"] = self.htmlproperties[child]["sbsettings"][1]*nm
            self.HTMLUpdateText(child,True)
         case "HTMLText":
            self.HTMLUpdateText(child,True)
         case "ScrolledListbox":
            if self.sbsettings[child][0] == True:
               self.children[child].vbar["width"] = self.sbsettings[child][1]*nm
            self.children[child]["font"] = self.resizefont(cl[6],mult)
         case "ImageLabel":
            self.children[child]["image"] = self.imagedict[cl[8]]["rimage"]
         case _:
            if cl[1] != "Frame":
               self.children[child]["font"] = self.resizefont(cl[6],mult)
   def bindChild(self, child:str, tkevent, function):
      self.children[child].bind(tkevent, function)
   def configureChild(self, child:str, **args):
      k = list(args.keys())
      v = list(args.values())
      for i in range(0, len(k)):
         match k[i]:
            case "x" | "y" | "width" | "height" | "font"| "anchor":
               if child in ("display","root"):
                  continue
               newlist = self.childproperties[child]
               match k[i]:
                  case "x":
                     newlist[2] = v[i]
                  case "y":
                     newlist[3] = v[i]
                  case "width":
                     newlist[4] = v[i]
                  case "height":
                     newlist[5] = v[i]
                  case "font":
                     newlist[6] = v[i]
                  case "anchor":
                     newlist[7] = v[i]
               self.childproperties[child] = newlist
               self.resizeChild(child, self.windowproperties["oldmult"])
            case "text" | "textadd":
               if child in ("display","root"):
                  continue
               if self.childproperties[child][1] in ("HTMLScrolledText","HTMLText"):
                  if k[i] == "text":
                     self.prepareHTMLST(child, v[i])
                  else:
                     self.prepareHTMLST(child, self.htmlproperties[child]["otext"] + v[i])
               else:
                  self.children[child][k[i]] = v[i]
            case "background" | "foreground":
               if child == "display":
                  if k[i] == "background":
                     self.children["display"]["bg"] = v[i]
               else:
                  match self.childproperties[child][1]:
                     case "Frame":
                        if k[i] == "background":
                           self.children[child]["bg"] = v[i]
                     case "HTMLScrolledText" | "HTMLText":
                        self.children[child][k[i]] = v[i]
                        if k[i] == "background":
                           self.htmlproperties[child]["bg"] = v[i]
                        else:
                           self.htmlproperties[child]["fg"] = v[i]
                        self.prepareHTMLST(child, self.htmlproperties[child]["otext"])
                     case _:
                        self.children[child][k[i]] = v[i]
            case "image":
               if child in ("display","root"):
                  continue
               self.imagedict[self.childproperties[child][8]]["references"] -= 1
               self.childproperties[child][8] = v[i]
               self.imagedict[v[i]]["references"] += 1
               self.children[child]["image"] = self.imagedict[v[i]]["rimage"]
            case "htmlfontbold":
               if child in ("display","root"):
                  continue
               if self.childproperties[child][1] in ("HTMLScrolledText","HTMLText"):
                  self.htmlproperties[child]["fontbold"] = v[i]
                  self.prepareHTMLST(child, self.htmlproperties[child]["otext"])
            case "sbwidth":
               if child in ("display","root"):
                  continue
               match self.childproperties[child][1]:
                  case "HTMLScrolledText":
                     self.htmlproperties[child]["sbsettings"][1] = int(v[i])
                  case "ScrolledListBox":
                     self.sbsettings[child][1] = int(v[i])
            case _:
               self.children[child][k[i]] = v[i]
   def destroyChild(self, child:str):
      if child in ("display","root"):
         pass
      temppref = self.childproperties.pop(child)
      match temppref[1]:
         case "HTMLScrolledText" | "HTMLText":
            self.htmlproperties.pop(child)
         case "ScrolledListbox":
            self.sbsettings.pop(child)
         case "ImageLabel":
            self.imagedict[temppref[8]]["references"] -= 1
      self.children[child].destroy()
      self.children.pop(child)
   def getChildAttribute(self, child:str, attribute:str):
      return self.children[child].cget(attribute)
   def getChildAttributes(self, child:str, *args:str):
      templist = {}
      for i in args:
         templist.append(getChildAttribute(child, i))
      return templist
   def doResize(self, event):
      if event.widget == self.children["root"]:
         newwidth = self.children["root"].winfo_width()
         newheight = self.children["root"].winfo_height()
         mult = self.calculate(newwidth,newheight)
         self.set_size(mult,newwidth,newheight)
         if mult != self.windowproperties["oldmult"]:
            self.windowproperties["oldmult"] = mult
            self.resizeChildren(mult)
   def calculate(self,newwidth,newheight):
      xmult = (100*newwidth)/self.windowproperties["startwidth"]
      ymult = (100*newheight)/self.windowproperties["startheight"]
      if xmult > ymult:
         mult = ymult
      elif xmult < ymult:
         mult = xmult
      elif xmult == ymult:
         mult = xmult
      return mult
   def set_size(self,mult,newwidth,newheight):
      nm = mult/100
      self.children["display"].place(anchor="center", width=self.windowproperties["startwidth"]*nm, height=self.windowproperties["startheight"]*nm, x=math.floor(newwidth/2), y=math.floor(newheight/2))

if __name__ == "__main__":
   #Test
   from platform import python_version
   testcolor = 0
   fontBold = False
   def test_changebold():
      global fontBold
      if fontBold == True:
         fontBold = False
         return False
      elif fontBold == False:
         fontBold = True
         return True
   def test_cyclecolor():
      global testcolor
      testcolorlist = ["#FFFFFF","#8F2F9F","#AAAAAA"]
      testcolor += 1
      if testcolor >= 3:
         testcolor = 0
      return testcolorlist[testcolor]
   root = window(1176,662,title="Adobe Flash Projector-like Window Demo")
   root.setAboutWindowText(f"Adobe Flash Projector-like window demo.\n\nPython {python_version()}")
   root.addButton("root","testbutton1",130,0,130,30,("Times New Roman",12))
   root.configureChild("testbutton1",command=lambda: root.configureChild("testtext", background=test_cyclecolor()))
   root.addLabel("root","testlabel1",0,30,100,20,("Times New Roman",12))
   root.addHTMLScrolledText("root","testtext",0,50,600,400,("Times New Roman",12),anchor="nw")
   root.addHTMLText("root","testtext2",601,50,400,400,("Times New Roman",12),anchor="nw")
   root.configureChild("testtext", text="TestTextpt1\n\nTestTextpt2", cursor="arrow", wrap="word")
   root.configureChild("testtext2", text="HTMLTextTest\n\ntext", cursor="arrow", wrap="word")
   root.configureChild("testbutton1", text="st_colourtest")
   root.configureChild("testlabel1", text="TestLabel")
   secondwindow = window(400,400,title="Second Window",type_="frame",mainwindow=False,nomenu=True)
   secondwindow.group(root.children["root"])
   root.addButton("root","testbutton2",0,0,130,30,("Times New Roman",12))
   root.configureChild("testbutton2",command=lambda: secondwindow.toTop()) 
   root.configureChild("testbutton2", text="liftsecondwindow")
   root.addButton("root","testbutton3",260,0,130,30,("Times New Roman",12))
   root.configureChild("testbutton3",command=lambda: root.configureChild("testtext",htmlfontbold=test_changebold()))
   root.configureChild("testbutton3", text="st_boldtest")
   root.addScrolledListbox("root","testslb",0,450,150,150,("Times New Roman",12))
   l1 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
   for i in l1:
      root.slb_Insert("testslb", "end", i)
   root.mainloop()