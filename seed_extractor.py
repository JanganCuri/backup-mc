import struct, sys

def read_nbt(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
    i = 0
    if data[i] != 0x0A:
        return None
    i += 1
    name_len = struct.unpack('>H', data[i:i+2])[0]
    i += 2 + name_len
    while i < len(data):
        tag_type = data[i]
        i += 1
        if i + 2 > len(data):
            break
        n_len = struct.unpack('>H', data[i:i+2])[0]
        i += 2
        name = data[i:i+n_len].decode('utf-8', errors='ignore')
        i += n_len
        if tag_type == 0x04:
            value = struct.unpack('>q', data[i:i+8])[0]
            i += 8
            if name == 'RandomSeed':
                return value
        elif tag_type == 0x01:
            i += 1
        elif tag_type == 0x02:
            i += 2
        elif tag_type == 0x03:
            i += 4
        elif tag_type == 0x05:
            i += 4
        elif tag_type == 0x06:
            i += 8
        elif tag_type == 0x07:
            length = struct.unpack('>i', data[i:i+4])[0]
            i += 4 + length
        elif tag_type == 0x08:
            str_len = struct.unpack('>H', data[i:i+2])[0]
            i += 2 + str_len
        elif tag_type == 0x09:
            i += 1
            count = struct.unpack('>i', data[i:i+4])[0]
            i += 4
            break
        elif tag_type == 0x0A:
            break
        elif tag_type == 0x0B:
            length = struct.unpack('>i', data[i:i+4])[0]
            i += 4 + 4*length
        elif tag_type == 0x0C:
            length = struct.unpack('>i', data[i:i+4])[0]
            i += 4 + 8*length
        else:
            break
    return None

if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else '/opt/minecraft/world/level.dat'
    seed = read_nbt(path)
    if seed is None:
        print('Seed not found')
    else:
        unsigned = seed & 0xFFFFFFFFFFFFFFFF
        print('Seed (signed):', seed)
        print('Seed (unsigned):', unsigned)
        print('Seed (hex):', hex(unsigned))
