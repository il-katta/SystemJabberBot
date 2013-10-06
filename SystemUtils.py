'''
Created on 25/ago/2013

@author: katta
'''
import os
from shlex import split
from os import getcwd, chdir
from subprocess import Popen,PIPE
#import cStringIO

class SystemUtils(object):
    _cwd=None

    def __init__(self):
        self._cwd=getcwd()

    def _execmd(self,cmd):
        def which_cmd(args):
            args[0] = self.which(args[0]) or args[0]
            return args

        def split_cmd(pcmd,s):
            i = (len(args) - 1) - args[::-1].index(s)
            l = which_cmd( args[:i] )
            r = which_cmd( args[i+1:] )
            return l,r

        args=split(cmd)
        

        if '|' in args:
            l , r = split_cmd(args,'|')
            #p = Popen(r, stdin=self._execmd( ' '.join(l) ),stdout=PIPE)
            retl , pin = self._execmd( ' '.join(l) )
            p = Popen(r, stdout=PIPE, stdin=PIPE) 
            stdout, stderr = p.communicate(input=pin)
            return p.wait() , stdout
        
        if '&&' in args:
            l , r = split_cmd(args,'&&')
            retcl, stdoutl = self._execmd( ' '.join(l) )
            if retcl is 0:
                retcr , stdoutr = self._execmd( ' '.join(r) )
                return retcr , "%s%s" % (stdoutl,stdoutr) 
            return retcl, stdoutl
        
        p = Popen(args, stdout=PIPE)
        retc = p.wait()
        stdout = p.stdout.read()
        return retc , stdout

    def execmd(self,cmd):
        rcwd=getcwd()
        chdir(self._cwd)
        code, out = self._execmd(cmd)
        chdir(rcwd)
        return out

    def cd(self,path):
        try:
            self._cwd=path;
        except Exception:
            pass

    def pwd(self):
        return self._cwd

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

