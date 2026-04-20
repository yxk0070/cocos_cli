BASE64_KEYS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def compress_uuid(uuid_str):
    uuid_str = uuid_str.replace('-', '')
    if len(uuid_str) != 32:
        return uuid_str
    
    head = uuid_str[:5]
    tail = []
    for i in range(5, 32, 3):
        hex_val = int(uuid_str[i:i+3], 16)
        tail.append(BASE64_KEYS[hex_val >> 6])
        tail.append(BASE64_KEYS[hex_val & 0x3F])
        
    return head + ''.join(tail)

print(compress_uuid("8c599182-1234-1234-1234-1234567890ab"))
