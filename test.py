import os,shlex
from os import getcwd, chdir
from subprocess import Popen,PIPE,check_output


#p=check_output(('grep','pts'),stdin=Popen(('ps','aux'), stdout=PIPE, shell=True).stdout, shell=True )
from subprocess import Popen, PIPE
from shlex import split

p = Popen("md5sum", stdin=Popen("ls", stdout=PIPE).stdout)

print str(p)