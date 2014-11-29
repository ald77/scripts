#! /usr/bin/env python

from tempfile import mkstemp
import subprocess
from socket import gethostname
from os import remove

list_of_jobs_file_name = mkstemp()[1]
list_of_jobs_file = open(list_of_jobs_file_name, 'w')

print "Finding list of jobs to kill..."
subprocess.call(['nice', '-n', '19', 'JobShow.csh'],
                stdout=list_of_jobs_file,
                stderr=subprocess.STDOUT)
list_of_jobs_file.close();
list_of_jobs_file = open(list_of_jobs_file_name, 'r')

set_of_jobs_to_kill = set()

lines = list_of_jobs_file.readlines()
for line in lines:
    words = line.split()
    num_nums = 0
    for word in words[0:4]:
        if word.isdigit():
            num_nums += 1

    if num_nums == 4:
        set_of_jobs_to_kill.add(words[0])

for job in set_of_jobs_to_kill:
    print 'Killing job #'+job+'...'
    subprocess.Popen(['nice', '-n', '19', 'JobKill.csh', job])

if gethostname() == 'cms2.physics.ucsb.edu':
    print 'Cleaning up...'
    subprocess.Popen(['nice', '-n', '19', 'JobCleanup.csh'])

list_of_jobs_file.close()
remove(list_of_jobs_file_name)
