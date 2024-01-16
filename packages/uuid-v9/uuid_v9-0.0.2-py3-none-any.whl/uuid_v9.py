import re
import random
import time

uuid_regex = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.IGNORECASE)
uuidv9_regex = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-9[0-9a-f]{3}-[0-9a-f]{4}-[0-9a-f]{12}$', re.IGNORECASE)

def calc_checksum(hex_string): # CRC-8
    data = [int(hex_string[i:i+2], 16) for i in range(0, len(hex_string), 2)]
    polynomial = 0x07
    crc = 0x00
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x80:
                crc = (crc << 1) ^ polynomial
            else:
                crc <<= 1
    return format(crc & 0xFF, 'x')
    # return format(crc & 0xF, 'x')

def verify_checksum(uuid):
    clean_uuid = uuid.replace('-', '')[0:30]
    checksum = calc_checksum(clean_uuid)
    return checksum == uuid[34:36]

# def verify_checksum(id):
#     clean_id = id.replace('-', '')
#     decimals = [int(char, 16) for char in clean_id[0:31]]
#     checksum = sum(decimals) % 16
#     return (format(checksum, 'x') == clean_id[31:32])

# def calc_checksum(string):
#     decimals = [int(char, 16) for char in string]
#     checksum = sum(decimals) % 16
#     return format(checksum, 'x')

def is_uuid(uuid, checksum=False):
    return isinstance(uuid, str) and uuid_regex.match(uuid) and (not checksum or verify_checksum(uuid))

def is_uuidv9(uuid, checksum=False):
    return isinstance(uuid, str) and uuidv9_regex.match(uuid) and (not checksum or verify_checksum(uuid))

def random_bytes(count):
    return ''.join(random.choice('0123456789abcdef') for _ in range(count))

base16_regex = re.compile(r'^[0-9a-fA-F]+$')

def is_base16(str):
    return bool(base16_regex.match(str))

def validate_prefix(prefix):
    if not isinstance(prefix, str):
        raise ValueError('Prefix must be a string')
    if len(prefix) > 8:
        raise ValueError('Prefix must be no more than 8 characters')
    if not is_base16(prefix):
        raise ValueError('Prefix must be only hexadecimal characters')

def add_dashes(str):
    return f'{str[:8]}-{str[8:12]}-{str[12:16]}-{str[16:20]}-{str[20:]}'

def uuid(prefix='', timestamp=True, version=True, checksum=False):
    if prefix:
        validate_prefix(prefix)
        prefix = prefix.lower()
    center = hex(int(time.time_ns() / 1000000))[2:] if timestamp else ''
    suffix = random_bytes(32 - len(prefix) - len(center) - (1 if version else 0) - (2 if checksum else 0))
    joined = prefix + center + suffix
    if version:
        joined = joined[:12] + '9' + joined[12:]
    if checksum:
        joined += calc_checksum(joined)
    return add_dashes(joined)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate a UUID v9.")
    parser.add_argument("--prefix", dest="prefix", default="", help="Include a prefix (default: '')")
    parser.add_argument("--unordered", dest="timestamp", action="store_false", help="Exclude timestamp (default: True)")
    parser.add_argument("--noversion", dest="version", action="store_false", help="Exclude version (default: True)")
    parser.add_argument("--checksum", dest="checksum", action="store_true", help="Include checksum (default: False)")
    args = parser.parse_args()
    print(uuid(args.prefix, args.timestamp, args.version, args.checksum))