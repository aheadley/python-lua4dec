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

from construct import *

class Lua4StringAdapter(Adapter):
    """Lua4 strings in the byte code have a null terminating byte, despite being
    pascal-style. PyConstruct doesn't handle this by default so we use this adapter
    to account for that.
    """
    def _decode(self, obj, context):
        return obj[:len(obj)-1]

    def _encode(self, obj, context):
        return obj + '\x00'

Lua4String = lambda name: Lua4StringAdapter(PascalString(name, length_field=SLInt32('length')))
Lua4Array = lambda subcon: PrefixedArray(subcon, length_field=SLInt32('length'))


Lua4Header = Struct('header',
    Const(ULInt8('format_id'), 0x1B),
    Magic('Lua'),
    ULInt8('version'),
    Flag('little_endian', default=True)
)

Lua4SelfCheck = Struct('self_check',
    ULInt8('size_int'),
    ULInt8('size_t'),
    ULInt8('size_instruction'),
    ULInt8('test_size_instruction'),
    ULInt8('test_size_op'),
    ULInt8('test_size_b'),
    ULInt8('size_number'),
    LFloat64('test_fp_number')
)

Lua4LocalVar        = Struct('local_var',
    Lua4String('name'),
    SLInt32('start_pc'),
    SLInt32('end_pc')
)
Lua4LineInfo        = SLInt32('line_info')
Lua4ChunkConstants  = Struct('constants',
    Lua4Array(Lua4String('string')),
    Lua4Array(LFloat64('number')),
    Lua4Array(LazyBound('function', lambda: Lua4Chunk))
)
Lua4Instruction     = ULInt32('instruction')

Lua4Chunk = Struct('code_chunk',
    Lua4String('source'),
    SLInt32('line_number'),
    SLInt32('num_params'),
    Flag('is_vararg'),
    SLInt32('max_stack_size'),
    Lua4Array(Lua4LocalVar),
    Lua4Array(Lua4LineInfo),
    Lua4ChunkConstants,
    Lua4Array(Lua4Instruction)
)

Lua4File = Struct('lua_file',
    Lua4Header,
    Lua4SelfCheck,
    Lua4Chunk
)
