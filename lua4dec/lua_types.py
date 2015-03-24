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

from lua4dec.util import C_Enum


LUA_HEADER  = 'B3sBB'


class OPCODE(C_Enum):
    OP_END              =  0
    OP_RETURN           =  1

    OP_CALL             =  2
    OP_TAILCALL         =  3

    OP_PUSHNIL          =  4
    OP_POP              =  5

    OP_PUSHINT          =  6
    OP_PUSHSTRING       =  7
    OP_PUSHNUM          =  8
    OP_PUSHNEGNUM       =  9

    OP_PUSHUPVALUE      = 10

    OP_GETLOCAL         = 11
    OP_GETGLOBAL        = 12

    OP_GETTABLE         = 13
    OP_GETDOTTED        = 14
    OP_GETINDEXED       = 15
    OP_PUSHSELF         = 16

    OP_CREATETABLE      = 17

    OP_SETLOCAL         = 18
    OP_SETGLOBAL        = 19
    OP_SETTABLE         = 20

    OP_SETLIST          = 21
    OP_SETMAP           = 22

    OP_ADD              = 23
    OP_ADDI             = 24
    OP_SUB              = 25
    OP_MULT             = 26
    OP_DIV              = 27
    OP_POW              = 28
    OP_CONCAT           = 29
    OP_MINUS            = 30
    OP_NOT              = 31

    OP_JMPNE            = 32
    OP_JMPEQ            = 33
    OP_JMPLT            = 34
    OP_JMPLE            = 35
    OP_JMPGT            = 36
    OP_JMPGE            = 37

    OP_JMPT             = 38
    OP_JMPF             = 39
    OP_JMPONT           = 40
    OP_JMPONF           = 41
    OP_JMP              = 42

    OP_PUSHNILJMP       = 43

    OP_FORPREP          = 44
    OP_FORLOOP          = 45

    OP_LFORPREP         = 46
    OP_LFORLOOP         = 47

    OP_CLOSURE          = 48


NUM_OPCODES     = len(OPCODE)
ISJUMP          = lambda op: (OPCODE.OP_JMPNE <= op) and (op <= OPCODE.OP_JMP)
