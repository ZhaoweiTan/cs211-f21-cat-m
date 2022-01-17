# main.py -- put your code here!

# Good links:
# https://alepycom.gitbooks.io/pycom-documentation/content/chapter/tutorials/lte/
# https://docs.pycom.io/gitbook/assets/Monarch-LR5110-ATCmdRefMan-rev6_noConfidential.pdf
# https://www.twilio.com/docs/iot/supersim/tutorials/apn-configuration
# http://www.noomio.com.au/wiki/bg96/bg96-volte-on-cat-m1/
# https://forum.pycom.io/topic/4165/sms-messages/2

# pylint: disable=all

import socket
import ssl
import time
from network import LTE

lte = LTE(debug=True) # Instantiate LTE object and print AT commands (debug mode)
lte.attach() # attach the cellular modem to a base station
while not lte.isattached():
    time.sleep(0.25)
lte.connect() # start a data session and obtain an IP address
while not lte.isconnected():
    time.sleep(0.25)

s = socket.socket()
s = ssl.wrap_socket(s)
s.connect(socket.getaddrinfo('www.google.com', 443)[0][-1])
s.send(b"GET / HTTP/1.0\r\n\r\n")
print(s.recv(4096))
s.close()

# Leave LTE open for now
# lte.disconnect()
# lte.dettach()

print("""

Unless there is a failure above, the FiPy is in LTE-M Data mode.
The above response was achieved using an SSL socket provided by
Pycom (FiPy vendor) as follows:

>>> s = socket.socket()
>>> s = ssl.wrap_socket(s)
>>> s.connect(socket.getaddrinfo('www.google.com', 443)[0][-1])
>>> s.send(b"GET / HTTP/1.0\\r\\n\\r\\n")
>>> print(s.recv(4096))
>>> s.close()

Note that since the modem is in data mode, AT commands cannot be sent.
Disconnect to leave data mode, then run some AT commands:

>>> lte.disconnect()
>>> lte.send_at_command('AT+CSQ')

Some useful links are provided in the comments of this file, main.py.
Pycom recommends the Pymakr program, but I was able to get Adafruit's
command line file interface, ampy, up and running. From the external
computer:

# ampy -p <COMX|/dev/ttyACM1> ls
# ampy -p <COMX|/dev/ttyACM1> ls /flash
# ampy -p <COMX|/dev/ttyACM1> get /flash/main.py
# ampy -p <COMX|/dev/ttyACM1> get /flash/main.py > main.py

Update main.py then push it back:

# ampy -p <COMX|/dev/ttyACM1> put main.py /flash/main.py

Or just use Pymakr...

""")

# SMS state setup
sms_is_initialized = False
def config_sms():
    global sms_is_initialized
    if not sms_is_initialized:
        lte.send_at_cmd('AT+CMGF=1') # Text message format
        lte.send_at_cmd('AT+CPMS="SM"') # Use SIM for message storage
        sms_is_initialized = True

# Send a text message to <number> with message <msg>
def send_sms(number, msg):
    config_sms()
    at_cmd = 'AT+SQNSMSSEND="%s","%s",1' % (number, msg)
    lte.send_at_cmd(at_cmd)

# Get the current list of SMS messages
def list_sms():
    config_sms()
    lte.send_at_cmd('AT+CMGL="ALL"')

# Testing
lte.disconnect()
lte.send_at_cmd('AT+CGDATA="PPP",1')
lte.send_at_cmd('+++')
# s = socket.socket()
# s = ssl.wrap_socket(s)
# s.connect(socket.getaddrinfo('www.google.com', 443)[0][-1])
# s.send(b"GET / HTTP/1.0\r\n\r\n")
# print(s.recv(4096))
# s.close()
for i in range(10):
    print(lte.send_at_cmd('AT!="fsm"'))
