#!/bin/python2
'''
Created on 25/ago/2013

@author: Katta < ilkatta88@gmail.com >
'''
# deps: http://thp.io/2007/python-jabberbot/
from jabberbot import JabberBot, botcmd
import jabberbot 
from ConfigParser import RawConfigParser,NoSectionError,NoOptionError
from SystemInfo import SystemInfo
from SystemUtils import SystemUtils
import logging, datetime, shlex
from os.path import expanduser

class SystemInfoJabberBot(JabberBot):
    auth_users=[]
    sysinfo=None
    __tc=None
    __logs=None
    __sysutils=None
    def __init__(self, username, password,auth_users):
        jabberbot.JabberBot.__init__(self, username, password)
        self.auth_users=auth_users
        self.sysinfo = SystemInfo()
        self.__sysu= SystemUtils()
    
    def setTransmissionConfig(self,host,port=9091,user=None,psw=None):
        try:
            from  TorrentCli import TorrentCli
            self.__tc = TorrentCli(host,port,user,psw)
            return self.__tc != None
        except:
            return False
    
    def setLogFiles(self,log_files):
        self.__logs=log_files
    
    def callback_message(self, conn, mess):
        # This is an example how you can set a "master" to listen to:
        if not self.whoami(mess,"") in self.auth_users:
            self.send(mess.getFrom(), "Commands denied", mess)
        else:
            return jabberbot.JabberBot.callback_message(self, conn, mess)
    
    @botcmd
    def logs(self,mess,args):
        __ll=' | '.join( self.__logs.keys() )
        usage="usage:\n logs < tail | head > [< #lines >] < %s >" % __ll + "\nor\n\t logs cat < %s >" % ' | '.join( self.__logs.keys() )
        usage_cat="usage:\n logs cat < %s >" % __ll
        usage_tail="usage:\n logs tail [<#lines>] < %s >" % __ll
        usage_head="usage:\n logs head [<#lines>] < %s >" % __ll
        
        """ show log files """
        if self.__logs != None:
            try:
                argz = self.__splitstr(args)
                
                ''' cat '''
                if argz[0] == 'cat':
                    if self.__logs.has_key(argz[1]) :
                        return SystemUtils.cat(self.__logs[argz[1]])
                    else:
                        return usage_cat
                
                ''' tail '''
                if argz[0] == 'tail':
                    if argz[1].isdigit():
                        if self.__logs.has_key(argz[2]) :
                            return SystemUtils.tail(self.__logs[argz[2]],int(argz[1]))
                        return SystemUtils.tail(self.__logs[argz[2]])
                    if self.__logs.has_key(argz[1]) :
                        return SystemUtils.tail(self.__logs[argz[1]])
                    
                    return usage_tail
                
                ''' head '''
                if argz[0] == 'head':
                    if argz[1].isdigit():
                        if self.__logs.has_key(argz[2]) :
                            return SystemUtils.tail(self.__logs[argz[2]],int(argz[1]))
                        return SystemUtils.head(self.__logs[argz[2]])
                    if self.__logs.has_key(argz[1]) :
                        return SystemUtils.head(self.__logs[argz[1]])
                    return usage_head
                
            except IndexError:
                return usage
            except Exception as e:
                return "Exception occurred < %s >" % e.message
        else:
            return "log files not set in configuration file"
        
        return usage
    @botcmd
    def hello(self,mess,args):
        """ Display script info """
        return "Hello , I'm developer version of System Info Jabber Bot"
    @botcmd
    def helo(self,mess,args):
        """ Display script info """
        return self.hello(mess,args)

    @botcmd
    def which(self,mess,args):
        ''' UNIX which command '''
        path=SystemUtils.which(args)
        if path:
            return "%s : %s" % (args,path)
        else:
            return "%s : command not found" % args

    @botcmd
    def torrent(self,mess,args):
        """ torrent client """
        usage_remove="usage: torrent remove < #torrent | complete | all > \n\ttorrent remove  data < #torrent > "
        usage_add="usage: torrent add < URL | magnet >"
        usage_start="usage: torrent start < all | #torrent > [ force ]"
        usage_verify="usage: torrent verify < all | #torrent > [ force ]"
        usage_stop="usage: torrent stop < all | #torrent >"
        usage_list="usage: torrent list [< complete | #idtorrent >]"
        usage="usage:\n\t%s \n\t%s \n\t%s \n\t%s \n\t%s" % ( usage_remove , usage_add , usage_verify , usage_stop , usage_list )
        if not len(args) > 0:
            return usage
        if self.__tc != None :
            try:
                argz = self.__splitstr(args)
                
                ''' start torrent '''
                if argz[0] == 'start':
                    if  argz[1] == 'all':
                        if len(argz)>2 and argz[2]=='force':
                            self.__tc.start_all(True)
                            return "all torrents have been (forced) started"
                        else:
                            self.__tc.start_all(False)
                            return "all torrents have been started"
                    if argz[1].isdigit():
                        try:
                            force=len(argz)>2 and argz[2]=='force'
                            ret=self.__tc.start(int(argz[1]),force)
                            return "started torrent "+ret
                        except KeyError as ke:
                            return ke.message
                    
                    return usage_start
                
                ''' stop torrent '''      
                if argz[0] == 'stop' :
                    if argz[1] == 'all' :
                        self.__tc.stop_all()
                        return "all torrents have been stopped"
                    if argz[1].isdigit():
                        ret=self.__tc.stop(int(argz[1]))
                        return "stoped torrent: %s " % ret
                    return usage_stop
                
                ''' verify torrent '''
                if argz[0] == 'verify':
                    if argz[1] == 'all' :
                        self.__tc.verify_all()
                        return "all torrents have been verified"
                    if argz[1].isdigit():
                        ret=self.__tc.verify(int(argz[1]))
                        return "verified torrent: %s " % ret
                    return usage_verify
                    
                
                ''' get lists of torrents '''
                if argz[0] == 'list':
                    if len(argz) is 1:
                        return "\n"+self.__tc.torrentList()
                    if  argz[1] == 'complete':
                        return "\n"+self.__tc.torrent_complete()
                    if argz[1].isdigit():
                        return self.__tc.torrent(int(argz[1]))
                    return usage_list

                ''' remove torrent '''
                if argz[0] == 'remove':
                    try:
                        if argz[1].isdigit():
                            n = self.__tc.torrent_remove(int(argz[1])).name
                            return "torrent '%s' removed" % n
                        
                        if argz[1] == 'complete':
                            ts=self.__tc.torrent_remove_complete()
                            return 'removed torrents: \n' + '\n'.join(ts)
                        
                        if argz[1] == 'data':
                            if argz[2].isdigit():
                                n=self.__tc.torrent_remove_data( int(argz[2]) ).name
                                return "torrent '%s' removed" % n
                        raise ValueError()
                    except ValueError,IndexError:
                        pass
                    return usage_remove
                
                ''' add torrent '''
                if argz[0] == 'add':
                    try:
                        t=self.__tc.add_torrent(argz[1])
                        return "Torrent '%s' added" % t.name
                    except KeyError:
                        return 'Torrent already added'
                    except IndexError:
                        return usage_add
                
                return usage
            
            except KeyError as ke:
                return ke.message
            except Exception as e:
                return "Exception occurred < %s >" % e.message
        else:
            return "Torrent client not configured"
    
    

    @botcmd
    def serverinfo( self, mess, args):
        """Displays information about the server"""
        return self.sysinfo.serverinfo()
    
    @botcmd
    def time( self, mess, args):
        """Displays current server time"""
        return str(datetime.datetime.now())

    @botcmd
    def whoami(self, mess, args):
        """Tells you your username"""
        return mess.getFrom().getStripped()
    @botcmd
    def info(self, mess, args):
        """Display general informations """
        self.idle_proc()
        return self.status_message

    # from http://www.uhoreg.ca/programming/jabber/systembot
    @botcmd
    def who(self, mess, args):
        """Display who's currently logged in."""
        return self.sysinfo.who()
    
    @botcmd
    def df(self, mess, args):
        """report file system disk space usage"""
        return self.sysinfo.df()

    def idle_proc(self):
        status = []
        status.append(self.sysinfo.load())
        status.append(self.sysinfo.uptime())
        status.append(self.sysinfo.memusage())
        if self.sysinfo.hasSwap():
            status.append(self.sysinfo.swapusage())
        status = '\n'.join(status)
        if self.status_message != status:
            self.status_message = status
        return

    @botcmd
    def cd(self, mess, cmd):
        ''' unix command to change current working dir '''
        if cmd is '' :
            cmd='~'
        self.__sysu.cd( expanduser(cmd) )
        return self.__sysu.pwd()

    @botcmd
    def pwd(self, mess, cmd):
        ''' return currend working dir '''
        return self.__sysu.pwd()


    def unknown_command(self, mess, cmd, args):
        path=SystemUtils.which(cmd)
        if path is not None:
            return self.__sysu.execmd(str(mess.getBody()))
        else:
            return None

    @botcmd
    def load(self, mess, args):
        """ system load """
        return self.sysinfo.load()
    
    @botcmd
    def uptime(self, mess, args):
        """ system uptime """
        return self.sysinfo.uptime()
    
    @botcmd
    def memusage(self, mess, args):
        """ system memory usage """
        msg=self.sysinfo.memusage()
        if self.sysinfo.hasSwap():
            msg+="\n"+self.sysinfo.swapusage()
        return msg
    
    def __splitstr(self,args):
        return [x.strip() for x in shlex.split(args)]
    
