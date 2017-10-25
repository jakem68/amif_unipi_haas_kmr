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


def on_message(ws, message):
    obj = json.loads(message)
    dev = obj['dev']
    circuit = obj['circuit']
    value = obj['value']
    print message

def on_error(ws, error):
    print error

def on_close(ws):
    print "Connection closed"

def iterate_answer(status_all):
    for d in status_all:
        for key, value in d.iteritems():
            if key == 'dev' and value == 'input':
                print 'di' , d['circuit'], '=', d['value'], '; ',
    print(' ')

def get_status(dev, circuit):
    status_all = json.loads(urllib2.urlopen(http_url_all).read())
    for d in status_all:
        if d['dev'] == dev and d['circuit'] == circuit:
            print d['value']
            return d['value']

            # if d['dev'] == dev and d['circuit'] == circuit:
            #     print d['value']
            # status = 'value' for dev in enumerate (d) if d['dev'] == dev
            # print status


#receiving messages
# ws = websocket.WebSocketApp(url, on_message = on_message, on_error = on_error, on_close = on_close)
# ws.run_forever()

def demo():
    for i in range(1):
        for i in range(1, 9):
            msg = '{"cmd":"set","dev":"relay","circuit":"%s", "value":"1"}' % i
            # print msg
            ws.send(msg)
            time.sleep(td1)
            status_all = json.loads(urllib2.urlopen(http_url_all).read())
            # iterate_answer(status_all)
            input1 = get_status('input', '1')

        for i in range(1, 9):
            msg = '{"cmd":"set","dev":"relay","circuit":"%s", "value":"0"}' % i
            # print msg
            ws.send(msg)
            time.sleep(td1)
            status_all = json.loads(urllib2.urlopen(http_url_all).read())
            # iterate_answer(status_all)
            get_status('input', '1')

    for i in range(1):
        for i in range(1, 9):
            msg = '{"cmd":"set","dev":"relay","circuit":"%s", "value":"1"}' % i
            # print msg
            ws.send(msg)
            time.sleep(td1)
            status_all = json.loads(urllib2.urlopen(http_url_all).read())
            # iterate_answer(status_all)
            get_status('input', '1')

            msg = '{"cmd":"set","dev":"relay","circuit":"%s", "value":"0"}' % i
            # print msg
            ws.send(msg)
            time.sleep(td1)
            status_all = json.loads(urllib2.urlopen(http_url_all).read())
            # iterate_answer(status_all)
            get_status('input', '1')

demo()

while 1:
    print get_status('input', '1')
    time.sleep(1)

ws.close()