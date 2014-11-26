#! /usr/bin/env python

import os
import subprocess
import socket

#list_of_jobs_file_name = subprocess.check_output(['mktemp'])[:-1]
list_of_jobs_file_name = '8rn7c98q7r8734h9rc7owrakfhkjwaehrlk32jhakj3hr.garbage'
list_of_jobs_file = open(list_of_jobs_file_name,'w')

subprocess.call(['JobShow.csh'],
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

    search_string = 'Running job # '
    running_job_pos = line.find(search_string)

    found_a_job = False
    the_job = 0
    if num_nums == 4:
        found_a_job = True
        the_job = int(words[0])
    elif running_job_pos != -1:
        found_a_job = True
        rest_of_line = line[running_job_pos+len(search_string):-1]
        the_job = int(rest_of_line.split()[0])

    if found_a_job:
        set_of_jobs_to_kill.add(str(the_job))

for job in set_of_jobs_to_kill:
    print 'Killing job #'+job+'...'
    subprocess.Popen(['nice','-n','19','JobKill.csh',job])

if socket.gethostname() == 'cms2.physics.ucsb.edu':
    print 'Cleaning up...'
    subprocess.Popen(['nice','-n','19','JobCleanup.csh'])
        
list_of_jobs_file.close()
os.remove(list_of_jobs_file_name)
