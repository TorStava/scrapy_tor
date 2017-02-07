# -*- coding: utf-8 -*-
import time
import urllib

import requests
import stem
import stem.connection
from stem import Signal
from stem.control import Controller

PROXY_PORT = 8118 # privoxy proxy port
TOR_CONTROL_PORT = 9151
TOR_CONTROL_PASSWORD = '123456'

def create_http_session(proxy_port):
    s = requests.Session()
    s.proxies = {
        "http": "http://127.0.0.1:%d" % proxy_port
    }
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    })
    
    return s

def query(session, url):
    # communicate with TOR via a local proxy (privoxy)
    r = session.get(url)
    return r.text

# signal TOR for a new connection 
def renew_tor_connection(control_port, password):
    with Controller.from_port(port=control_port) as controller:
        controller.authenticate(password=password)
        controller.signal(Signal.NEWNYM)
        controller.close()

if __name__ == '__main__':
    interval = 2 # two seconds
    oldIP = "0.0.0.0"
    newIP = "0.0.0.0"
    http_session = create_http_session(PROXY_PORT)

    for i in range(7):
        renew_tor_connection(TOR_CONTROL_PORT, TOR_CONTROL_PASSWORD)
        if newIP != "0.0.0.0":
            oldIP = newIP
        newIP = query(http_session, "http://icanhazip.com/")

        seconds = 0
        # loop until the "new" IP address
        # is different than the "old" IP address,
        # as it may take the TOR network some
        # time to effect a different IP address 
        while oldIP == newIP:
            time.sleep(interval)
            seconds += interval
            newIP = query(http_session, "http://icanhazip.com/")
            print ("%d seconds elapsed awaiting a different IP address." % seconds)
        # new IP address
        print ("newIP: %s" % newIP)