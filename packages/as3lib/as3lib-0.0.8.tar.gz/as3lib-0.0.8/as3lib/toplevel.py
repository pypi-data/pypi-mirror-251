import math as m
import random as r
from numpy import nan, inf, NINF, base_repr
from textwrap import wrap
from time import time, strftime
from datetime import datetime
from pathlib import Path
from . import configmodule
from typing import Union
import builtins

class Array:
   #dummy class
   pass
class Boolean:
   #dummy class
   pass
class int:
   #dummy class
   pass
class Number:
   #dummy class
   pass
class String:
   #dummy class
   pass
class uint:
   #dummy class
   pass
class Vector:
   #dummy class
   pass
class NInfinity:
   __slots__ = ("__value")
   def __init__(self):
      self.__value = NINF
   def __str__(self):
      return "-Infinity"
   def __repr__(self):
      return self.__value
   def __lt__(self, value):
      if typeName(value) == "NInfinity":
         return False
      else:
         return True
   def __le__(self, value):
      if typeName(value) == "NInfinity":
         return True
      else:
         return False
   def __eq__(self, value):
      if typeName(value) == "NInfinity":
         return True
      else:
         return False
   def __ne__(self, value):
      if typeName(value) == "NInfinity":
         return False
      else:
         return True
   def __gt__(self, value):
      return False
   def __ge__(self, value):
      if typeName(value) == "NInfinity":
         return True
      else:
         return False
   def __bool__(self):
      return True
   def __getattr__(self, value):
      return "NInfinity"
   def __getattribute__(self, value):
      return "NInfinity"
   def __setattr__(self, *value):
      pass
   def __add__(self, value):
      return self
   def __radd__(self, value):
      return self
   def __iadd__(self, value):
      return self
   def __sub__(self, value):
      return self
   def __mul__(self, value):
      return self
   def __matmul__(self, value):
      return self
   def __truediv__(self, value):
      return self
   def __floordiv__(self, value):
      return self
   def __mod__(self, value):
      return self
   def __divmod__(self, value):
      return self
   def __pow__(self, value):
      return self
   def __lshift__(self, value):
      return self
   def __rshift__(self, value):
      return self
   def __and__(self, value):
      if bool(value) == True:
         return True
      else:
         return False
   def __or__(self, value):
      return True
   def __xor__(self, value):
      if bool(value) == True:
         return False
      else:
         return True
   def __neg__(self):
      return self
   def __pos__(self):
      return NInfinity()
   def __abs__(self):
      return Infinity()
   def __invert__(self):
      return Infinity()
   def __complex__(self):
      return self
   def __int__(self):
      return self
   def __float__(self):
      return self
   def __round__(self):
      return self
   def __floor__(self):
      return self
   def __ceil__(self):
      return self
class Infinity:
   __slots__ = ("__value")
   def __init__(self):
      self.__value = inf
   def __str__(self):
      return "Infinity"
   def __repr__(self):
      return self.__value
   def __lt__(self, value):
      return False
   def __le__(self, value):
      if typeName(value) == "Infinity":
         return True
      else:
         return False
   def __eq__(self, value):
      if typeName(value) == "Infinity":
         return True
      else:
         return False
   def __ne__(self, value):
      if typeName(value) == "Infinity":
         return False
      else:
         return True
   def __gt__(self, value):
      if typeName(value) == "Infinity":
         return False
      else:
         return True
   def __ge__(self, value):
      return True
   def __bool__(self):
      return True
   def __getattr__(self, value):
      return "Infinity"
   def __getattribute__(self, value):
      return "Infinity"
   def __setattr__(self, *value):
      pass
   def __add__(self, value):
      return self
   def __radd__(self, value):
      return self
   def __iadd__(self, value):
      return self
   def __sub__(self, value):
      return self
   def __mul__(self, value):
      return self
   def __matmul__(self, value):
      return self
   def __truediv__(self, value):
      return self
   def __floordiv__(self, value):
      return self
   def __mod__(self, value):
      return self
   def __divmod__(self, value):
      return self
   def __pow__(self, value):
      return self
   def __lshift__(self, value):
      return self
   def __rshift__(self, value):
      return self
   def __and__(self, value):
      if bool(value) == True:
         return True
      else:
         return False
   def __or__(self, value):
      return True
   def __xor__(self, value):
      if bool(value) == True:
         return False
      else:
         return True
   def __neg__(self):
      return NInfinity()
   def __pos__(self):
      return self
   def __abs__(self):
      return self
   def __invert__(self):
      return NInfinity()
   def __complex__(self):
      return self
   def __int__(self):
      return self
   def __float__(self):
      return self
   def __round__(self):
      return self
   def __floor__(self):
      return self
   def __ceil__(self):
      return self
class NaN:
   __slots__ = ("__value")
   def __init__(self):
      self.__value = nan
   def __str__(self):
      return "NaN"
   def __repr__(self):
      return f"{self.__value}"
   def __lt__(self, value):
      return False
   def __le__(self, value):
      return False
   def __eq__(self, value):
      return False
   def __ne__(self, value):
      return True
   def __gt__(self, value):
      return False
   def __ge__(self, value):
      return False
   def __bool__(self):
      return False
   def __getattr__(self, value):
      return "NaN"
   def __getattribute__(self, value):
      return "NaN"
   def __setattr__(self, *value):
      pass
   def __contains__(self, value):
      return False
   def __add__(self, value):
      return self
   def __radd__(self, value):
      return self
   def __iadd__(self, value):
      return self
   def __sub__(self, value):
      return self
   def __mul__(self, value):
      return self
   def __matmul__(self, value):
      return self
   def __truediv__(self, value):
      return self
   def __floordiv__(self, value):
      return self
   def __mod__(self, value):
      return self
   def __divmod__(self, value):
      return self
   def __pow__(self, value):
      return self
   def __lshift__(self, value):
      return self
   def __rshift__(self, value):
      return self
   def __and__(self, value):
      return False
   def __xor__(self, value):
      return False
   def __or__(self, value):
      return False
   def __neg__(self):
      return self
   def __pos__(self):
      return self
   def __abs__(self):
      return self
   def __invert__(self):
      return
   def __complex__(self):
      return self
   def __int__(self):
      return self
   def _uint(self):
      return 0
   def __float__(self):
      return self
   def __round__(self):
      return self
   def __trunc__(self):
      return self
   def __floor__(self):
      return self
   def __ceil__(self):
      return self
