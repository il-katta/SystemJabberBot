'''
Created on 25/ago/2013

@author: katta
'''
import transmissionrpc

class TorrentCli(object):
    '''
    classdocs
    '''
    __tcc={}

    def __init__(self,host,port=9091,user=None,psw=None):
        if user is None:
            self.__tcc = {"host":host,"port":port}
        else:
            self.__tcc = {"host":host,"port":port,"user":user,"psw":psw}
    
    def __connect(self):
        cc = self.__tcc
        if cc.has_key('user'):
            return transmissionrpc.Client(cc['host'],port=cc['port'],user=cc['user'],password=cc['psw'])
        else:
            return transmissionrpc.Client(cc['host'],port=cc['port'])
    
    def torrentList(self):
        tc = self.__connect()
        trs = []
        torrents = tc.get_torrents()
        for i in range( 0, len(torrents) ):
            tr = torrents[i]
            trs.append( "%d - %s - %s - %0.2f%% " % ( tr.id , tr.name , tr.status , tr.progress ) )
        return "\n".join(trs)
    '''
    def torrent_complete(self):
        tc = self.__connect()
        fs=tc.get_files()
        completed=[];
        for i in range(1,len(fs)+1):
            f=fs[i]
            c=True
            for sf in f:
                if sf['completed'] is not sf['size']:
                    c=False
            if c:
                completed.append("%d %s" % ( i , tc.get_torrent(i) ) )
        return "\n".join(completed)
    '''
    def torrent_complete(self):
        tc = self.__connect()
        trs = []
        torrents = tc.get_torrents()
        for i in range( 0, len(torrents) ):
            tr = torrents[i]
            if tr.status is 'seeding':
                trs.append("%d - %s : %s" % (tr.id,tr.name,tr.status) )
        return "\n".join(trs)
    def torrent(self,idt):
        tc = self.__connect()
        tr=tc.get_torrent(idt)
        return "%d - %s - %s - %0.2f%% " % ( tr.id , tr.name , tr.status , tr.progress ) 
        
    def torrent_remove(self,args):
        tc = self.__connect()
        tt=tc.get_torrent(args)
        tc.remove_torrent(tt.hashString,delete_data=False)
        return tt
    
    def torrent_remove_complete(self):
        tc = self.__connect()
        trs = []
        torrents = tc.get_torrents()
        for i in range( 0, len(torrents) ):
            tr = torrents[i]
            if tr.status is 'seeding':
                self.torrent_remove(tr.id)
                trs.append(tr.name)
        return trs
    
    def torrent_remove_data(self,args):
        tc = self.__connect()
        tt=tc.get_torrent(int(args))
        tc.remove_torrent(tt.hashString,delete_data=True)
        return tt

    def add_torrent(self,args):
        tc = self.__connect()
        t=tc.add_torrent(args)
        return t
    
    def stat(self):
        tc = self.__connect()
        return tc.session_stats()
    
    def start(self,idt,force=False):
        tc = self.__connect()
        tc.start_torrent(idt, bypass_queue=force )
        return self.torrent(idt)
        
    def start_all(self,force=False):
        tc = self.__connect()
        tc.start_all(bypass_queue=force )
    
    def stop(self,idt):
        tc = self.__connect()
        tc.stop_torrent(idt)
        return self.torrent(idt)
    
    def stop_all(self):
        tc = self.__connect()
        for tor in tc.get_torrents():
            tor.stop()
    
    def verify(self,idt):
        tc = self.__connect()
        tc.verify_torrent(idt)
        return self.torrent(idt)
    
    def verify_all(self):
        tc = self.__connect() 
        for tor in tc.get_torrents():
            tc.verify_torrent(tor.id) 