import os,shlex
from os import getcwd, chdir
from subprocess import Popen,PIPE,check_output

p=check_output(('grep','"ipython2"'),stdin=Popen(('ps','aux'), stdout=PIPE, shell=True).stdout, shell=True )
#p=Popen(('grep','bash'),stdin=Popen(('ps','aux'), stdout=PIPE, shell=True).stdout, stdout=PIPE, shell=True )
print p.stdout.read()