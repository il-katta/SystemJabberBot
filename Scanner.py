'''
Created on 25/ago/2013

@author: katta
'''
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
from scapy import arch
# https://pypi.python.org/pypi/netifaces
from netifaces import interfaces, ifaddresses, AF_INET

conf.verb = 0

class Scanner(object):
    '''
    classdocs
    '''

    def __init__(self,iface=None):
        if iface:
            conf.iface=iface
            
    
    def hostScanner(self):
        addr=arch.get_if_addr(conf.iface)
        ip_scan="192.168.1.0/24"
        a,u=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip_scan),timeout=2)
        a.summary(lambda (s,r): r.sprintf("%ARP.psrc% è attivo") )