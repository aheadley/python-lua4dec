# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2015 Alex Headley <aheadley@waysaboutstuff.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from lua4dec.util import C_Enum, CAST_TO_UINT32

SIZE_INSTRUCTION    = 32
SIZE_B              =  9
SIZE_OP             =  6
SIZE_U              = SIZE_INSTRUCTION - SIZE_OP
POS_U               = SIZE_OP
POS_B               = SIZE_OP
POS_A               = SIZE_OP + SIZE_B
SIZE_A              = SIZE_INSTRUCTION - POS_A

MAXARG_U            = (1 << SIZE_U) - 1
MAXARG_S            = MAXARG_U >> 1

class OPCODE(C_Enum):
    # We assume that instructions are unsigned numbers.
    # All instructions have an opcode in the first 6 bits. Moreover,
    # an instruction can have 0, 1, or 2 arguments. Instructions can
    # have the following types:
    # type 0: no arguments
    # type 1: 1 unsigned argument in the higher bits (called `U')
    # type 2: 1 signed argument in the higher bits          (`S')
    # type 3: 1st unsigned argument in the higher bits      (`A')
    #       2nd unsigned argument in the middle bits      (`B')
    #
    # A signed argument is represented in excess K; that is, the number
    # value is the unsigned value minus K. K is exactly the maximum value
    # for that argument (so that -max is represented by 0, and +max is
    # represented by 2*max), which is half the maximum for the corresponding
    # unsigned argument.
    #
    # The size of each argument is defined in `llimits.h'. The usual is an
    # instruction with 32 bits, U arguments with 26 bits (32-6), B arguments
    # with 9 bits, and A arguments with 17 bits (32-6-9). For small
    # installations, the instruction size can be 16, so U has 10 bits,
    # and A and B have 5 bits each.
    #
    # arg key:
    #   K: U argument used as index to `kstr`
    #   J: S argument used as jump offset (relative to pc of next instruction)
    #   L: unsigned argument used as index of local var
    #   N: U argument used as index to `knum`
    # op name           id      args    stack (before)      stack (after)       side effects
    OP_END              =  0  # -       -                   (return)            no results
    OP_RETURN           =  1  # U       v_n-v_x (at u)      (return)            returns v_x-v_n

    OP_CALL             =  2  # A B     v_n-v_1 f(at a)     r_b-r_1             f(v1, ..., v_n)
    OP_TAILCALL         =  3  # A B     v_n-v_1 f(at a)     (return)            f(v1, ..., v_n)

    OP_PUSHNIL          =  4  # U       -                   IDT_Nil_1-IDT_Nil_u
    OP_POP              =  5  # U       a_u-a_1             -


    OP_PUSHINT          =  6  # S       -                   (Number)s
    OP_PUSHSTRING       =  7  # K       -                   KSTR[k]
    OP_PUSHNUM          =  8  # N       -                   KNUM[n]
    OP_PUSHNEGNUM       =  9  # N       -                   -KNUM[n]

    OP_PUSHUPVALUE      = 10  # U       -                   IDT_Closure[u]

    OP_GETLOCAL         = 11  # L       -                   LOC[l]
    OP_GETGLOBAL        = 12  # K       -                   VAR[KSTR[k]]

    OP_GETTABLE         = 13  # -       i t                 t[i]
    OP_GETDOTTED        = 14  # K       t                   t[KSTR[k]]
    OP_GETINDEXED       = 15  # L       t                   t[LOC[l]]
    OP_PUSHSELF         = 16  # K       t                   t t[KSTR[k]]

    OP_CREATETABLE      = 17  # U       -                   newarray(size = u)

    OP_SETLOCAL         = 18  # L       x                   -                   LOC[l]=x
    OP_SETGLOBAL        = 19  # K       x                   -                   VAR[KSTR[k]]=x
    OP_SETTABLE         = 20  # A B     v a_a-a_1 i t       (pops b values)     t[i]=v

    OP_SETLIST          = 21  # A B     v_b-v_1 t           t                   t[i+a*FPF]=v_i
    OP_SETMAP           = 22  # U       v_u k_u - v_1 k_1   t   t               t[k_i]=v_i

    OP_ADD              = 23  # -       y x                 x+y
    OP_ADDI             = 24  # S       x                   x+s
    OP_SUB              = 25  # -       y x                 x-y
    OP_MULT             = 26  # -       y x                 x*y
    OP_DIV              = 27  # -       y x                 x/y
    OP_POW              = 28  # -       y x                 x^y
    OP_CONCAT           = 29  # U       v_u-v_1             v1..-..v_u
    OP_MINUS            = 30  # -       x                   -x
    OP_NOT              = 31  # -       x                   (x==nil)? 1 : IDT_Nil

    OP_JMPNE            = 32  # J       y x                 -                   (x~=y)? PC+=s
    OP_JMPEQ            = 33  # J       y x                 -                   (x==y)? PC+=s
    OP_JMPLT            = 34  # J       y x                 -                   (x<y)? PC+=s
    OP_JMPLE            = 35  # J       y x                 -                   (x<=y)? PC+=s
    OP_JMPGT            = 36  # J       y x                 -                   (x>y)? PC+=s
    OP_JMPGE            = 37  # J       y x                 -                   (x>=y)? PC+=s

    OP_JMPT             = 38  # J       x                   -                   (x~=nil)? PC+=s
    OP_JMPF             = 39  # J       x                   -                   (x==nil)? PC+=s
    OP_JMPONT           = 40  # J       x                   (x~=nil)? x : -     (x~=nil)? PC+=s
    OP_JMPONF           = 41  # J       x                   (x==nil)? x : -     (x==nil)? PC+=s
    OP_JMP              = 42  # J       -                   -                   PC+=s

    OP_PUSHNILJMP       = 43  # -       -                   IDT_Nil             PC++

    OP_FORPREP          = 44  # J
    OP_FORLOOP          = 45  # J

    OP_LFORPREP         = 46  # J
    OP_LFORLOOP         = 47  # J

    OP_CLOSURE          = 48  # A B     v_b-v_1             IDT_Closure(KPROTO[a], v_1-v_b)

