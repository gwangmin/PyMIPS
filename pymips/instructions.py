'''
Instructions
'''

from .util import dec_to_bit

class RType:
    '''
    R type instruction composer
    '''
    def __init__(self, op, rs, rt, rd, shamt, funct):
        '''
        op(6) | rs(5) | rt(5) | rd(5) | shamt(5) | funct(6)
        all arg: decimal
        '''
        self.op = op
        self.rs = rs
        self.rt = rt
        self.rd = rd
        self.shamt = shamt
        self.funct = funct
        self.compile()

    def compile(self):
        '''
        Compose (binary/hex)instruction with decimal fields.
        '''
        op_b = dec_to_bit(self.op, 6)
        rs_b = dec_to_bit(self.rs, 5)
        rt_b = dec_to_bit(self.rt, 5)
        rd_b = dec_to_bit(self.rd, 5)
        shamt_b = dec_to_bit(self.shamt, 5)
        funct_b = dec_to_bit(self.funct, 6)
    
        # 최종 인스트럭션을 2진수로(접두사 없이)
        self.inst_b = op_b + rs_b + rt_b + rd_b + shamt_b + funct_b
        # 최종 인스트럭션을 8자리 16진수로(접두사 없이)
        h = hex(int('0b' + self.inst_b, 2))[2:]
        self.inst_h = ('0' * (8 - len(h))) + h


class IType:
    '''
    I type instruction composer
    '''
    def __init__(self, op, rs, rt, im):
        '''
        op(6) | rs(5) | rt(5) | immediate(16)
        all arg: decimal
        '''
        self.op = op
        self.rs = rs
        self.rt = rt
        self.im = im
        self.compile()

    def compile(self):
        '''
        Compose (binary/hex)instruction with decimal fields.
        '''
        op_b = dec_to_bit(self.op, 6)
        rs_b = dec_to_bit(self.rs, 5)
        rt_b = dec_to_bit(self.rt, 5)
        im_b = dec_to_bit(self.im, 16)
    
        # 최종 인스트럭션을 2진수로(접두사 없이)
        self.inst_b = op_b + rs_b + rt_b + im_b
        # 최종 인스트럭션을 8자리 16진수로(접두사 없이)
        h = hex(int('0b' + self.inst_b, 2))[2:]
        self.inst_h = ('0' * (8 - len(h))) + h


class JType:
    '''
    J type instruction composer
    '''
    def __init__(self, op, addr):
        '''
        op(6) | addr(26)
        all arg: decimal
        '''
        self.op = op
        self.addr = addr
        self.compile()

    def compile(self):
        '''
        Compose (binary/hex)instruction with decimal fields.
        '''
        op_b = dec_to_bit(self.op, 6)
        addr_b = dec_to_bit(self.addr, 26)

        # 최종 인스트럭션을 2진수로(접두사 없이)
        self.inst_b = op_b + addr_b
        # 최종 인스트럭션을 8자리 16진수로(접두사 없이)
        h = hex(int('0b' + self.inst_b, 2))[2:]
        self.inst_h = ('0' * (8 - len(h))) + h