class undefined:
   __slots__ = ("value")
   def __init__(self):
      self.value = None
   def __str__(self):
      return "undefined"
   def __repr__(self):
      return "None"
class null:
   __slots__ = ("value")
   def __init__(self):
      self.value = None
   def __str__(self):
      return "null"
   def __repr__(self):
      return "None"

class ArgumentError():
   __slots__ = ("error")
   def __init__(self, message=""):
      trace(type(self), message, isError=True)
      self.error = message
class Array(list):
   __slots__ = ("filler")
   CASEINSENSITIVE = 1
   DESCENDING = 2
   UNIQUESORT = 4
   RETURNINDEXEDARRAY =  8
   NUMERIC = 16
   def __init__(self,*args,numElements:Union[builtins.int,int]=None):
      self.filler = undefined()
      if numElements == None:
         super().__init__(args)
      else:
         if numElements < 0:
            RangeError(f"Array; numElements can not be less than 0. numElements is {numElements}")
         else:
            tempList = []
            for i in range(0,numElements):
               tempList.append(undefined())
            super().__init__(tempList)
   def __getitem__(self, item):
      try:
         if super().__getitem__(item) == None:
            return undefined()
         else:
            return super().__getitem__(item)
      except:
         return ""
   def _getLength(self):
      return len(self)
   def _setLength(self,value:Union[builtins.int,int]):
      if value < 0:
         trace("RangeError",f"Array; new length {value} is below zero",isError=True)
      elif value == 0:
         self.clear()
      elif len(self) > value:
         while len(self) > value:
            self.pop()
      elif len(self) < value:
         while len(self) < value:
            self.append(self.filler)
   length = property(fget=_getLength,fset=_setLength)
   def setFiller(self,newFiller):
      self.filler = newFiller
   def concat(self,*args):
      """
      Concatenates the elements specified in the parameters with the elements in an array and creates a new array. If the parameters specify an array, the elements of that array are concatenated. If you don't pass any parameters, the new array is a duplicate (shallow clone) of the original array.
      Parameters:
         *args — A value of any data type (such as numbers, elements, or strings) to be concatenated in a new array.
      Returns:
         Array — An array that contains the elements from this array followed by elements from the parameters.
      """
      if len(args) == 0:
         raise Exception("Must have at least 1 arguments")
      else:
         if len(args) == 0:
            raise Exception("Must have at least 1 arguments")
         else:
            tempArray = Array(*self)
            for i in args:
               if type(i) in (list,tuple,Array):
                  for c in i:
                     tempArray.append(c)
               else:
                  tempArray.append(i)
            return tempArray
   def every(self, callback:callable):
      """
      Executes a test function on each item in the array until an item is reached that returns False for the specified function. You use this method to determine whether all items in an array meet a criterion, such as having values less than a particular number.
      Parameters:
         callback:Function — The function to run on each item in the array. This function can contain a simple comparison (for example, item < 20) or a more complex operation, and is invoked with three arguments; the value of an item, the index of an item, and the Array object:
         - function callback(item:*, index:int, array:Array)
      Returns:
         Boolean — A Boolean value of True if all items in the array return True for the specified function; otherwise, False.
      """
      #for i in range(0,len(self)):
      #   if callback(self[i], i, self) == False:
      #      return False
      #return True
      tempBool = True
      for i in range(0,len(self)):
         if callback(self[i], i, self) == False:
            tempBool = False
            break
      return tempBool
   def filter(self, callback:callable):
      """
      Executes a test function on each item in the array and constructs a new array for all items that return True for the specified function. If an item returns False, it is not included in the new array.
      Parameters:
         callback:Function — The function to run on each item in the array. This function can contain a simple comparison (for example, item < 20) or a more complex operation, and is invoked with three arguments; the value of an item, the index of an item, and the Array object:
         - function callback(item:*, index:int, array:Array)
      Returns:
         Array — A new array that contains all items from the original array that returned True. 
      """
      tempArray = Array()
      for i in range(0,len(self)):
         if callback(self[i], i, self) == True:
            tempArray.push(self[i])
      return tempArray
   def forEach(self, callback:callable):
      """
      Executes a function on each item in the array.
      Parameters:
         callback:Function — The function to run on each item in the array. This function can contain a simple command (for example, a trace() statement) or a more complex operation, and is invoked with three arguments; the value of an item, the index of an item, and the Array object:
         - function callback(item:*, index:int, array:Array)
      """
      for i in range(0, len(self)):
         self[i] = callback(self[i], i, self)
   def indexOf(self, searchElement, fromIndex:Union[builtins.int,int]=0):
      """
      Searches for an item in an array using == and returns the index position of the item.
      Parameters:
         searchElement — The item to find in the array.
         fromIndex:int (default = 0) — The location in the array from which to start searching for the item.
      Returns:
         index:int — A zero-based index position of the item in the array. If the searchElement argument is not found, the return value is -1.
      """
      index = -1
      if fromIndex < 0:
         fromIndex = 0
      for i in range(fromIndex,len(self)):
         if self[i] == searchElement:
            index = i
            break
      return index
   def insertAt(self, index:Union[builtins.int,int], element):
      """
      Insert a single element into an array.
      Parameters
	      index:int — An integer that specifies the position in the array where the element is to be inserted. You can use a negative integer to specify a position relative to the end of the array (for example, -1 is the last element of the array).
	      element — The element to be inserted.
      """
      #can possibly be replaced with just self.insert(index,element) but this is slightly different than current
      #current inserts from end if negative while insert acts like the array is reversed
      if index < 0:
         self.insert((len(self) + index), element)
      else:
         self.insert(index, element)
   def _denest(self, array):
      tempA = []
      for i in array:
         if type(i) in (list,tuple,Array):
            tempA.extend(self._denest(i))
         else:
            tempA.append(i)
      return tempA
   def join(self, sep:Union[str,String]=","):
      """
      Converts the elements in an array to strings, inserts the specified separator between the elements, concatenates them, and returns the resulting string. A nested array is always separated by a comma (,), not by the separator passed to the join() method.
      Parameters:
	      sep (default = ",") — A character or string that separates array elements in the returned string. If you omit this parameter, a comma is used as the default separator.
      Returns:
	      String — A string consisting of the elements of an array converted to strings and separated by the specified parameter.
      """
      result = ""
      for i in range(0, len(self)):
         if type(self[i]) in (list,tuple,Array):
            temp = self._denest(self[i])
            for j in range(0,len(temp)):
               if j == len(temp) - 1:
                  if i == len(self) - 1:
                     result += f"{temp[j]}"
                  else:
                     result += f"{temp[j]}{sep}"
               else:
                  result += f"{temp[j]},"
         elif i != len(self) - 1:
            result += f"{self[i]}{sep}"
         else:
            result += f"{self[i]}"
      return result
   def lastIndexOf(self, searchElement, fromIndex:Union[builtins.int,int]=None):
      """
      Searches for an item in an array, working backward from the last item, and returns the index position of the matching item using ==.
      Parameters:
	      searchElement — The item to find in the array.
	      fromIndex:int (default = 99*10^99) — The location in the array from which to start searching for the item. The default is the maximum value allowed for an index. If you do not specify fromIndex, the search starts at the last item in the array.
      Returns:
	      int — A zero-based index position of the item in the array. If the searchElement argument is not found, the return value is -1.
      """
      if fromIndex == None:
         fromIndex = 0
      elif fromIndex < 0:
         RangeError(f"Array.lastIndexOf; fromIndex can not be less than 0, fromIndex is {fromIndex}")
      tempA = Array(*self).reverse()
      index = tempA.indexOf(searchElement,fromIndex)
      if index == -1:
         return index
      else:
         return len(self) - 1 - index
   def map(self, callback:callable):
      """
      Executes a function on each item in an array, and constructs a new array of items corresponding to the results of the function on each item in the original array.
      Parameters:
         callback:Function — The function to run on each item in the array. This function can contain a simple command (such as changing the case of an array of strings) or a more complex operation, and is invoked with three arguments; the value of an item, the index of an item, and the Array object:
         - function callback(item:*, index:int, array:Array)
      Returns:
         Array — A new array that contains the results of the function on each item in the original array.
      """
      output = Array()
      for i in range(0,len(self)):
         output.push(callback(self[i], i, self))
      return output
   def pop(self):
      """
      Removes the last element from an array and returns the value of that element.
      Returns:
         * — The value of the last element (of any data type) in the specified array.
      """
      return super().pop(-1)
   def push(self, *args):
      """
      Adds one or more elements to the end of an array and returns the new length of the array.
      Parameters:
         *args — One or more values to append to the array.
      """
      for i in args:
         self.append(i)
   def removeAt(self, index:Union[builtins.int,int]):
      """
      Remove a single element from an array. This method modifies the array without making a copy.
      Parameters:
	      index:int — An integer that specifies the index of the element in the array that is to be deleted. You can use a negative integer to specify a position relative to the end of the array (for example, -1 is the last element of the array).
      Returns:
	      * — The element that was removed from the original array.
      """
      return super().pop(index)
   def reverse(self):
      """
      Reverses the array in place.
      Returns:
	      Array — The new array.
      """
      super().reverse()
      return self
   def shift(self):
      """
      Removes the first element from an array and returns that element. The remaining array elements are moved from their original position, i, to i-1.
      Returns:
         * — The first element (of any data type) in an array. 
      """
      return super().pop(0)
   def slice(self, startIndex:Union[builtins.int,int]=0, endIndex:Union[builtins.int,int]=99*10^99):
      #!implement negative indicies
      """
      Returns a new array that consists of a range of elements from the original array, without modifying the original array. The returned array includes the startIndex element and all elements up to, but not including, the endIndex element.
      If you don't pass any parameters, the new array is a duplicate (shallow clone) of the original array.
      Parameters:
         startIndex:int (default = 0) — A number specifying the index of the starting point for the slice. If startIndex is a negative number, the starting point begins at the end of the array, where -1 is the last element.
         endIndex:int (default = 99*10^99) — A number specifying the index of the ending point for the slice. If you omit this parameter, the slice includes all elements from the starting point to the end of the array. If endIndex is a negative number, the ending point is specified from the end of the array, where -1 is the last element.
      Returns:
         Array — An array that consists of a range of elements from the original array.
      """
      
      result = Array()
      if startIndex < 0:
         startIndex = len(self) + startIndex
      if endIndex < 0:
         endIndex = len(self) + endIndex
      if endIndex > len(self):
         endIndex = len(self)
      i = startIndex
      while i < endIndex:
         result.push(self[i])
         i += 1
      return result
   def some(self, callback:callable):
      """
      Executes a test function on each item in the array until an item is reached that returns True. Use this method to determine whether any items in an array meet a criterion, such as having a value less than a particular number.
      Parameters:
         callback:Function — The function to run on each item in the array. This function can contain a simple comparison (for example item < 20) or a more complex operation, and is invoked with three arguments; the value of an item, the index of an item, and the Array object:
         - function callback(item:*, index:int, array:Array)
      Returns:
         Boolean — A Boolean value of True if any items in the array return True for the specified function; otherwise False.
      """
      tempBool = False
      for i in range(0,len(self)):
         if callback(self[i], i, self) == True:
            tempBool == True
            break
      return tempBool
   def sort(self, sortOptions=0, pythonsort=False):
      """
      """
      if pythonsort == True:
         super().sort()
      else:
         match sortOptions:
            case 0:
               raise Exception("Not yet implemented")
            case 1:
               raise Exception("Not yet implemented")
            case 2:
               raise Exception("Not yet implemented")
            case 4:
               raise Exception("Not yet implemented")
            case 8:
               raise Exception("Not yet implemented")
            case 16:
               super().sort()
   def sortOn():
      pass
   def splice(self, startIndex:Union[builtins.int,int], deleteCount:Union[builtins.int,int], *values):
      """
      Adds elements to and removes elements from an array. This method modifies the array without making a copy.
      Parameters:
	      startIndex:int — An integer that specifies the index of the element in the array where the insertion or deletion begins. You can use a negative integer to specify a position relative to the end of the array (for example, -1 is the last element of the array).
	      deleteCount:int — An integer that specifies the number of elements to be deleted. This number includes the element specified in the startIndex parameter. If you do not specify a value for the deleteCount parameter, the method deletes all of the values from the startIndex element to the last element in the array. If the value is 0, no elements are deleted.
	      *values — An optional list of one or more comma-separated values to insert into the array at the position specified in the startIndex parameter. If an inserted value is of type Array, the array is kept intact and inserted as a single element. For example, if you splice an existing array of length three with another array of length three, the resulting array will have only four elements. One of the elements, however, will be an array of length three.
      Returns:
	      Array — An array containing the elements that were removed from the original array. 
      """
      removedValues = Array()
      i = deleteCount
      if startIndex < 0:
         startIndex = len(self) + startIndex
      while i > 0:
         removedValues.push(self[startIndex])
         self.removeAt(startIndex)
         i -= 1
      if len(values) > 0:
         for i in range(0,len(values)):
            self.insertAt(startIndex + i, values[i])
      return removedValues
   def toList(self):
      return list(self)
   def toLocaleString(self):
      """
      Returns a string that represents the elements in the specified array. Every element in the array, starting with index 0 and ending with the highest index, is converted to a concatenated string and separated by commas. In the ActionScript 3.0 implementation, this method returns the same value as the Array.toString() method.
      Returns:
	      String — A string of array elements. 
      """
      return self.toString()
   def toString(self, formatLikePython:Union[bool,Boolean]=False):
      """
      Returns a string that represents the elements in the specified array. Every element in the array, starting with index 0 and ending with the highest index, is converted to a concatenated string and separated by commas. To specify a custom separator, use the Array.join() method.
      Returns:
	      String — A string of array elements. 
      """
      if formatLikePython == True:
         return str(self)
      else:
         a = ""
         for i in range(0, len(self)):
            if i == len(self) - 1:
               a += f"{self[i]}"
            else:
               a += f"{self[i]},"
         return a
   def unshift(self, *args):
      """
      Adds one or more elements to the beginning of an array and returns the new length of the array. The other elements in the array are moved from their original position, i, to i+1.
      Parameters:
	      *args — One or more numbers, elements, or variables to be inserted at the beginning of the array.
      Returns:
	      int — An integer representing the new length of the array.
      """
      tempArray = [*args,*self]
      self.clear()
      self.extend(tempArray)
      return len(self)
