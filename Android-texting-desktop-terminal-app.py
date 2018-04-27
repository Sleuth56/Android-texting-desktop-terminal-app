"""The companion app for my Android Termux scrypt"""
from socket import socket, AF_INET, SOCK_STREAM
import threading
import pyaes
import sys
import subprocess

PORT = 8888
IP = '0.0.0.0'

try:
    PASSWORD = open('password.conf', 'r').read()
except FileNotFoundError:
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
    PORT2 = 8889
    IP2 = '0.0.0.0'

    SOCKET2 = socket(AF_INET, SOCK_STREAM)
    SOCKET2.bind((IP2, PORT2))
    SOCKET2.listen(1)
    (CLIENTSOCKET2, ADDRESS2) = SOCKET.accept()

    while True:
        TEST2 = CLIENTSOCKET2.recv(1024)
        print(bytes.decode(decrypt(TEST2)))

# Definging the serversocket variable and setting it to use the TCP protocol
SOCKET = socket(AF_INET, SOCK_STREAM)
SOCKET.bind((IP, PORT))
SOCKET.listen(1)
(CLIENTSOCKET, ADDRESS) = SOCKET.accept()

try:
    threading.incomming_texts(incomming_texts, ())
except:
    print("Error: unable to start thread")

while True:
    command = input(': ')
