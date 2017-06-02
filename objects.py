import re
import os
from copy import deepcopy as dc
from collections import OrderedDict
from getFileList import get_files

class onething(object):
    def __init__(self, filters):
        self.filters = OrderedDict(zip([ff.name for ff in filters], filters)) 
    
    def __add__(self, other):
        if self.filters.keys() != other.filters.keys():
            raise
        for k in self.filters.keys():
            self.filters[k] += other.filters[k]
        
        return dc(self)

class counter(object):
    def __init__(self, trig, bitn, visited, passed, failed, error, name):
        self.trig = int(trig)
        self.bitn = int(bitn)
        self.visited = int(visited)
        self.passed = int(passed)
        self.failed = int(failed)
        self.error = int(error)
        self.name = name
    
    def __str__(self):
        return 'TrigReport %6d %6d %6d %6d %6d %6d %s' %(self.trig   ,
                                                         self.bitn   ,
                                                         self.visited,
                                                         self.passed ,
                                                         self.failed ,
                                                         self.error  ,
                                                         self.name   )
    
    def __add__(self, other):
        if self.name != other.name:
            raise
        
        newcounter = counter('-999',
                             '-999',
                             '-999',
                             '-999',
                             '-999',
                             '-999',
                             self.name)
        
        newcounter.trig    = self.trig  
        newcounter.bitn    = self.bitn  
        newcounter.visited = self.visited + other.visited
        newcounter.passed  = self.passed  + other.passed 
        newcounter.failed  = self.failed  + other.failed 
        newcounter.error   = self.error   + other.error  

        return newcounter