class Boolean:
   """
   Lets you create boolean object similar to ActionScript3
   Since python is case sensitive the values are "True" or "False" instead of "true" or "false"
   """
   __slots__ = ("bool")
   def __init__(self, expression=False):
      self.bool = self.Boolean(expression)
   def __str__(self):
      return f'{self.bool}'
   def __getitem__(self):
      return self.bool
   def __setitem__(self, value):
      self.bool = value
   def Boolean(self, expression, strrepbool:Union[bool,Boolean]=False):
      match typeName(expression):
         case "bool":
            return expression
         case "Boolean":
            return expression.value
         case "int" | "float" | "uint" | "Number":
            if expression == 0:
               return False
            else:
               return True
         case "NaN":
            return False
         case "str" | "String":
            match expression:
               case "false":
                  if strrepbool == True:
                     return False
                  else:
                     return True
               case "true":
                  return True
               case "":
                  return False
               case _:
                  return True
         case "null":
            return False
         case "undefined":
            return False
   def toString(self, formatLikePython:Union[bool,Boolean]=False):
      if formatLikePython == True:
         return f"{self.bool}"
      else:
         return f"{self.bool}".lower()
   def valueOf(self):
      if self.bool == True:
         return True
      else:
         return False
class Date:
   def __init__(self, time=time()):
      self.time = time
      #self.date
      #self.dateUTC
      #self.day
      #self.dayUTC
      #self.fullYear
      #self.fullYearUTC
      #self.hours
      #self.hoursUTC
      #self.milliseconds
      #self.millisecondsUTC
      #self.minutes
      #self.minutesUTC
      #self.month
      #self.monthUTC
      #self.seconds
      #self.secondsUTC
      self._tz = str(strftime('%Z%z'))
      self.timezoneOffset = self._getcurrenttzoffset()
   def __str__(self):
      #returns dayoftheweek month dayofmonth time timezone year
      pass
   def __repr__(self):
      return self.time
   def _getcurrenttzoffset(self):
      #Returns difference in minutes between local and UTC
      i1 = self._tz.find("-")
      if i1 == -1:
         i1 = self._tz.find("+")
         if i1 == -1:
            return 0
         else:
            signmult = 1
            l1 = self._tz.split("+")
      else:
         signmult = -1
         l1 = self._tz.split("-")
      l2 = wrap(l1[1],1)
      hours = builtins.int(l2.pop(0) + l2.pop(0))
      minutes = builtins.int(l2.pop(0) + l2.pop(0))
      return (hours * 60 + minutes) * signmult
   def Date():
      pass
   def getDate():
      pass
   def getDay():
      pass
   def getFullYear():
      pass
   def getHours():
      pass
   def getMilliseconds():
      pass
   def getMinutes():
      pass
   def getMonth():
      pass
   def getSeconds():
      pass
   def getTime():
      pass
   def getTimezoneOffset():
      pass
   def getUTCDate():
      pass
   def getUTCDay():
      pass
   def getUTCFullYear():
      pass
   def getUTCHours():
      pass
   def getUTCMilliseconds():
      pass
   def getUTCMinutes():
      pass
   def GetUTCMonth():
      pass
   def getUTCSeconds():
      pass
   def parse():
      pass
   def setDate():
      pass
   def setFullYear():
      pass
   def setHours():
      pass
   def setMilliseconds():
      pass
   def setMinutes():
      pass
   def setMonth():
      pass
   def setSeconds():
      pass
   def setTime():
      pass
   def setUTCDate():
      pass
   def setUTCFullYear():
      pass
   def setUTCHours():
      pass
   def setUTCMilliseconds():
      pass
   def setUTCMinutes():
      pass
   def setUTCMonth():
      pass
   def setUTCSeconds():
      pass
   def toDateString():
      pass
   def toJSON():
      pass
   def toLocaleDateString():
      pass
   def toLocaleString():
      pass
   def toLocaleTimeString():
      pass
   def toString():
      pass
   def toTimeString():
      pass
   def toUTCString():
      pass
   def UTC():
      pass
   def valueOf(self):
      return self.time
