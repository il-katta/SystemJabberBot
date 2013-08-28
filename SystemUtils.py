'''
Created on 25/ago/2013

@author: katta
'''

class SystemUtils(object):
    
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