def main():
    print "reading configuration"
    logging.basicConfig()
    config = RawConfigParser()
    config.read(['SystemInfoJabberBot.cfg',expanduser('~/.config/SystemInfoJabberBot.cfg')]) 
    username = config.get('systembot','username')
    password = config.get('systembot','password')
    auth_users_raw= config.get('systembot','auth_users')
    auth_users=auth_users_raw.replace(' ','').split(',')
    
    print "set config"
    bot = SystemInfoJabberBot(username,password,auth_users)
    
    # Transmission config
    if config.has_section('transmissionrpc'):
        host = config.get('transmissionrpc','host')
        port = config.getint('transmissionrpc','port')
        try:
            user = config.get('transmissionrpc','user')
            psw = config.get('transmissionrpc','password')
            bot.setTransmissionConfig(host,port=port,user=user,psw=psw)
        except NoOptionError:
            bot.setTransmissionConfig(host,port=port)
    
    if config.has_section('logs'):
        log_files=config.items('logs')
        
        bot.setLogFiles( dict(log_files) )
    print "start serve"
    bot.serve_forever()

    try:
        bot.quit()
    except Exception:
        pass

if __name__ == "__main__":
    while True:
        try:
            print "start server"
            main()
        except KeyboardInterrupt as q:
            print "Exception occurred < %s : %s >" % (type(q), q.message )
            print "Shutting down"
            exit(0)
        except Exception as e:
            print "Exception occurred < %s : %s >" % (type(e), e.message )
            pass