class DefinitionError():
   __slots__ = ("error")
   def __init__(self, message=""):
      trace(type(self), message, isError=True)
      self.error = message
def decodeURI():
   pass
def decodeURIComponent():
   pass
def encodeURI():
   pass
def encodeURIComponent():
   pass
class Error():
   __slots__ = ("error")
   def __init__(self, message=""):
      trace(type(self), message, isError=True)
      self.error = message
def escape():
   """
   Converts the parameter to a string and encodes it in a URL-encoded format, where most nonalphanumeric characters are replaced with % hexadecimal sequences. When used in a URL-encoded string, the percentage symbol (%) is used to introduce escape characters, and is not equivalent to the modulo operator (%). 
   The following characters are not converted to escape sequences by the escape() function.
   0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ@-_.*+/
   """
   pass
class EvalError():
   __slots__ = ("error")
   def __init__(self, message=""):
      trace(type(self), message, isError=True)
      self.error = message
class int:
   __slots__ = ("value")
   MAX_VALUE = 2147483647
   MIN_VALUE = -2147483648
   def __init__(self, value):
      self.value = self._int(value)
   def __str__(self):
      return f'{self.value}'
   def __getitem__(self):
      return self.value
   def __setitem__(self, value):
      self.value = self._int(value)
   def __add__(self, value):
      return int(self.value + self._int(value))
   def __sub__(self, value):
      return int(self.value - self._int(value))
   def __mul__(self, value):
      return int(self.value * self._int(value))
   def __truediv__(self, value):
      if value == 0:
         if self.value == 0:
            return NaN()
         elif self.value > 0:
            return Infinity()
         elif self.value < 0:
            return NInfinity()
      else:
         try:
            return int(self.value / self._int(value))
         except:
            raise TypeError(f"Can not divide int by {type(value)}")
   def __float__(self):
      return float(self.value)
   def __int__(self):
      return self.value
   def _int(self, value):
      match typeName(value):
         case "NaN" | "Infinity" | "NInfinity":
            return value
         case "int":
            return value
         case "float" | "Number":
            return builtins.int(value)
         case "str" | "String":
            try:
               return builtins.int(value)
            except:
               raise TypeError(f"Can not convert string {value} to integer")
         case _:
            raise TypeError(f"Can not convert type {type(value)} to integer")
   def toExponential(self, fractionDigits:Union[builtins.int,int]):
      if fractionDigits < 0 or fractionDigits > 20:
         RangeError("fractionDigits is outside of acceptable range")
      else:
         tempString1 = f"{self.value}"
         exponent = len(tempString1) - 1
         if tempString1[0] == "-":
            exponent -= 1
            tempString2 = tempString1[:2]
            tempString1 = tempString1[2:]
         else:
            tempString2 = tempString1[:1]
            tempString1 = tempString1[1:]
         if fractionDigits > 0:
            tempString2 += "."
            for i in range(0,fractionDigits):
               try:
                  tempString2 += tempString1[i]
               except:
                  tempString2 += "0" #I am assuming this is what it does since it isn't supposed to throw another error
         if exponent > 0:
            tempString2 += f"e+{exponent}"
         return tempString2
   def toFixed(self, fractionDigits:Union[builtins.int,int]):
      if fractionDigits < 0 or fractionDigits > 20:
         RangeError("fractionDigits is outside of acceptable range")
      else:
         tempString = f"{self.value}"
         if fractionDigits == 0:
            return tempString
         else:
            tempString += "."
            i = 0
            while i < fractionDigits:
               tempString += "0"
               i += 1
            return tempString
   def toPrecision(self,precision:Union[builtins.int,int,uint]):
      if precision < 1 or precision > 21:
         RangeError("fractionDigits is outside of acceptable range")
      tempString = f"{self.value}"
      len_ = len(tempString)
      if precision < len_:
         return toExponential(precision-1)
      elif precision == len_:
         return tempString
      else:
         tempString += "."
         for i in range(0,precision-len_):
            tempString += "0"
         return tempString
   def toString(self, radix:Union[builtins.int,int,uint]=10):
      if radix > 36 or radix < 2:
         pass
      else:
         return base_repr(self.value, base=radix)
   def valueOf(self):
      return self.value
