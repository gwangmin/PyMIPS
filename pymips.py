'''
PyMIPS
'''

# registers
ZERO = 0
AT = 1
V0, V1 = 2, 3
A0, A1, A2, A3 = range(4, 8)
T0, T1, T2, T3, T4, T5, T6, T7 = range(8, 16)
S0, S1, S2, S3, S4, S5, S6, S7 = range(16, 24)
T8, T9 = 24, 25
K0, K1 = 26, 27
GP, SP, FP, RA = range(28, 32)


# utils
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

def bit_to_dec(bit, signed=False):
    '''
    Convert bit(s) to dec

    signed: signed or unsigned? default unsigned
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

def hex_to_bit(_hex):
    '''
    Hex to bit(s)
    '''
    bit = ''
    for h in _hex:
        b = bin(int('0x' + h, 16))[2:]
        bit += bit_ext(b, 4, sign=False)
    return bit

def bit_to_hex(bit):
    '''
    Bit(s) to hex
    '''
    _hex = ''
    for i in range(len(bit) // 4):
        si = 0 + (4*i)
        _hex += hex(int('0b' + bit[si:si+4], 2))[2:]
    return _hex

def hex_to_dec(_hex, signed=True):
    '''
    Hex to decimal

    signed: signed or unsigned. default signed.
    '''
    bit = hex_to_bit(_hex)
    return bit_to_dec(bit, signed=signed)

def dec_to_hex(dec, _len):
    '''
    Decimal to hex

    _len: hex length
    '''
    bit = dec_to_bit(dec, _len * 4)
    return bit_to_hex(bit)


# instructions
# decode
class RType:
    '''
    R type instruction composer
    op(6) | rs(5) | rt(5) | rd(5) | shamt(5) | funct(6)
    '''
    def __init__(self):
        '''
        Initialize all fields to None
        '''
        self.op, self.op_b = None, None
        self.rs, self.rs_b = None, None
        self.rt, self.rt_b = None, None
        self.rd, self.rd_b = None, None
        self.shamt, self.shamt_b = None, None
        self.funct, self.funct_b = None, None
        self.inst_b, self.inst_h = None, None

    def fill_dec(self, op, rs, rt, rd, shamt, funct):
        '''
        Fill fields with decimal
        
        all arg: decimal
        '''
        self.op = op
        self.rs = rs
        self.rt = rt
        self.rd = rd
        self.shamt = shamt
        self.funct = funct
        self.fill_with_dec()

    def fill_bit(self, op, rs, rt, rd, shamt, signed, funct):
        '''
        Fill fields with bit(s)
        all arg: bit(s)

        signed: shamt is signed?
        '''
        self.op_b = op
        self.rs_b = rs
        self.rt_b = rt
        self.rd_b = rd
        self.shamt_b = shamt
        self.funct_b = funct
        self.fill_with_bit(signed)

    def fill_with_dec(self):
        '''
        Encode decimal fields to bit(s)
        '''
        self.op_b = dec_to_bit(self.op, 6)
        self.rs_b = dec_to_bit(self.rs, 5)
        self.rt_b = dec_to_bit(self.rt, 5)
        self.rd_b = dec_to_bit(self.rd, 5)
        self.shamt_b = dec_to_bit(self.shamt, 5)
        self.funct_b = dec_to_bit(self.funct, 6)

    def fill_with_bit(self, signed):
        '''
        Fill decimal fields with bit(s)
        '''
        self.op = bit_to_dec(self.op_b, signed=False)
        self.rs = bit_to_dec(self.rs_b, signed=False)
        self.rt = bit_to_dec(self.rt_b, signed=False)
        self.rd = bit_to_dec(self.rd_b, signed=False)
        self.shamt = bit_to_dec(self.shamt_b, signed=signed)
        self.funct = bit_to_dec(self.funct_b, signed=False)

    def encode(self):
        '''
        Compose (binary/hex)instruction with binary fields.
        '''
        # 최종 인스트럭션을 2진수로(접두사 없이)
        self.inst_b = self.op_b + self.rs_b + self.rt_b + self.rd_b + self.shamt_b + self.funct_b
        # 최종 인스트럭션을 8자리 16진수로(접두사 없이)
        h = hex(int('0b' + self.inst_b, 2))[2:]
        self.inst_h = ('0' * (8 - len(h))) + h

    def decode_hex(self, signed):
        '''
        Decode hex instruction

        signed: shamt is signed?
        '''
        _hex = self.inst_h
        self.inst_b = hex_to_bit(_hex)

        self.op_b = self.inst_b[:6]
        self.rs_b = self.inst_b[6:6+5]
        self.rt_b = self.inst_b[11:11+5]
        self.rd_b = self.inst_b[16:16+5]
        self.shamt_b = self.inst_b[21:21+5]
        self.funct_b = self.inst_b[26:26+6]

        self.op = bit_to_dec(self.op_b, signed=False)
        self.rs = bit_to_dec(self.rs_b, signed=False)
        self.rt = bit_to_dec(self.rt_b, signed=False)
        self.rd = bit_to_dec(self.rd_b, signed=False)
        self.shamt = bit_to_dec(self.shamt_b, signed=signed)
        self.funct = bit_to_dec(self.funct_b, signed=False)


# decode
class IType:
    '''
    I type instruction composer
    op(6) | rs(5) | rt(5) | immediate(16)
    '''
    def __init__(self):
        '''
        Initialize all fields to None
        '''
        self.op, self.op_b = None, None
        self.rs, self.rs_b = None, None
        self.rt, self.rt_b = None, None
        self.im, self.im_b = None, None
        self.inst_b, self.inst_h = None, None

    def fill_dec(self, op, rs, rt, im):
        '''
        Fill fields with decimal
        
        all arg: decimal
        '''
        self.op = op
        self.rs = rs
        self.rt = rt
        self.im = im
        self.fill_with_dec()

    def fill_bit(self, op, rs, rt, im, signed):
        '''
        Fill fields with bit(s)
        all arg: bit(s)

        signed: im is signed?
        '''
        self.op_b = op
        self.rs_b = rs
        self.rt_b = rt
        self.im_b = im
        self.fill_with_bit(signed)

    def fill_with_dec(self):
        '''
        Encode decimal fields to bit(s)
        '''
        self.op_b = dec_to_bit(self.op, 6)
        self.rs_b = dec_to_bit(self.rs, 5)
        self.rt_b = dec_to_bit(self.rt, 5)
        self.im_b = dec_to_bit(self.im, 16)

    def fill_with_bit(self, signed):
        '''
        Fill decimal fields with bit(s)
        '''
        self.op = bit_to_dec(self.op_b, signed=False)
        self.rs = bit_to_dec(self.rs_b, signed=False)
        self.rt = bit_to_dec(self.rt_b, signed=False)
        self.im = bit_to_dec(self.im_b, signed=signed)

    def encode(self):
        '''
        Compose (binary/hex)instruction with binary fields.
        '''
        # 최종 인스트럭션을 2진수로(접두사 없이)
        self.inst_b = self.op_b + self.rs_b + self.rt_b + self.im_b
        # 최종 인스트럭션을 8자리 16진수로(접두사 없이)
        h = hex(int('0b' + self.inst_b, 2))[2:]
        self.inst_h = ('0' * (8 - len(h))) + h

    def decode_hex(self, signed):
        '''
        Decode hex instruction

        signed: im is signed?
        '''
        _hex = self.inst_h
        self.inst_b = hex_to_bit(_hex)

        self.op_b = self.inst_b[:6]
        self.rs_b = self.inst_b[6:6+5]
        self.rt_b = self.inst_b[11:11+5]
        self.im_b = self.inst_b[16:]

        self.op = bit_to_dec(self.op_b, signed=False)
        self.rs = bit_to_dec(self.rs_b, signed=False)
        self.rt = bit_to_dec(self.rt_b, signed=False)
        self.im = bit_to_dec(self.im_b, signed=signed)


# decode
class JType:
    '''
    J type instruction composer
    op(6) | addr(26)
    '''
    def __init__(self):
        '''
        Initialize all fields to None
        '''
        self.op, self.op_b = None, None
        self.addr, self.addr_b = None, None
        self.inst_b, self.inst_h = None, None

    def fill_dec(self, op, addr):
        '''
        Fill fields with decimal

        all arg: decimal
        '''
        self.op = op
        self.addr = addr
        self.fill_with_dec()

    def fill_bit(self, op, addr):
        '''
        Fill fields with bit(s)

        all arg: bit(s)
        '''
        self.op_b = op
        self.addr_b = addr
        self.fill_with_bit()

    def fill_with_dec(self):
        '''
        Encode decimal fields to bit(s)
        '''
        self.op_b = dec_to_bit(self.op, 6)
        self.addr_b = dec_to_bit(self.addr, 26)

    def fill_with_bit(self):
        '''
        Fill decimal fields with bit(s)
        '''
        self.op = bit_to_dec(self.op_b, signed=False)
        self.addr = bit_to_dec(self.addr_b, signed=False)

    def encode(self):
        '''
        Compose (binary/hex)instruction with binary fields.
        '''
        # 최종 인스트럭션을 2진수로(접두사 없이)
        self.inst_b = self.op_b + self.addr_b
        # 최종 인스트럭션을 8자리 16진수로(접두사 없이)
        h = hex(int('0b' + self.inst_b, 2))[2:]
        self.inst_h = ('0' * (8 - len(h))) + h

    def decode_hex(self):
        '''
        Decode hex instruction
        '''
        _hex = self.inst_h
        self.inst_b = hex_to_bit(_hex)

        self.op_b = self.inst_b[:6]
        self.addr_b = self.inst_b[6:]

        self.op = bit_to_dec(self.op_b, signed=False)
        self.addr = bit_to_dec(self.addr_b, signed=False)


if __name__ == "__main__":
    #result = RType(0, S2, S3, S1, 0, bit_to_dec('100000', signed=False)).inst_h
    result = dec_to_hex(-1945075712,8)
    print(result)
