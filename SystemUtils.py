'''
Created on 25/ago/2013

@author: katta
'''
import os,shlex
from os import getcwd, chdir
from subprocess import Popen,PIPE
import cStringIO

class SystemUtils(object):
    __cwd=None


    def __init__(self):
        self.__cwd=getcwd()

    def __execmd(self,cmd):
        args=shlex.split(cmd)
        if '|' in args:
            #i = args.index('|')
            i = (len(args) - 1) - args[::-1].index('|')
            l = ' '.join(args[:i])
            r = args[i+1:]
            return Popen(r, stdin=self.__execmd(l),stdout=PIPE).stdout
        else:
            return  Popen(args, stdout=PIPE).stdout

    def execmd(self,cmd):
        rcwd=getcwd()
        chdir(self.__cwd)
        ret = self.__execmd(cmd)
        chdir(rcwd)
        return ret.read()

    def cd(self,path):
        try:
            self.__cwd=path;
        except Exception:
            pass

    def pwd(self):
        return self.__cwd

    @staticmethod
    def cat(sfile):
        in_f= open(sfile,'r')
        ls=in_f.readlines()
        in_f.close()
        return '\n'.join( ls )
    
    @staticmethod
    def tail(sfile,nls=20):
        in_f= open(sfile,'r')
        ls=in_f.readlines()
        in_f.close()
        t=len(ls)-nls
        if t<0:
            t=0
        return '\n'.join( ls[t:] )
    
    @staticmethod
    def head(sfile,nls=20):
        in_f= open(sfile,'r')
        ls=in_f.readlines()
        in_f.close()
        return '\n'.join( ls[:nls] )

    @staticmethod
    def which(program):
        def is_exe(fpath):
            return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

        fpath, fname = os.path.split(program)
        if fpath:
            if is_exe(program):
                return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                path = path.strip('"')
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    return exe_file

        return None

