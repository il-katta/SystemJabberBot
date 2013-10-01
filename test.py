import os,shlex
from os import getcwd, chdir
from subprocess import Popen,PIPE,check_output
import subprocess
#p=check_output(('grep','pts'),stdin=Popen(('ps','aux'), stdout=PIPE, shell=True).stdout, shell=True )
from subprocess import Popen, PIPE
from shlex import split



cmd="sleep 2 && echo ciao"
cmd="echo -n \"ciao\nmondo\" | grep \"mondo\""
shcmd="/bin/sh -c '%s'" % cmd
p=Popen(split(shcmd), stdout=PIPE).stdout.read()
print str(p)
exit()

subprocess.check_call(cmd, shell=True) # | (pipe) and && works but: how can redirect output into string??
exit()
print split(cmd)
#p = Popen("md5sum", stdin=Popen("ls", stdout=PIPE).stdout)


p=subprocess.check_output(split(cmd))
print p
exit()