class INTP_DATA_TYPE(C_Enum):
    IDT_Nil             = 0
    IDT_Integral        = 1
    IDT_Float           = 2
    IDT_Char            = 3
    IDT_Table           = 4
    IDT_LocalVar        = 5
    IDT_Closure         = 6

class INTP_DATA_FLAG(C_Enum):
    IDF_IsALocalValue           = 1
    IDF_FunctionReturn          = 2
    IDF_FunctionReturnWithEQ    = 4

class OPERATOR:
    COMMENT             = '--'



NUM_OPCODES     = len(OPCODE)
ISJUMP          = lambda op: (OPCODE.OP_JMPNE <= op) and (op <= OPCODE.OP_JMP)

MASK1           = lambda n, p: CAST_TO_UINT32((~(0xFFFFFFFF << n)) << p)
MASK0           = lambda n, p: CAST_TO_UINT32(~MASK1(n, p))

OP_MASK         = MASK1(SIZE_OP, 0)

GET_OPCODE      = lambda i: i & OP_MASK
SET_OPCODE      = lambda i, o: (i & MASK0(SIZE_OP, 0)) | o

CREATE_U        = lambda o, u: o | (u << POS_U)
GETARG_U        = lambda i: i >> POS_U
SETARG_U        = lambda i, u: (i & MASK0(SIZE_U, POS_U)) | (u << POS_U)

# these are probably all wrong due to not overflowing as expected
CREATE_S        = lambda o, u: CREATE_U(o, s + MAXARG_S)
GETARG_S        = lambda i: GETARG_U(i) - MAXARG_S
SETARG_S        = lambda i, s: SETARG_U(i, s + MAXARG_S)

CREATE_AB       = lambda o, a, b: o | (a << POS_A) | (b << POS_B)

GETARG_A        = lambda i: i >> POS_A

GETARG_B        = lambda i: (i >> POS_B) & MASK1(SIZE_B, 0)
