import websocket
import json
import time
import urllib2

# url = "ws://192.168.1.23/ws"
url_unipi = "ws://192.168.0.149/ws"
# http_url_all = "http://192.168.1.23/rest/all"
http_url_unipi_all = "http://192.168.0.149/rest/all"

ws_unipi = websocket.WebSocket()
ws_unipi.connect(url_unipi)
td1 = 0.1   # time delay between switching
rpt = 1     # nr of repeats in demo

def get_status(dev, circuit):
    status_all = json.loads(urllib2.urlopen(http_url_unipi_all).read())
    for d in status_all:
        if d['dev'] == dev and d['circuit'] == circuit:
            print d['value']
            return d['value']

def set_status(dev, circuit, value):
    msg = '{"cmd":"set","dev":"%s","circuit":"%s","value":"%s"}' % (dev, circuit, value)
    print msg
    ws_unipi.send(msg)
    time.sleep(td1)

def demo():
    for i in range(rpt):
        for i in range(1, 9):
            msg = '{"cmd":"set","dev":"relay","circuit":"%s", "value":"1"}' % i
            ws_unipi.send(msg)
            time.sleep(td1)

        for i in range(1, 9):
            msg = '{"cmd":"set","dev":"relay","circuit":"%s", "value":"0"}' % i
            ws_unipi.send(msg)
            time.sleep(td1)

    for i in range(rpt):
        for i in range(1, 9):
            msg = '{"cmd":"set","dev":"relay","circuit":"%s", "value":"1"}' % i
            ws_unipi.send(msg)
            time.sleep(td1)
            msg = '{"cmd":"set","dev":"relay","circuit":"%s", "value":"0"}' % i
            ws_unipi.send(msg)
            time.sleep(td1)

demo()

set_status('relay', '3', '1')
time.sleep(1)
set_status('relay', '3', '0')

while 1:
    print get_status('input', '1')
    time.sleep(1)


ws_unipi.close()