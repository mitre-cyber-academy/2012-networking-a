import socket
import struct
import zlib
import random
import pickle

HOST = '127.0.0.1'
PORT = 20

def pack_message(payload):
    p = payload
    zip_len = len(p)
    header = struct.pack('<H', zip_len)
    p += ''.join([chr(random.randint(0,255)) for i in range(1024 - len(header) - len(p))])
    msg = header + p
    return msg

if __name__ == "__main__":
    s = socket.socket()
    s.connect((HOST, PORT))

    d = {}
    f = open('blob', 'rb')
    for i in range(500):
        d[i] = f.read(64)
        
    d[36328] = 'MCA-20DFF3A1'

    msg = pickle.dumps(d)
    msg = zlib.compress(msg)
    print "compressed payload len = %d" % len(msg)
    while len(msg) > 0:
        chunk_size = random.randint(0, 1020)
        if chunk_size > len(msg):
            chunk_size = len(msg)
        chunk = msg[:chunk_size]
        print "len(chunk) = %d" % len(chunk)
        s.sendall(pack_message(chunk))
        msg = msg[chunk_size:]
    s.close()
    
    
