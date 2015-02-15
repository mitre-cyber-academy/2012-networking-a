The Challenge
=============

This is the 400 level networking challenge.  It requires competitors
to reconstruct a TCP flow, identify the custom protocol within, and
decode it to find the flag.  The flag is a value in a Python
dictionary that has been pickled.  There are 50,000 other keys in the
dictionary that are random bytes from MP3 files.  The dictionary is
compressed with zlib.  The compressed payload is then split into
randomly sized chunks in the range (0, 1022].  The client prepends the
length of the chunk as a little endian unsigned short.  The chunk +
header has a size in the range (0, 1024] which the client then pads to
1024 bytes using random data.  The 1024 byte chunk gets sent over the
wire to a server on TCP port 20.

challenge.pcap is a capture of the session.  It's a clean TCP session
with no other traffic so even with unsophisticated tools it should be
easy to reassemble it.

The Solution
============ 

I wrote solution.py using pynids.  All you have to do is run
solution.py to get the flag.  It's not necessary to figure out that
the decompressed data is a python dictionary because the flag appears
as a string in the raw bytes.  It took me about an hour to write and
test the solution so I expect that it will take contestants a while to
figure out the protocol and reassemble the payload.  Decompressing is
trivial once they realize that it's deflate.  Extracting the flag is
also trivial using strings at this point.  I think the real challenge
is in reconstructing the payload and then recognizing the deflate
header.  I originally considered encrypting the whole thing with RC4
and including the key at the beginning of the flow.  If this seems to
easy we can add that feature to it.  I would not tell the the cipher
but I would try to give some hints that a stream cipher was used.
That would narrow popular choices down to 3DES, RC4, and Blowfish.
They would have to guess the cipher.
