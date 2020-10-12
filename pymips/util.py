'''
Util
'''

def handle_err(f, msg):
    '''
    Error handler
    '''
    return '[Error] ' + f.__name__ + ': ' + msg

def ones_complement(bits):
    '''
    Return 1's complement
    '''
    ones = ''
    for bit in bits:
        if bit == '0':
            ones += '1'
        else:
            ones += '0'
    return ones

def twos_complement(bits):
    '''
    Return 2's complement
    '''
    _len = len(bits)
    ones = ones_complement(bits)
    result = bin(int('0b' + ones, 2) + 1)[2:]
    if len(result) > _len:
        # if out of range
        l = len(result) - _len
        result = result[l:]
    return result

def dec_to_bit(dec, _len):
    '''
    Convert decimal to binary str(no prefix).

    dec: decimal int
    _len: bit(s) length
    '''
    if str(dec)[0] != '-':
        # positive
        bit = bin(dec)[2:]
        return bit_ext(bit, _len, sign=False)
    else:
        # negative
        _abs = bin(abs(dec))[2:]
        _abs = bit_ext(_abs, _len, sign=False)
        return twos_complement(_abs)

def bit_to_dec(bit, signed=True):
    '''
    Convert bit(s) to dec

    signed: signed or unsigned? default signed
    '''
    if (bit[0] == '0') or (signed == False):
        # positive or unsigned
        return int('0b' + bit, 2)
    else:
        # negative
        n = '-' + str(int('0b' + twos_complement(bit), 2))
        return int(n)

def bit_ext(bit, _len, sign=False):
    '''
    Bit extension

    bit: bit str
    _len: length
    sign: sign ext or zero ext. default zero ext.
    '''
    bit = str(bit)
    if sign == False:
        pad = '0'
    else:
        pad = bit[0]

    l = _len - len(bit)
    if 0 < l:
        bit = pad * l + bit
    elif l == 0:
        pass
    elif l < 0:
        return handle_err(bit_ext, 'out of range')
    
    return bit
