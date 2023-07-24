# -*- coding: utf-8 -*-
"""
Created on Sun Jan 16 23:43:50 2022
@author: Kieffer
"""

import numpy as np


def gen_bin(x, n=16):
    """
    Generates the binary representation of 0 <= x < 1 on n bits.
    """

    # Binary representation of x
    if x == 0:
        return [0]
    else:
        b = []
        while n > 0:
            if x * 2 >= 1:
                b += [1]
                x = x * 2 - 1
            else:
                x = x * 2
                b += [0]
            n = n - 1
        return b


def gen_float(c):
    """
    Evaluates the floating-point number associated with the binary representation
    of the decimal part given by c.
    """

    x = 0;

    for i in range(0, len(c)):
        x += c[i] * 2 ** (-i - 1)

    return x


def arith_code_inf(x, p0, verbose=0):
    """
    Arithmetic encoder assuming infinite precision for encoding interval bounds.

    Inputs:
        x : sequence of bits to be encoded
        p0 : probability of emitting a zero by the source
        verbose : if set to 1, displays verbose code information
    """

    l = 0
    h = 1

    if verbose:
        print(f'Initial Interval: [l,h[ = [{l:.3f},{h:.3f}[')

    for i in range(0, len(x)):
        if x[i] == 0:
            l = l
            h = l + p0 * (h - l)
            if verbose:
                print(f'x({i})={x[i]}, resulting in [l,h[ = [{l:.8f},{h:.8f}[ (lower sub-interval)')
        else:
            l = l + p0 * (h - l)
            h = h
            if verbose:
                print(f'x({i})={x[i]}, resulting in [l,h[ = [{l:.8f},{h:.8f}[ (upper sub-interval)')

    if verbose:
        print(f'Final Interval [l,h[ = [{l:.8f},{h:.8f}[')

    m = (h + l) / 2
    if verbose:
        print(f'Midpoint:  m = {m:.8f}')
    lambd = np.ceil(-np.log2(h - l)) + 1
    if verbose:
        print(f'Number of code bits:  lambda = {lambd:.8f}')

    return gen_bin(m, lambd)


def arith_decode_inf(c, p0, N, verbose=0):
    """
    Arithmetic decoder assuming infinite precision for decoding interval bounds.

    Inputs:
        c : list of code bits
        p0 : probability of emitting a zero by the source
        N : length of the message to be decoded
        verbose : if set to 1, displays verbose code information
    """
    l = 0
    h = 1
    x = []

    m = gen_float(c)
    if verbose:
        print(f'Floating-point number associated with binary representation code\n {c} :\n c=', gen_float(c))

    for i in range(0, N):
        if verbose:
            print(f'[{l:.8f},{h:.8f}[ is divided into ')
            print(f'   [{l:.8f},{l + p0 * (h - l):.8f}[ or [{l + p0 * (h - l):.8f},{h:.8f}[')
        if (m >= l) & (m < l + p0 * (h - l)):
            if verbose:
                print(f'   m is in [{l:.8f},{l + p0 * (h - l):.8f}[ and x({i})=0')
            x.append(0)
            l = l;
            h = l + p0 * (h - l);
        else:
            if verbose:
                print(f'   m is in [{l + p0 * (h - l):.8f},{h:.8f}[ and x({i})=1')
            x.append(1)
            l = l + p0 * (h - l);
            h = h;
    return x


# Main program
print('Representation of 0.1: ', gen_bin(0.1, 16))

c = gen_bin(0.1, 16)

print(f'Floating-point number whose representation is {c}: ', gen_float(c))

# Arithmetic coding
x = [0, 0, 0, 1, 1, 1, 0, 0, 0]

# Encoding
c = arith_code_inf(x, 0.6, verbose=1)
# Decoding
x_hat = arith_decode_inf(c, 0.6, len(x), verbose=1)

print('Initial message: ', x)
print('Code: ', c)
print('Decoded message: ', x_hat)

# Longer sequences
p0 = 0.8
b = np.random.uniform(0, 1, 20)
x = [int(i >= p0) for i in b]

# Encoding
c = arith_code_inf(x, p0, verbose=1)
# Decoding
x_hat = arith_decode_inf(c, p0, len(x), verbose=1)

print('Initial message: ', x)
print('Code: ', c)
print('Decoded message: ', x_hat)
