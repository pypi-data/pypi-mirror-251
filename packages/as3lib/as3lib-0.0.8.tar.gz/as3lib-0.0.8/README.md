<h1>python-as3lib</h1>
A partial implementation of ActionScript3 and flash in python. Things are as close as I could get them with my knowledge and the very limited documentation that adobe provides. Once I learn how to make python c modules, I plan on offloading some of this stuff to c or c++ modules to speed things up. If I can figure out how to do it in this context, I might implement the interface in OpenGL, Vulkan, or something like PyGame to make it work better and more customizable. Some stuff will be impossible to implement in python because <a href="https://docs.python.org/3/glossary.html#term-global-interpreter-lock">python is a fish</a>.
<br><br>Version 0.0.8 note: I have currently implemented basic dependency checks. They aren't very good and might fail. If you have problems with them, remove the line in initconfig.py that calls the function "dependencyCheck" or change the variable "checkdependencies" in configmodule.py to False.
<br><br>Warning: Some early versions of this library that contain the config module are broken on Windows. It was fixed in version 0.0.6.
<br><br><b>If you are using wayland, this library will have a first time init message because wayland does not currently support fetching some values automatically. You must either launch this library, or the program that uses it, from the terminal to input these values, or fill out the blank config file that I provide on github (it will lock up otherwise).</b> These values are stored in &lt;library-directory&gt;/wayland.cfg. They are only needed if you are using any of the graphical elements of this library. I will not be able to fix the window grouping jank on wayland until tcl/tk natively supports wayland.
<br><br>I have no way as of current to test the accuracy of these functions as I can't find a compiler for actionscript that I could get to work so if anything doesn't work or there is undocumented functionality please let me know on the github issues page. DO NOT EMAIL ME, I will not respond and nothing will get fixed.
<h3>Requirements</h3>
System:
<br>&emsp;Linux:
<br>&emsp;&emsp;bash (will add support for others later)
<br>&emsp;&emsp;xwininfo (xorg)
<br>&emsp;&emsp;xrandr (xorg)
<br>&emsp;&emsp;echo
<br>&emsp;&emsp;grep
<br>&emsp;&emsp;awk
<br>&emsp;&emsp;loginctl (This requirement will probably be removed later, this was just the easiest way to do things)
<br>&emsp;&emsp;whoami
<br>&emsp;Windows:
<br>&emsp;&emsp;PyLaucher (should be included in the python installer)
<br>Python:
<br>&emsp;Built-in:
<br>&emsp;&emsp;tkinter, re, math, io, platform, subprocess, random, time, datetime, os, pwd (linux), pathlib, configparser, webbrowser, textwrap, typing
<br>&emsp;External:
<br>&emsp;&emsp;<a href="https://pypi.org/project/numpy">numpy</a>, <a href="https://pypi.org/project/Pillow">Pillow</a>, <a href="https://pypi.org/project/tkhtmlview">tkhtmlview</a>
<h3>Future Requirements</h3>
The requirements that are going to be needed in the future once I implement more.
<br>Python:
<br>lzma, zlib, gzip
<h3>Modules</h3>
There are currently 16 modules plus a parser (not even close to working yet, I also don't know how far I'll be able to go with it) in this library, toplevel, interface_tk, keyConversions, configmodule, initconfig, com.adobe, flash.ui, flash.display, flash.filesystem, flash.utils, flash.events, flash.display3D, flash.net, flash.crypto, flash.system, and flash.errors.
<h4>toplevel</h4>
Most of the functions and classes are implemented but there are some things missing. The inherited properties of many of the classes would be a pain to implement so I left them out for now.
<br><br>As of version 0.0.7 I reimplemented the Array and String class as extensions of the their conterparts from python instead of how I was doing it. I also implemented creating an array to a specified size in the constructor and implemented the length assignment feature. Array.toSize has been merged into length and no longer exists. I also added the ability to specify what to fill the empty slots with when using length assignment (not in actionscript).
<br><br>I implemented the type conversions inside a separate function in some of the dataclasses (ex: String._String(exression)). These are used as part of the constructor (__init__ function) but are separate in case they need to be used multiple times or by those using this library. They return values in python types instead of in the types of this module because they are meant to be used internally.
<br><br>As of version 0.0.8 the length properties of various classes are properties instead of functions (as they should be). The Int class is now named properly (now named int) and the rest of the module uses builtins.int for python integers. This version also makes many functions more accurate to the original as well as making some things faster.
<h4>interface_tk</h4>
<b>Warning:</b> This module is does not retain compatibility between versions, things will change when I need them to with no regard to consistancy.
<br>Unlike the other modules, this one is completely different from anything actionscript had. This module implements dynamic scaling and other things that I need for a game port that I am working on. I will try to make one with similar syntax to actionscript later (no promises). Making the windows too small will result in a divide by zero error and might cause the program to crash if not handled. This will be fixed later.
<h4>keyConversions</h4>
This module includes cross-platform key conversion functions for tkinter events, javascript (actionscript) keycodes, and mouse buttons (currently only supports united states standard keyboard on linux and windows).
<h4>configmodule</h4>
The module that holds all of the things that this library needs globally or that need to be used many times so I only have to fetch them once. This module includes information like;
<br>the current platform
<br>the library directory
<br>library debug status
<br>the config for the trace function loaded from mm.cfg
<br>details about the screen (width, hight, refresh rate, and color depth) for the display module.
<br>information about the filesystem (path separator, user directory, desktop directory, and documents directory) for the flash.filesystem module
<br>library initialization status and errors
<h4>initconfig</h4>
The module that is called when this library initializes and its only purpose is to set the variables in configmodule.
<br>Note: use of multiple displays has not been tested yet.
<h4>flash.cryto</h4>
This module is as cryptographically secure as it can be while being reasonably fast. It uses the os.urandom function. Currently its functions return python strings because I haven't implemented bytearrays yet but I plan to switch it in the future.
<h4>com.adobe, flash.ui, flash.display, flash.filesystem, flash.utils, flash.events, flash.display3D, flash.net, flash.cryto, flash.system, and flash.errors</h4>
These modules contain things from their respective actionscript modules. None of them are complete yet since many actionscript modules rely on each other to function. I have to go back and forth between modules coding things here and there so these are taking much longer than the other modules.
<h3>Config Files</h3>
&lt;library-directory&gt;/mm.cfg - this file is the same as it was in actionscript with the same options as defined <a href="https://web.archive.org/web/20180227100916/helpx.adobe.com/flash-player/kb/configure-debugger-version-flash-player.html">here</a> with the exception of "ClearLogsOnStartup" which I added to configure what it says. Its defualt value is 1 to match the behavior in actionscript.
<br>&lt;library-directory&gt;/wayland.cfg - generated on the first use of this library if you are using wayland. Stores all of the values that can't be fetch automatically so you only have to input them once. They must be changed manually if you want to change them.
