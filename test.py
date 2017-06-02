import re
import os
from copy import deepcopy as dc
from collections import OrderedDict
from getFileList import get_files
from objects import onething, counter
from unpackers import unpackTriggerReport


samples = [
    ('/store/group/phys_tau/check_tau_rates_with_data_V1/HLTPhysics1/check_tau_rates_with_data_V1/170531_190919/0000/log/', 1.), # normal APE
#     ('/store/group/phys_tau/check_tau_rates_with_data_smallAPE_V1/HLTPhysics1/check_tau_rates_with_data_smallAPE_V1/170601_155445/0000/log/', 1.), # small APE
]

rates = []
filenames = []

for sample in samples:
    filenames += get_files(sample[0], pattern='*.log.tar.gz')

all_files = []
for k, file in enumerate(filenames):
    print '====> %d / %d' %(k, len(filenames))
    file = file[1:].replace('/','')
    i = int(re.findall(r'\d+', file)[0])
    #file = 'cmsRun_%d.log.tar.gz' %i
    toread = 'cmsRun-stdout-%d.log' %i
    trigger_paths = unpackTriggerReport(file, toread, dir=sample[0])
        
    if not len(trigger_paths):
        continue
    
    os.system('rm FrameworkJobReport-%d.xml' %i)
    os.system('rm cmsRun-stderr-%d.log'      %i)
    os.system('rm cmsRun-stdout-%d.log'      %i)
    os.system('rm cmsRun_%d.log.tar.gz'      %i)
    
    all_files.append(onething(trigger_paths))
        
total = all_files[0]
for ff in all_files[1:]:
    total += ff

outfile = open('rates_HLTPhysics_normalAPE.csv', 'w+')
#     outfile = open('rates_HLTPhysics_smallAPE.csv', 'w+')
for k, v in total.filters.iteritems():
    efficiency = float(v.passed)/float(v.visited)
    print >> outfile, ','.join([str(k), str(v.passed), str(v.visited), str(efficiency), str(20./1.4*266*28.5*efficiency)])
    print k,' '*(80-len(k)), v.passed, v.visited, efficiency, '\t\t', 20./1.4*266*28.5*efficiency, 'Hz'

outfile.close()

