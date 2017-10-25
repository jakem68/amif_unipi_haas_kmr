import websocket
import json
import time
import urllib2

url = "ws://192.168.1.23/ws"
http_url_all = "http://192.168.1.23/rest/all"

ws = websocket.WebSocket()
ws.connect(url)
i=0
td1 = 0.05

def get_status(dev, circuit):
    status_all = json.loads(urllib2.urlopen(http_url_all).read())
    for d in status_all:
        if d['dev'] == dev and d['circuit'] == circuit:
            print d['value']
            return d['value']

def set_status(dev, circuit, value):
    msg = '{"cmd":"set","dev":"%s","circuit":"%s","value":"%s"}' % (dev, circuit, value)
    print msg
    ws.send(msg)
    time.sleep(td1)

def demo():
    for i in range(9):
        for i in range(1, 9):
            msg = '{"cmd":"set","dev":"relay","circuit":"%s", "value":"1"}' % i
            ws.send(msg)
            time.sleep(td1)

        for i in range(1, 9):
            msg = '{"cmd":"set","dev":"relay","circuit":"%s", "value":"0"}' % i
            ws.send(msg)
            time.sleep(td1)

    for i in range(9):
        for i in range(1, 9):
            msg = '{"cmd":"set","dev":"relay","circuit":"%s", "value":"1"}' % i
            ws.send(msg)
            time.sleep(td1)
            msg = '{"cmd":"set","dev":"relay","circuit":"%s", "value":"0"}' % i
            ws.send(msg)
            time.sleep(td1)

demo()

set_status('relay', '3', '1')
time.sleep(1)
set_status('relay', '3', '0')

while 1:
    print get_status('input', '1')
    time.sleep(1)


ws.close()