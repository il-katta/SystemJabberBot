import os,shlex
from os import getcwd, chdir
from subprocess import Popen,PIPE

p=Popen(('grep','"bash"'),stdin=Popen(('ps','aux'), stdout=PIPE, shell=True).stdout, stdout=PIPE )