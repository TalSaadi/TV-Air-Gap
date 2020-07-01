
def to_bits(string):
    """
    Convert string to bits list
    :param string: string to convert
    :return: bits list
    """
    result = []

    for char in string:
        bits = bin(ord(char))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(bit) for bit in bits])

    return result


def from_bits(bits):
    """
    Convert bits list to string
    :param bits: bits list to convert
    :return: string
    """
    if (len(bits) % 8) != 0:
        raise ValueError

    chars = []

    for b in range(int(len(bits) / 8)):
        byte = bits[b * 8: (b+1) * 8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))

    return ''.join(chars)
