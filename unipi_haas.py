#!/usr/bin/env python
__author__ = 'Jan Kempeneers'

import websocket
import socket
import json
import time
import urllib2
import sys

# <editor-fold desc="global values">
'''
relay 1 = 'remote cycle start'
relay 3 = 'clamp control: 1 = close; 0 = open'
'''

# url_unipi = "ws://192.168.1.23/ws"    # (was IP at sirris.visitors)
# url_unipi = "ws://192.168.0.149/ws"   # (was IP at telenet-22702)
url_unipi = "ws://127.0.0.1/ws"         # (running locally on rpi)

# http_url_unipi_all = "http://192.168.1.23/rest/all"   # (was IP at sirris.visitors)
# http_url_unipi_all = "http://192.168.0.149/rest/all"  # (was IP at telenet-22702)
http_url_unipi_all = "http://127.0.0.1/rest/all"        # (running locally on rpi)

# open websocket to unipi server
ws_unipi = websocket.WebSocket()
ws_unipi.connect(url_unipi)

# IP address kmr server and communication port
# IP_kmr = ''
IP_kmr = '172.31.1.10'     # for testing with kmr_server_simulation at telenet-22702, change to kmr IP = 172.31.1.10
PORT = 30002  # Arbitrary non-privileged port

# open socket to kmr server
# s_kmr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# print("Socket created")
# s_kmr.connect(IP_kmr)

td1 = 0.1  # time delay between switching
rpt = 1  # nr of repeats in demo

# requests from server kmr
start_haas_var = b'(3)/n'
send_status_haas = b'(1)/n'  # this one is not used, client is sending every time in infinite loop
close_clamp_var = b'(2)/n'
open_clamp_var = b'(4)/n'

# machine statuses
ready = b'100'
ready_clamp_closed = b'101'
busy = b'102'
finished = b'103'
closed = 1
open = 0
# </editor-fold>


def get_status(dev, circuit):   # dev is string of device pe 'input' see unipi description https://github.com/UniPiTechnology/evok
    status_all = json.loads(urllib2.urlopen(http_url_unipi_all).read())
    for d in status_all:
        if d['dev'] == dev and d['circuit'] == circuit:
            #            print d['value']
            return d['value']


def set_device(dev, circuit, value):
    msg = '{"cmd":"set","dev":"%s","circuit":"%s","value":"%s"}' % (dev, circuit, value)
    #    print msg
    ws_unipi.send(msg)
    time.sleep(td1)

# clamp connected on relay3
def monitor_clamp():
    status_clamp = get_status('relay', '3')
    return status_clamp

def close_clamp():
    set_device('relay', '3', '1')

def open_clamp():
    set_device('relay', '3', '0')

# relay1 for controlling haas, relay2 is optional
def monitor_haas():
    status_haas= busy
    input1 = get_status('input', '1')
    input2 = get_status('input', '2')
    if input1:
        status_haas = ready
    if input2:
        status_haas = busy
    if input1 and input2:
        status_haas = busy
        print 'something is wrong! input 1 and input 2 ar both high'
    if not input1 and not input2:
        status_haas = busy
    return status_haas


def start_haas():
    set_device('relay', '1', '1')


def open_socket(IP, PORT):
    max_retries = 3
    connect_answer = 'a'
    # open a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created")


    # try to connect to server
    for i in range(max_retries):
        try:
            connect_answer = s.connect((IP, PORT))
        except:
            pass
        # print(connect_answer)
        if connect_answer is None:
            hostname = socket.gethostname()
            hostaddress = socket.getaddrinfo(IP_kmr, PORT)
            print('Socket connected with hostname: {} at addressinfo:{}'.format(hostname, hostaddress))
            connection = True
            break
    else:
        print('unable to establish socket communication to kmr')
        connection = False
    return s, connection


# wait for socket to kmr to open
def ring_server():
    kmr_socket_connection = False
    while not kmr_socket_connection:
        kmr_socket_object = open_socket(IP_kmr, PORT)
        kmr_socket = kmr_socket_object[0]
        kmr_socket_connection = kmr_socket_object[1]
    # set socket timeout
    kmr_socket.settimeout(2)
    return kmr_socket


def read_socket(s):
    msg = ''
    #    print(s)
    try:
        msg = s.recv(1024)
    except socket.timeout as e:
        print('socket timed out')
        pass
    except:
        print"can't read socket anymore, ringing the server again."
        pass
    if msg:
        print('received msg: {}'.format(msg))
    else:
        print('no message available')
    return msg


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

def toggle_relay8(nr):
    for i in range (nr):
        set_device('relay', '8', '1')
        time.sleep(td1)
        set_device('relay', '8', '0')
        time.sleep(td1)

def monitor_overall():
    status_overall = busy  # initialization
    status_haas = monitor_haas()
    status_clamp = monitor_clamp()
    if status_haas == ready and status_clamp == open:
        status_overall = ready
    if status_haas == ready and status_clamp == closed:
        status_overall = ready_clamp_closed
    if status_haas == busy:
        status_overall = busy
    return status_overall



def main():
    # demo()
    toggle_relay8(3)    # sounds relay 9 to signal there is no socket connection but is retrying.
    set_device('relay', '1', '0')    # make sure 'cycle start' relay is off when starting
    kmr_socket = ring_server()
    kmr_msg = read_socket(kmr_socket)

    # send first status of haas to kmr server
    status_overall = monitor_overall()
    kmr_socket.send(status_overall)

    while not kmr_msg is None:
        status_overall = monitor_overall()
        kmr_msg = read_socket(kmr_socket)
        # heartbeat on relay9 indicating connection established
        toggle_relay8(1)
        time.sleep(1)
        if kmr_msg == start_haas_var:
            print 'received start haas command'
            if monitor_haas() == ready:
                start_haas()
                status_overall = busy
                kmr_socket.send(status_overall)
            else:
                status_overall = monitor_overall()
                print'something went wrong! status was not ready and nevertheless start command was given, ' \
                     'status overall was %s' % status_overall
                kmr_socket.send(status_overall)

        elif kmr_msg == close_clamp_var:
            print 'closing clamp'
            close_clamp()
            time.sleep(0.5)
            status_overall = monitor_overall()
            kmr_socket.send(status_overall)

        elif kmr_msg == open_clamp_var:
            print 'opening clamp'
            open_clamp()
            time.sleep(0.5)
            status_overall = monitor_overall()
            kmr_socket.send(status_overall)
        else:
            print('status overall is %s' % status_overall)
            try:
                kmr_socket.send(status_overall)
            except:
                kmr_msg = None
                pass

    # ws_unipi.close()
    main()

if __name__ == "__main__":
    open_clamp()
    main()