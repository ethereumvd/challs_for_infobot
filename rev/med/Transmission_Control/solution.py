from pwn import *

buf = bytearray(b"l5{0v0Y7fVf?u>|:O!|Lx!o$j,;f")
print(buf)
print(len(buf))
for i in range(len(buf)):
    buf[i] ^= i

print((b"flag{" + buf).decode())
