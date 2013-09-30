'''
Created on 25/ago/2013

@author: katta
'''
import os,shlex
from os import getcwd, chdir
from subprocess import Popen,PIPE
class SystemUtils(object):
    __cwd=None


    def __init__(self):
        self.__cwd=getcwd()

    def __execmd(self,cmd):
        
        args=shlex.split(cmd)
        if '|' in args:
            i=args.index('|')
            l=' '.join(args[:i])
            r=args[i+1:]
            print("i: %d \n l: '%s' \n r: '%s' \n" % (i,l,' '.join(r)))
            print('args[i]: %s\n'% args[i])
            return Popen(r,stdin=self.__execmd(l)).stdout
        else:
            out = Popen(args, stdout=PIPE, shell=True).stdout
            return out

    def execmd(self,cmd):
        rcwd=getcwd()
        chdir(self.__cwd)
        ret = self.__execmd(cmd).read()
        chdir(rcwd)
        return ret

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

if __name__ == "__main__":
    su=SystemUtils()
    out=su.execmd('ps aux | grep bash')
    print(out);