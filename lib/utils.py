def int_to_bytes(n, length):
    return n.to_bytes(length, byteorder='big')

def bytes_to_int(b):
    return int.from_bytes(b, byteorder='big')
