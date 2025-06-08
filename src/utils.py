# ------------------------
# Useful constants
# ------------------------
# Not exhaustive, but supported by both the M3Y and GM65
common_baud_rates = [
    '9600',
    '14400',
    '19200',
    '38400',
    '57600',
    '115200',
]

# ------------------------
# Utility Functions
# ------------------------
def compute_crc16_xmodem(data: bytes) -> bytes:
    crc = 0
    for byte in data:
        for i in range(7, -1, -1):
            crc *= 2
            if (crc & 0x10000) != 0:
                crc ^= 0x11021
            if (byte & (1 << i)) != 0:
                crc ^= 0x1021
    crc &= 0xFFFF
    return crc.to_bytes(2, byteorder='big')

def check_crc16_xmodem(data_with_crc: bytes) -> bool:
    if len(data_with_crc) < 3:
        return False
    data = data_with_crc[:-2]
    received_crc = data_with_crc[-2:]
    calculated_crc = compute_crc16_xmodem(data)
    return received_crc == calculated_crc

def compute_bcc(data: bytes) -> bytes:
    bcc = 0
    for byte in data:
        bcc ^= byte
    return bytes([bcc])

def check_bcc(data_with_bcc: bytes) -> bool:
    if len(data_with_bcc) < 2:
        return False
    data = data_with_bcc[:-1]
    received_bcc = data_with_bcc[-1:]
    calculated_bcc = compute_bcc(data)
    return received_bcc == calculated_bcc

def set_bit(val, bit): return val | (1 << bit)
def clear_bit(val, bit): return val & ~(1 << bit)
def toggle_bit(val, bit): return val ^ (1 << bit)
def check_bit(val, bit): return (val >> bit) & 1
