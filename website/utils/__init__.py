
def stoi(s):
    h = '0x'
    for i in s: h += hex(ord(i))[-2:]
    return int(h, 16)
