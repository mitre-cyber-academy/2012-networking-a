import nids
import zlib
import pickle
import traceback
import struct
import sys
import time
import binascii

end_states = (nids.NIDS_CLOSE, nids.NIDS_TIMEOUT, nids.NIDS_RESET)

def packet_time(t):
        local = time.localtime(t)
        return "%02d:%02d:%02d" % (local[3], local[4], local[5])    

def solve(data):
    unzip = zlib.decompressobj()
    d = data
    payload = ''

    print len(d)
    print len(d) / 1024
    while len(d) > 0:
        zipped_length= struct.unpack('<H', d[:2])[0]
        print zipped_length
        d = d[2:]
        chunk = d[:zipped_length]
        payload += chunk
        d = d[1022:]

    print "compressed payload len = %d" % len(payload)
    print binascii.hexlify(payload[:16])
    payload = zlib.decompress(payload)

    f = open('pickled', 'wb')
    f.write(payload)
    f.close()

    h = pickle.loads(payload)
    print h[36328]
        

def handle_tcp(tcp):
    ((src, sport), (dst, dport)) = tcp.addr
    if tcp.nids_state == nids.NIDS_JUST_EST:
        tcp.client.collect = 1
        tcp.server.collect = 1
        print "%s:%d -> %s:%d" % (src, sport, dst, dport)
    elif tcp.nids_state == nids.NIDS_DATA:
        if tcp.client.count_new > 0:
            tcp.discard(0)
            return
        if tcp.server.count_new > 0:
            tcp.discard(0)
            return
    elif tcp.nids_state in end_states:
        print "done with %d bytes" % tcp.server.count
        solve(tcp.server.data[:tcp.server.count])

if __name__ == "__main__":
    nids.param("pcap_filter", "tcp port %d" % 20)                    
    nids.chksum_ctl([("0.0.0.0/0", False),])
    nids.param("filename", "challenge.pcap")
    nids.param("scan_num_hosts", 0)
    nids.init()
    nids.register_tcp(handle_tcp)
    try:
        nids.run()
    except nids.error, e:
        print "nids/pcap error:", e
    except Exception, e:
        traceback.print_exc(file=sys.stderr)