def isFinite(num):
   if num in (inf,NINF,NaN) or typeName(num) in ("NInfinity","Infinity","NaN"):
      return False
   else:
      return True
def isNaN(num):
   if num == nan or typeName(num) == "NaN":
      return True
   else:
      return False
def isXMLName(str_:Union[str,String]):
   #currently this is spec compatible with the actual xml specs but unknown if it is the same as the actionscript function.
   whitelist = "-_."
   if (len(str_) == 0) or (str_[0].isalpha() == False and str_[0] != "_") or (str_[:3].lower() == "xml") or (str_.find(" ") != -1):
      return False
   for i in str_:
      if i.isalnum() == True or i in whitelist:
         continue
      return False
   return True
class JSON:
   def parse():
      pass
   def stringify():
      pass
class Math:
   __slots__ = ()
   E = 2.71828182845905
   LN10 = 2.302585092994046
   LN2 = 0.6931471805599453
   LOG10E = 0.4342944819032518
   LOG2E = 1.442695040888963387
   PI = 3.141592653589793
   SQRT1_2 = 0.7071067811865476
   SQRT2 = 1.4142135623730951
   def abs(val):
      return abs(val)
   def acos(val):
      return m.acos(val)
   def asin(val):
      return m.asin(val)
   def atan(val):
      return m.atan(val)
   def atan2(y, x):
      return m.atan2(y,x)
   def ceil(val):
      return m.ceil(val)
   def cos(angleRadians):
      return m.cos(angleRadians)
   def exp(val):
      return m.exp(val)
   def floor(val):
      return m.floor(val)
   def log(val):
      return m.log(val)
   def max(*values):
      if len(values) == 1:
         return values[0]
      else:
         return max(values)
   def min(*values):
      if len(values) == 1:
         return values[0]
      else:
         return min(values)
   def pow(base, power):
      return m.pow(base,power)
   def random():
      return r.random()
   def round(val):
      return round(val)
   def sin(angleRadians):
     return m.sin(angleRadians)
   def sqrt(val):
      return m.sqrt(val)
   def tan(angleRadians):
      return m.tan(angleRadians)
