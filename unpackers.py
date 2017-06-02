import re
import os
from copy import deepcopy as dc
from collections import OrderedDict
from getFileList import get_files
from objects import onething, counter


def unpackTriggerReport(file, toread, dir):

    os.system('cmsStage %s/%s .' %(dir, file))
    os.system('tar -xf %s' %file)
    try:
        with open(toread) as ifile:
            content = ifile.readlines()
    except:
        print 'no file, Arr!'
        return []

    trigger_paths = []    
    for i, line in enumerate(content):
        if 'TrigReport ---------- Path   Summary ------------' in line:
            for jj in range(i+2, len(content)):
                chunks = content[jj].split()
                if not len(chunks):
                    break
                #print chunks
                trigger_paths.append(counter(chunks[1],
                                             chunks[2],
                                             chunks[3],
                                             chunks[4],
                                             chunks[5],
                                             chunks[6],
                                             chunks[7]))
    
    return trigger_paths 



def unpack(file, toread, 
           trigger = 'HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v1', 
           dir = '/store/group/phys_tau/HLT2016/NewIsoWPV2Check/HLTPhysics/NewIsoWPV2Check/160905_133544/0000/log/',
           lastlineindex = 242):
    
    #print 'copying file: %s' %file
    
    os.system('cmsStage %s/%s .' %(dir, file))
    os.system('tar -xf %s' %file)
    
    try:
        with open(toread) as ifile:
            content = ifile.readlines()
    except:
        print 'no file, Arr!'
        return []
    
    trigger_filters = []    
    for i, line in enumerate(content):
        if 'TrigReport ---------- Modules in Path: %s ------------' %trigger in line:
            for j in range(i+2, i+lastlineindex):
                chunks = content[j].split()
                #print chunks
                trigger_filters.append(counter(chunks[1],
                                               chunks[2],
                                               chunks[3],
                                               chunks[4],
                                               chunks[5],
                                               chunks[6],
                                               chunks[7]))
    
    return trigger_filters 
