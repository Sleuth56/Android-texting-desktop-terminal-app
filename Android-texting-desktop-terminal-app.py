"""The companion app for my Android Termux scrypt"""
from socket import socket, AF_INET, SOCK_STREAM
import pyaes
import sys
import time

PORT = 8888
PORT2 = 8889

IP = '0.0.0.0'

try:
    PASSWORD = open('password.conf', 'r').read()
except:
    print('ERROR: Can\'t find password.conf file')
    sys.exit()


def encrypt(MESSAGE):
    # key must be bytes, so we convert it
    key = PASSWORD.encode('utf-8')

    aes = pyaes.AESModeOfOperationCTR(key)
    return aes.encrypt(MESSAGE)


def decrypt(MESSAGE):
    # key must be bytes, so we convert it
    key = PASSWORD.encode('utf-8')

    # CRT mode decryption requires a new instance be created
    aes = pyaes.AESModeOfOperationCTR(key)

    # decrypted data is always binary, need to decode to plaintext
    return aes.decrypt(MESSAGE).decode('utf-8')


def incomming_texts():
    SOCKET2 = socket(AF_INET, SOCK_STREAM)
    SOCKET2.bind((IP, PORT2))
    SOCKET2.listen(1)
    (CLIENTSOCKET2, ADDRESS2) = SOCKET2.accept()

    while True:
        TEST2 = CLIENTSOCKET2.recv(1024)
        print(bytes.decode(decrypt(TEST2)))


newthread = incomming_texts()
newthread.start()

# Definging the serversocket variable and setting it to use the TCP protocol
SOCKET = socket(AF_INET, SOCK_STREAM)
SOCKET.bind((IP, PORT))
SOCKET.listen(1)
(CLIENTSOCKET, ADDRESS) = SOCKET.accept()

print('to exit type exit')
print()
while True:
    NUMBER = input("Number: ")
    if(NUMBER == 'exit'):
        CLIENTSOCKET.send(encrypt('exit'))
        time.sleep(0.4)
        CLIENTSOCKET.close()
        SOCKET.close()
        sys.exit()

    MESSAGE = input("Message: ")
    if(MESSAGE == 'exit'):
        CLIENTSOCKET.send(encrypt('exit'))
        time.sleep(0.4)
        CLIENTSOCKET.close()
        SOCKET.close()
        sys.exit()
    CLIENTSOCKET.send(encrypt('send text'))
    time.sleep(0.2)
    CLIENTSOCKET.send(encrypt(NUMBER))
    time.sleep(0.2)
    CLIENTSOCKET.send(encrypt(MESSAGE))
