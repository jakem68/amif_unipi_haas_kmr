import websocket
import json
import time
import pigpio
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
PIN = 27
GPIO.setup(PIN,GPIO.OUT)

url = "ws://192.168.1.23/ws"

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

#receiving messages
#ws = websocket.WebSocketApp(url, on_message = on_message, on_error = on_error, on_close = on_close)
#ws.run_forever()

#sending messages
ws = websocket.WebSocket()
ws.connect(url)
while True:
    # ws.send('{"cmd":"set","dev":"relay","circuit":"3","value":"1"}')
    # time.sleep(1)
    # ws.send('{"cmd":"set","dev":"relay","circuit":"3","value":"0"}')
    # time.sleep(1)

    GPIO.output(PIN,True)


    time.sleep(1)
    ws.send('{"cmd":"set","dev":"relay","circuit":"3","value":"0"}')
    time.sleep(1)


ws.close()