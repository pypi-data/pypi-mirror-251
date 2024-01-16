from __future__ import annotations
import json
import logging 
import os 
import typing

AnyType = typing.Any

class NoSQL():

    def __init__(self,**kw):
        self.kw = kw 

    def get(self,key:str,default=None)-> bool | str | int | float | None: 
        ''''''
    
    def batchGet(self,keyList:list)->list:
        ''''''

    def set(self,key:str,val:bool | str | int | float):
        ''''''

    def batchSet(self,keyList:list,valList:list):
        ''''''

    def clean(self):
        ''''''


class jsonFile(NoSQL):
    '''real implementation of NoSQL'''

    def __init__(self, **kw):
        super().__init__(**kw)
        self.filePath = kw['filePath']

    def get(self,key:str,default=None):
        if os.path.exists(self.filePath):
            with open(self.filePath, "r") as f:
                try:
                    d = json.loads(f.read())
                except:
                    logging.warn(f"cannot read cache file {self.filePath}, it is not a standard json file.")
                    return default
            return d.get(key, default)
        else:
            return default
        
    def batchGet(self,keyList:list)->list:
        return [ self.get(k) for k in keyList ] 

    
    def set(self,key:str,val:bool | str | int | float):
        if os.path.exists(self.filePath):
            try:
                with open(self.filePath, "r") as f:
                    d = json.loads(f.read())
            except:
                logging.warn("load jsonFile error when set, skip it by using a new file. ")
                d = {} 
        else:
            d = {} 
        d[key] = val
        with open(self.filePath, "w") as f:
            f.write(json.dumps(d, indent=4))
        return self 
    
    def batchSet(self,keyList:list,valList:list):
        for i in range(len(keyList)):
            self.set(key=keyList[i],val=valList[i])
    

    def clean(self):
        if os.path.exists( self.filePath ):
            os.remove( self.filePath )






class CacheStore():
    '''high level, support dict and list'''

    def __init__(self,**kw):
        self.nosql = jsonFile(**kw) 

    def get(self,key:str,default=None):
        return self.nosql.get(key=key,default=default) 
    
    def set(self,key:str,val:bool | str | int | float):
        self.nosql.set(key=key,val=val) 
        return self 
    
    def batchGet(self,keyList:list)->list:
        return self.nosql.batchGet(keyList=keyList)
    
    def batchSet(self,keyList:list,valList):
        self.nosql.batchSet(keyList=keyList,valList=valList)

    def getdl(self,key,default=None)->list|dict|None:
        str = self.get(key=key) 
        if str is None:
            return default
        else:
            return json.loads(str) 
        
    def batchGetdl(self,keyList)->list:
        valList = self.batchGet(keyList=keyList)
        return [ json.loads(val) for val in valList]
        
    def setdl(self,key:str,val:list|dict):
        str = json.dumps( val ) 
        self.set(key=key,val=str) 
        return self  
    
    def batchSetdl(self,keyList,valList):
        self.batchSet( keyList=keyList,valList = [ json.dumps(val) for val in valList] )
    
    def clean(self):
        self.nosql.clean()




