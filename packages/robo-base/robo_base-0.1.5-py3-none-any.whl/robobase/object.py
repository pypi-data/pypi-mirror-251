#
#
# Object - primary primordal base class 
#
# (c) 2022 - 2024  Mike Knerr
#
#

import os 

class Object(object): 
     ## primordal class
     def __init__(self): 
         self._id = id(self) #dont override ever
         self._debug_flag = False
         # successive classes override these in init
         self._name="Object"
         self._desc="Object - Primary Base Object"
         self._vers="v0.01.08" # not pypi vers
         self._model = "" # more for derived classes
         self._about="About Object..."
         self._instance_name = ""
         
     # who ##
     def whoami(self):
         print(self._name,self._vers,self._model)

     def getWhoami(self):
         # space sep for now
         return str(self._name+" "+self._vers)
         #return str(self._name+" "+self._vers+" "+self._model)
                   
     def whoamiStr(self):
         return self.getWhoami()
     
#    def whoami(self):
#          if len(self._model) > 0:
#           print(self._name + " - " + self._vers +" - "+ self._model) 
#          else:
#           print(self._name + " - " + self._vers)

     # get ##
     
     def getId(self):
         return self._id
     
     def getName(self):
        return self._name

     def getDesc(self):
        return self._desc
    
     def getVersion(self):
        return self._vers
    
     def getVers(self):
        return self._vers
    
     def getAbout(self):
        return self._about
    
     def getModel(self):
        return self._model
        
     # set ##
     
     def setName(self,n):
         self._name = n
    
     def setDesc(self,d):
         self._desc = d
         
     def setAbout(self,a):
         self._about = a
    
     def setModel(self,m):
        self._model = m
    
     # not on the public inteface
     # hard code this one in derived classes
     # def setVers(self,v):
     #    self._vers =v
     
     # shell commands ##
     
     def id(self):
         print(self._id)
         
     def name(self):
          print(self._name)

     def desc(self):
          print(self._desc)
    
     def version(self):
          print(self._vers)
    
     def vers(self):
          print(self._vers)
    
     def about(self):
          print(self._about)
    
     def model(self):
          print(self._model)
          
     # debug ##   
     
     def setDebugOn(self):
         self._debug_flag = True
         
     def setDebugOff(self):
         self._debug_flag = False

     def debug(self):
         return (self._debug_flag == True) 
         
     def debugIsOn(self):
         # makes more sense w/ if debugIsOn(): then...
         return (self._debug_flag == True) #test as bool
       
     def isDebugOn(self):
         # backward compat
         return self.debugIsOn()
          
     #future rem these 2 use set*()
     #def debugOn(self):
     #    self.setDebugOn()
     
     #def debugOff(self):
     #    self.setDebugOff()
        
    