class Namespace:
   def __init__():
      pass
   def toString():
      pass
   def valueOf():
      pass
class Number:
   __slots__ = ("number")
   MAX_VALUE = 1.79e308
   MIN_VALUE = 5e-324
   NaN = NaN()
   NEGATIVE_INFINITY = NInfinity()
   POSITIVE_INFINITY = Infinity()
   def __init__(self, num=None):
      self.number = self._Number(num)
   def __str__(self):
      if self.number in (NaN(),Infinity(),NInfinity()):
         return str(self.number)
      if self.number.is_integer() == True:
         return f'{builtins.int(self.number)}'
      return f'{self.number}'
   def __getitem__(self):
      return self.number
   def __setitem__(self, value):
      self.number = self._Number(value)
   def __add__(self, value):
      try:
         return Number(self.number + float(value))
      except ValueError:
         raise TypeError(f"can not add {type(value)} to Number")
   def __sub__(self, value):
      try:
         return Number(self.number - float(value))
      except ValueError:
         raise TypeError(f"can not subtract {type(value)} from Number")
   def __mul__(self, value):
      try:
         return Number(self.number * float(value))
      except ValueError:
         raise TypeError(f"can not multiply Number by {type(value)}")
   def __truediv__(self, value):
      if value == 0:
         if self.number == 0:
            return Number(NaN())
         elif self.number > 0:
            return Number(Infinity())
         elif self.number < 0:
            return Number(NInfinity())
      else:
         try:
            return Number(self.number / float(value))
         except:
            raise TypeError(f"Can not divide Number by {type(value)}")
   def __float__(self):
      return float(self.number)
   def __int__(self):
      return builtins.int(self.number)
   def _Number(self, expression):
      tpexp = type(expression)
      if expression == NInfinity():
         return NInfinity()
      elif expression == Infinity():
         return Infinity()
      elif expression in (None,NaN()):
         return NaN()
      elif tpexp in (builtins.int,int):
         return float(expression)
      elif tpexp in (float,Number):
         return expression
      elif expression == "undefined":
         return NaN()
      elif expression == "null":
         return 0.0
      elif expression == self.NaN:
         return self.NaN
      elif tpexp in (bool,Boolean):
         if expression == True:
            return 1.0
         else:
            return 0.0
      elif tpexp in (str,String):
         if expression == "":
            return 0.0
         else:
            try:
               return float(expression)
            except:
               return NaN()
   def toExponential(self):
      pass
   def toFixed(self):
      pass
   def toPrecision():
      pass
   def toString(self, radix=10):
      #!
      return str(self.number)
   def valueOf(self):
      return self.number
def parseFloat(str_:Union[str,String]):
   if str_[0].isspace() == True:
      while str_[0].isspace() == True:
         str_ = str_[1:]
   if str_[0].isdigit() == True:
      tempstr = String()
      for i in str_:
         if i.isdigit() != True and i != ".":
            break
         tempstr += i
      return Number(tempstr)
   else:
      return NaN()
def parseInt(str_:Union[str,String],radix:Union[int,uint]=0):
   if radix < 2 or radix > 36:
      trace("parseInt",f"radix {radix} is outside of the acceptable range",isError=True)
      pass
   if str_[0].isspace() == True:
      while str_[0].isspace() == True:
         str_ = str_[1:]
   if len(str_) >= 2 and f"{str_[0]}{str_[1]}" == "0x":
      radix = 16
      str_ = str_[2:]
   if len(str_) >= 1 and str_[0] == "0":
      while str[0] == "0":
         str_ = str_[1:]
   radixchars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:radix]
   str_ = str_.upper()
   tempstr = String()
   for i in str_:
      if i not in radixchars:
         break
      tempstr += i
   return int(builtins.int(tempstr,radix))
class QName:
   def __init__():
      pass
   def toString():
      pass
   def valueOf():
      pass
class RangeError():
   __slots__ = ("error")
   def __init__(self, message=""):
      trace(type(self), message, isError=True)
      self.error = message
class ReferenceError():
   __slots__ = ("error")
   def __init__(self, message=""):
      trace(type(self), message, isError=True)
      self.error = message
class RegExp:
   pass
class SecurityError():
   __slots__ = ("error")
   def __init__(self, message=""):
      trace(type(self), message, isError=True)
      self.error = message
