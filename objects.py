import re
import os
import ROOT
from copy import deepcopy as dc
from collections import OrderedDict
from getFileList import get_files

ROOT.TH1.SetDefaultSumw2()
ROOT.gStyle.SetOptStat(0)

class onething(object):
    def __init__(self, filters):
        self.filters = OrderedDict(zip([(ff.bitn, ff.name) for ff in filters], filters))
    
    def __add__(self, other):
        if self.filters.keys() != other.filters.keys():
            raise
        for k in self.filters.keys():
            self.filters[k] += other.filters[k]
        
        return dc(self)
    
    def fillHisto(self):
        self.histo = ROOT.TH1F('modules', 'modules', len(self.filters), 0, len(self.filters))
        for k, v in self.filters.iteritems():
            self.histo.Fill(k[0], v.passed)
            self.histo.GetXaxis().SetBinLabel(k[0] + 1, v.name)
        self.histo.GetYaxis().SetTitle('events passed')

    def fillReducedHisto(self):
        self.reducedHisto = ROOT.TH1F('filters', 'filters', len(self.filters), 0, len(self.filters))
        passed = -1
        iter = 0
        for k, v in self.filters.iteritems():
            if v.passed != passed:
                self.reducedHisto.Fill(iter, v.passed)
                self.reducedHisto.GetXaxis().SetBinLabel(iter+1, v.name)
                passed = v.passed
                iter += 1
        self.reducedHisto.GetYaxis().SetTitle('events passed')
        
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
        if self.name != other.name or self.bitn != other.bitn :
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

