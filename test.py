import re
import os
from copy import deepcopy as dc
from collections import OrderedDict
from getFileList import get_files
from objects import onething, counter
from unpackers import unpackTriggerReport


samples = [    
#     ('/store/group/phys_tau/Run296786/PU30to36/HLTPhysics1/minosMenuRun296786V1/170615_220501/0000/log', 1.),
#     ('/store/group/phys_tau/Run296786/PU30to36/HLTPhysics2/minosMenuRun296786V1/170615_220707/0000/log', 1.),
#     ('/store/group/phys_tau/Run296786/PU30to36/HLTPhysics3/minosMenuRun296786V1/170615_220916/0000/log', 1.),
#     ('/store/group/phys_tau/Run296786/PU30to36/HLTPhysics4/minosMenuRun296786V1/170615_221125/0000/log', 1.),
#     ('/store/group/phys_tau/Run296786/PU30to36/HLTPhysics5/minosMenuRun296786V1/170615_221346/0000/log', 1.),
#     ('/store/group/phys_tau/Run296786/PU30to36/HLTPhysics6/minosMenuRun296786V1/170615_221554/0000/log', 1.),
#     ('/store/group/phys_tau/Run296786/PU30to36/HLTPhysics7/minosMenuRun296786V1/170615_221803/0000/log', 1.),
#     ('/store/group/phys_tau/Run296786/PU30to36/HLTPhysics8/minosMenuRun296786V1/170615_222021/0000/log', 1.),

#     ('/store/group/phys_tau/Run296786/PU36to40/HLTPhysics1/minosMenuRun296786V1/170615_220431/0000/log', 1.),
#     ('/store/group/phys_tau/Run296786/PU36to40/HLTPhysics2/minosMenuRun296786V1/170615_220635/0000/log', 1.),
#     ('/store/group/phys_tau/Run296786/PU36to40/HLTPhysics3/minosMenuRun296786V1/170615_220846/0000/log', 1.),
#     ('/store/group/phys_tau/Run296786/PU36to40/HLTPhysics4/minosMenuRun296786V1/170615_221052/0000/log', 1.),
#     ('/store/group/phys_tau/Run296786/PU36to40/HLTPhysics5/minosMenuRun296786V1/170615_221309/0000/log', 1.),
#     ('/store/group/phys_tau/Run296786/PU36to40/HLTPhysics6/minosMenuRun296786V1/170615_221522/0000/log', 1.),
#     ('/store/group/phys_tau/Run296786/PU36to40/HLTPhysics7/minosMenuRun296786V1/170615_221730/0000/log', 1.),
#     ('/store/group/phys_tau/Run296786/PU36to40/HLTPhysics8/minosMenuRun296786V1/170615_221947/0000/log', 1.),

#     ('/store/group/phys_tau/Run296786/PU40to44/HLTPhysics1/minosMenuRun296786V1/170615_220355/0000/log', 1.),
#     ('/store/group/phys_tau/Run296786/PU40to44/HLTPhysics2/minosMenuRun296786V1/170615_220605/0000/log', 1.),
#     ('/store/group/phys_tau/Run296786/PU40to44/HLTPhysics3/minosMenuRun296786V1/170615_220816/0000/log', 1.),
#     ('/store/group/phys_tau/Run296786/PU40to44/HLTPhysics4/minosMenuRun296786V1/170615_221019/0000/log', 1.),
#     ('/store/group/phys_tau/Run296786/PU40to44/HLTPhysics5/minosMenuRun296786V1/170615_221238/0000/log', 1.),
#     ('/store/group/phys_tau/Run296786/PU40to44/HLTPhysics6/minosMenuRun296786V1/170615_221450/0000/log', 1.),
#     ('/store/group/phys_tau/Run296786/PU40to44/HLTPhysics7/minosMenuRun296786V1/170615_221658/0000/log', 1.),
#     ('/store/group/phys_tau/Run296786/PU40to44/HLTPhysics8/minosMenuRun296786V1/170615_221914/0000/log', 1.),

    ('/store/group/phys_tau/Run296786/PU44to47/HLTPhysics1/minosMenuRun296786V1/170615_220324/0000/log', 1.),
    ('/store/group/phys_tau/Run296786/PU44to47/HLTPhysics2/minosMenuRun296786V1/170615_220532/0000/log', 1.),
    ('/store/group/phys_tau/Run296786/PU44to47/HLTPhysics3/minosMenuRun296786V1/170615_220743/0000/log', 1.),
    ('/store/group/phys_tau/Run296786/PU44to47/HLTPhysics4/minosMenuRun296786V1/170615_220949/0000/log', 1.),
    ('/store/group/phys_tau/Run296786/PU44to47/HLTPhysics5/minosMenuRun296786V1/170615_221200/0000/log', 1.),
    ('/store/group/phys_tau/Run296786/PU44to47/HLTPhysics6/minosMenuRun296786V1/170615_221418/0000/log', 1.),
    ('/store/group/phys_tau/Run296786/PU44to47/HLTPhysics7/minosMenuRun296786V1/170615_221626/0000/log', 1.),
    ('/store/group/phys_tau/Run296786/PU44to47/HLTPhysics8/minosMenuRun296786V1/170615_221843/0000/log', 1.),
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

outfile = open('rates_HLTPhysics_run296786_Minos_PU44to47.csv', 'w+')
#     outfile = open('rates_HLTPhysics_smallAPE.csv', 'w+')
for k, v in total.filters.iteritems():
    efficiency = float(v.passed)/float(v.visited)
    print >> outfile, ','.join([str(k), str(v.passed), str(v.visited), str(efficiency), str(20./6.22*150.*250.*efficiency)])
    print k,' '*(80-len(k)), v.passed, v.visited, efficiency, '\t\t', 20./6.22*150.*250.*efficiency, 'Hz'

outfile.close()