class String(str):
   def __init__(self, value=""):
      self._hiddeninit(self._String(value))
   def _hiddeninit(self, value):
      super().__init__()
   def _getLength(self):
      return len(self)
   length = property(fget=_getLength)
   def _String(self, expression):
      match typeName(expression):
         case "str" | "String":
            return expression
         case "bool":
            if expression == True:
               return "true"
            elif expression == False:
               return "false"
         case "NaN":
            return "NaN"
         case "Array" | "Boolean" | "Number":
            return expression.toString()
         case _:
            return f"{expression}"
   def __add__(self, value):
      return String(f"{self}{self._String(value)}")
   def __iadd__(self, value):
      return String(f"{self}{self._String(value)}")
   def charAt(self, index:Union[builtins.int,int]=0):
      if index < 0 or index > len(self) - 1:
         return ""
      else:
         return self[index]
   def charCodeAt(self, index:Union[builtins.int,int]=0):
      if index < 0 or index > len(self) - 1:
         return NaN()
      else:
         return r'\u{:04X}'.format(ord(self[index]))
   def concat(self, *args):
      tempString = String(self)
      for i in args:
         tempString += self._String(i)
      return tempString
   def fromCharCode():
      pass
   def indexOf(self, val, startIndex:Union[builtins.int,int]=0):
      return self.find(val, startIndex)
   def lastIndexOf(self, val, startIndex:Union[builtins.int,int]=None):
      tempInt = len(self)
      if startIndex == None or startIndex > tempInt:
         return self.rfind(val,0,tempInt)
      else:
         return self.rfind(val,0,startIndex)
   def localeCompare():
      pass
   def match():
      pass
   def replace():
      pass
   def search():
      pass
   def slice(self,startIndex=0,endIndex=None):
      #!
      """
      rtl = False
      if endIndex == None:
         endIndex = len(self)
      if startIndex < 0:
         rtl = True
         startIndex = len(self) + startIndex
      if endIndex < 0:
         endIndex = len(self) + endIndex
      """
      pass
   def split():
      pass
   def substr(self, startIndex:Union[builtins.int,int]=0, Len:Union[builtins.int,int]=None):
      tempInt = len(self)
      if startIndex > tempInt - 1:
         return String()
      if startIndex < 0:
         if startIndex > abs(tempInt) - 1:
            startIndex = 0
         else:
            startIndex = tempInt + startIndex
      if Len == None:
         Len = tempInt
      tempString = String()
      for i in range(startIndex, startIndex + Len):
         try:
            tempString += self[i]
         except:
            break
      return tempString
   def substring(self, startIndex:Union[builtins.int,int]=0, endIndex:Union[builtins.int,int]=None):
      tempInt = len(self)
      if startIndex < 0:
         startIndex = 0
      if endIndex != None:
         if endIndex < 0:
            endIndex = 0
         elif endIndex > tempInt:
            endIndex = tempInt
      else:
         endIndex = tempInt
      if startIndex > endIndex:
         temp = startIndex
         startIndex = endIndex
         endIndex = temp
      tempString = String()
      for i in range(startIndex,endIndex):
         tempString += self[i]
      return tempString
   def toLocaleLowerCase(self):
      return self.toLowerCase()
   def toLocaleUpperCase(self):
      return self.toUpperCase()
   def toLowerCase(self):
      return self.lower()
   def toUpperCase(self):
      return self.upper()
   def valueOf(self):
      return f"{self}"
class SyntaxError():
   __slots__ = ("error")
   def __init__(self, message=""):
      trace(type(self), message, isError=True)
      self.error = message
def trace(*args, isError=False):
   if configmodule.as3DebugEnable == True:
      if isError == True and configmodule.ErrorReportingEnable == 1:
         if configmodule.MaxWarningsReached == False:
            if configmodule.CurrentWarnings < configmodule.MaxWarnings or configmodule.MaxWarnings == 0:
               output = f"Error:{formatTypeToName(args[0])}; {args[1]}"
               configmodule.CurrentWarnings += 1
            else:
               output = "Maximum number of errors has been reached. All further errors will be suppressed."
               configmodule.MaxWarningsReached = True
         else:
            pass
      else:
         output = ""
         if len(args) == 1:
            output = f"{args[0]}"
         else:
            for i in range(0, len(args)):
               if i == len(args) - 1:
                  output += f"{args[i]}"
               else:
                  output += f"{args[i]} "
      if configmodule.TraceOutputFileEnable == 1:
         if configmodule.TraceOutputFileName == configmodule.defaultTraceFilePath:
            if Path(configmodule.TraceOutputFileName).exists() == True:
               with open(configmodule.TraceOutputFileName, "r") as f:
                  tempread = f.read()
               with open(configmodule.TraceOutputFileName, "w") as f:
                  output = f"{tempread}{output}\n" 
                  f.write(output)
            else:
               with open(configmodule.TraceOutputFileName, "w") as f:
                  output += "\n" 
                  f.write(output)
         else:
            if Path(configmodule.TraceOutputFileName).exists() == True:
               if Path(configmodule.TraceOutputFileName).is_file() == True:
                  with open(configmodule.TraceOutputFileName, "r") as f:
                     tempread = f.read()
                  with open(configmodule.TraceOutputFileName, "w") as f:
                     output = f"{tempread}{output}\n"
                     f.write(output)
            else:
               with open(configmodule.TraceOutputFileName, "w") as f:
                  output += "\n"
                  f.write(output)
      else:
         print(output)
class TypeError():
   __slots__ = ("error")
   def __init__(self, message=""):
      trace(type(self), message, isError=True)
      self.error = message
