import struct, sys

def read_tag(data, offset):
    if offset >= len(data):
        return None, offset
    tag_type = data[offset]
    offset += 1
    if tag_type == 0:
        return ('end', None, offset), offset
    name_len = struct.unpack('>H', data[offset:offset+2])[0]
    offset += 2
    name = data[offset:offset+name_len].decode('utf-8', errors='ignore')
    offset += name_len
    if tag_type == 0x04:
        value = struct.unpack('>q', data[offset:offset+8])[0]
        offset += 8
        if name == 'RandomSeed':
            return ('seed', value, offset), offset
    elif tag_type == 0x0A:
        while True:
            res, offset = read_tag(data, offset)
            if res is None or res[0] == 'end':
                break
        return None, offset
    else:
        if tag_type == 0x01:
            offset += 1
        elif tag_type == 0x02:
            offset += 2
        elif tag_type == 0x03:
            offset += 4
        elif tag_type == 0x05:
            offset += 4
        elif tag_type == 0x06:
            offset += 8
        elif tag_type == 0x07:
            length = struct.unpack('>i', data[offset:offset+4])[0]
            offset += 4 + length
        elif tag_type == 0x08:
            slen = struct.unpack('>H', data[offset:offset+2])[0]
            offset += 2 + slen
        elif tag_type == 0x09:
            elem_type = data[offset]
            offset += 1
            count = struct.unpack('>i', data[offset:offset+4])[0]
            offset += 4
            for _ in range(count):
                if elem_type == 0x04:
                    offset += 8
                elif elem_type == 0x03:
                    offset += 4
                elif elem_type == 0x02:
                    offset += 2
                elif elem_type == 0x01:
                    offset += 1
                else:
                    break
        elif tag_type == 0x0B:
            length = struct.unpack('>i', data[offset:offset+4])[0]
            offset += 4 + 4*length
        elif tag_type == 0x0C:
            length = struct.unpack('>i', data[offset:offset+4])[0]
            offset += 4 + 8*length
    return None, offset

with open('/opt/minecraft/world/level.dat','rb') as f:
    data = f.read()
# skip root tag header
offset = 0
if data[offset] != 0x0A:
    print('Unexpected format')
    sys.exit(1)
offset += 1
name_len = struct.unpack('>H', data[offset:offset+2])[0]
offset += 2 + name_len
seed = None
while offset < len(data):
    res, offset = read_tag(data, offset)
    if res and res[0] == 'seed':
        seed = res[1]
        break
if seed is None:
    print('Seed not found')
else:
    unsigned = seed & 0xFFFFFFFFFFFFFFFF
    print('Seed (signed):', seed)
    print('Seed (unsigned):', unsigned)
    print('Seed (hex):', hex(unsigned))