class U29:
   def decodeU29int(type_, data):
      """
      Must have an input of the data type ("h" or "b" for hexidecimal or binary) and the data as a string.
      Binary data must be either 8, 16, 32, or 48 bits.
      The first bit if each byte, aside from the 4th, determines if there is another byte afterwards (1xxxxxxx means there is another). This leaves a maximum of 29 bits for actual data, hence u29int.
      The specs of u29int can be found at https://web.archive.org/web/20080723120955/http://download.macromedia.com/pub/labs/amf/amf3_spec_121207.pdf on page 3
      This function returns a list. Value 0 is the number it translates to, value 1 is the type of u29int value (1, 2, 3, or 4). The types basically mean how many bytes the u29int was (this is a part of the spec)
      """
      data = data.replace(" ", "")
      r = ""
      if type_ == "h":
         bindat = bin(builtins.int(data, 16))[2:].zfill(len(data) * 4)
      elif type_ == "b":
         bindat = data
      else:
         trace("U29Error; Wrong type",isError=True)
      if bindat[0] == "1":
         if bindat[8] == "1":
            if bindat[16] == "1":
               rtype = 4
               for i in range(0,32):
                  if i not in (0,8,16):
                     r += bindat[i]
               result = builtins.int(r,2)
            else:
               rtype = 3
               for i in range(0,24):
                  if i not in (0,8,16):
                     r += bindat[i]
               result = builtins.int(r,2)
         else:
            rtype = 2
            for i in range(0,16):
               if i not in (0,8):
                  r += bindat[i]
            result = builtins.int(r,2)
      else:
         rtype = 1
         for i in range(0,8):
            if i != 0:
               r += bindat[i]
         result = builtins.int(r,2)
      return [result, rtype]
   def decodeU29str(_type, data):
      """
      Must have an input of the data type ("h" or "b" for hexidecimal or binary) and the data as a string.
      A u29str value is an encoded string which is preceded by (a) u29str length byte(s).
      The u29str length byte(s) is, in all the cases I've seen, the length in bits of the string times 2 plus 1 (for some stupid reason).
      """
      dat = data.replace(" ", "")
      if _type == "h":
         bindat = bin(builtins.int(dat, 16))[2:].zfill(len(dat) * 4)
         x=0
      elif _type == "b":
         bindat = dat
      length1 = u29._decodeU29str(bindat)
      temp = u29.read_byte_destructive(bindat)
      bindat = temp[0]
      length = builtins.int((length1[0] - 1) / 2)
      result = ''
      for i in range(0, length):
         temp = u29.read_byte_destructive(bindat)
         bindat = temp[0]
         result += bytes.fromhex('%0*X' % ((len(temp[1]) + 3) // 4, builtins.int(temp[1], 2))).decode('utf-8')
      return result
   def read_byte_destructive(binary_data):
      temp = u29.remove_byte(binary_data)
      return temp[0], temp[1]
   def remove_byte(binary_data):
      temp1 = wrap(binary_data, 8)
      temp2 = temp1.pop(0)
      temp1 = ''.join(temp1)
      return temp1, temp2
   def _decodeU29str(binary_data):
      numlist = binary_data.replace(" ", "")
      numlist = numlist[:32]
      r = ""
      if numlist[0] == '1':
         if numlist[1] == '1':
            if numlist[2] == '1':
               if numlist[3] == '1':
                  for i in range(0,16):
                     #if i == 0 or i == 1 or i == 2 or i == 3 or i == 4 or i == 8 or i == 9 or i == 16 or i == 17 or i == 24 or i == 25:
                     if i in (0,1,2,3,4,8,9,16,17,24,25):
                        continue
                     else:
                        r += numlist[i]
                  number = builtins.int(r,2)
                  return [number,4]
               else:
                  for i in range(0,16):
                     #if i == 0 or i == 1 or i == 2 or i == 3 or i == 8 or i == 9 or i == 16 or i == 17:
                     if i in (0,1,2,3,8,9,16,17):
                        continue
                     else:
                        r += numlist[i]
                  number = builtins.int(r,2)
                  return [number,3]
            else:
               for i in range(0,16):
                  #if i == 0 or i == 1 or i == 2 or i == 8 or i == 9:
                  if i in (0,1,2,8,9):
                     continue
                  else:
                     r += numlist[i]
               number = builtins.int(r,2)
               return [number,2]
         else:
            raise Exception("Not U29 string/utf-8 value")
      else:
         for i in range(0,8):
            if i != 0:
               r += numlist[i]
         number = builtins.int(r,2)
         return [number,1]
class uint:
   pass
def unescape():
   pass
class URIError():
   __slots__ = ("error")
   def __init__(self, message=""):
      trace(type(self), message, isError=True)
      self.error = message
class Vector: #probably should have list as parent
   def __init__(self,type,sourceArray:Union[list,tuple,Array,Vector]):
      pass
   def _getFixed(self):
      return self._fixed
   def _setFixed(self,value:Union[bool,Boolean]):
      self._fixed = Boolean(value)
   fixed = property(fget=_getFixed,fset=_setFixed)
   def _getLength(self):
      pass
   def _setLength(self,value):
      pass
   length = property(fget=_getLength,fset=_setLength)
   def concat():
      pass
   def every():
      pass
   def filter():
      pass
   def forEach():
      pass
   def indexOf():
      pass
   def insertAt():
      pass
   def join():
      pass
   def lastIndexOf():
      pass
   def map():
      pass
   def pop():
      pass
   def push():
      pass
   def removeAt():
      pass
   def reverse():
      pass
   def shift():
      pass
   def slice():
      pass
   def some():
      pass
   def sort():
      pass
   def splice():
      pass
   def toLocaleString():
      pass
   def toString():
      pass
   def unshift():
      pass
class VerifyError():
   __slots__ = ("error")
   def __init__(self, message=""):
      trace(type(self), message, isError=True)
      self.error = message

def EnableDebug():
   """
   Enables 'debug mode' for this module. This is a substitute for have an entire separate interpreter.
   If you want to automatically enable debug mode based on the commandline arguements of a file, do something like:
   if __name__ == "__main__":
      import sys.argv
      if "-debug" in sys.argv:
         <this module>.EnableDebug()
   """
   configmodule.as3DebugEnable = True
def DisableDebug():
   configmodule.as3DebugEnable = False
def listtoarray(l:Union[list, tuple]):
   """
   A function to convert a python list to an Array.
   """
   tempArray = Array()
   for i in l:
      tempArray.push(i)
   return tempArray
def typeName(obj:object):
   return formatTypeToName(type(obj))
def formatTypeToName(arg:type):
   tempStr = f"{arg}"
   if tempStr.find(".") != -1:
      return tempStr.split(".")[-1].split("'")[0]
   else:
      return tempStr.split("'")[1]
def isEven(Num:Union[builtins.int,float,int,Number,uint,NaN,Infinity,NInfinity]):
   match typeName(Num):
      case "NaN" | "Infinity" | "NInfinity":
         return False
      case "int" | "uint":
         if Num % 2 == 0:
            return True
         else:
            return False
      case "float" | "Number":
         pass
def isOdd(Num:Union[builtins.int,float,int,Number,uint,NaN,Infinity,NInfinity]):
   match typeName(Num):
      case "NaN" | "Infinity" | "NInfinity":
         return False
      case "int" | "uint":
         if Num % 2 == 0:
            return False
         else:
            return True
      case "float" | "Number":
         pass
def _checkValidDir(dir_):
   #!check if directory is valid
   return True
def setDataDirectory(directory:Union[str,String]):
   if _checkValidDir(directory) == True:
      configmodule.appdatadirectory = directory
   else:
      Error(f"setDataDirectory; Directory {directory} not valid")