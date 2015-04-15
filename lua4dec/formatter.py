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

import logging

from lua4dec.lua_lang import *

logger = logging.getLogger('lua4dec.formatter')

class Lua4Formatter(object):
    def dump(self, lua_file, out_stream):
        raise NotImplemented()

class Lua4DebugFormatter(Lua4Formatter):
    INDENT_SPACE = 4

    def dump(self, lua_file, out_stream):
        out_stream.write('-- %r\n' % lua_file.header)
        out_stream.write('-- %r\n' % lua_file.self_check)
        self._dump_chunk(lua_file.code_chunk, out_stream)

    def _dump_chunk(self, lua_chunk, out_stream, level=0):
        SPACE = ' ' * (level * self.INDENT_SPACE)
        write_line = lambda s: out_stream.write(SPACE + s + '\n')

        write_line('-- @source {0:s}:{1:d}'.format(lua_chunk.source, lua_chunk.line_number))
        write_line('-- #params={0:d} var_arg={1} max_stack_size={2:d}'.format(
            lua_chunk.num_params, lua_chunk.is_vararg, lua_chunk.max_stack_size))

        write_line('-- Local Vars (%d) --' % len(lua_chunk.local_var))
        for i, lv in enumerate(lua_chunk.local_var):
            write_line(' [{3}] => {0} ({1}-{2})'.format(lv.name, lv.start_pc, lv.end_pc, i))

        write_line('-- Line Info (%d) --' % len(lua_chunk.line_info))
        for i, l in enumerate(lua_chunk.line_info):
            write_line(' [{0}] => 0x{1:08X}'.format(i, l & 0xFFFFFFFF))

        strings = lua_chunk.constants.string
        write_line('-- String Constants (%d) --' % len(strings))
        for i, s in enumerate(strings):
            write_line(' [{1}] => "{0}"'.format(s, i))

        numbers = lua_chunk.constants.number
        write_line('-- Number Constants (%d) --' % len(numbers))
        for n in numbers:
            write_line(' [{0}] => {1}'.format(i, n))

        write_line('-- Instructions (%d) -- ' % len(lua_chunk.instruction))
        for instruction in lua_chunk.instruction:
            write_line(' ' + self._format_instruction(lua_chunk, instruction))

        functions = lua_chunk.constants.function
        write_line('-- Function Constants (%d) --' % len(functions))
        for f in functions:
            self._dump_chunk(f, out_stream, level + 1)
            out_stream.write('\n')

    def _format_instruction(self, chunk, i):
        op_fmt = '-- 0x{0:08X} => [{1:02d}] {2:16s}'
        op = self._get_op(i)

        if op is OPCODE.OP_END:
            return '-- end --'
        if op is OPCODE.OP_RETURN:
            return 'return'

        if op is OPCODE.OP_CALL:
            A = GETARG_A(i)
            B = GETARG_B(i)
            op_fmt += 'A: {0} B: {1}'.format(A, B)

        if op is OPCODE.OP_PUSHINT:
            S = GETARG_S(i)
            return str(S)
        if op is OPCODE.OP_PUSHSTRING:
            K = GETARG_U(i)
            return '"%s"' % chunk.constants.string[K]
        if op in (OPCODE.OP_PUSHNUM, OPCODE.OP_PUSHNEGNUM):
            N = GETARG_U(i)
            num = chunk.constants.number[N]
            if op is OPCODE.OP_PUSHNEGNUM:
                num = -num
            return str(num)

        if op is OPCODE.OP_GETLOCAL:
            L = GETARG_U(i)
            return 'LOCAL[{0}]'.format(chunk.local_var[L].name)
        if op is OPCODE.OP_GETGLOBAL:
            U = GETARG_U(i)
            return 'GLOBAL[{0}]'.format(chunk.constants.string[U])

        if op is OPCODE.OP_SETLOCAL:
            L = GETARG_U(i)
            return 'LOCAL[{0}]='.format(chunk.local_var[L].name)
        if op is OPCODE.OP_SETGLOBAL:
            U = GETARG_U(i)
            return 'GLOBAL[{0}]='.format(chunk.constants.string[U])

        if op is OPCODE.OP_CLOSURE:
            A = GETARG_A(i)
            B = GETARG_B(i)
            op_fmt += 'A: {0} B: {1}'.format(A, B)

        return op_fmt.format(i, op.value, op.name)

    def _get_op(self, i):
        return OPCODE(GET_OPCODE(i))


class Lua4PrettyFormatter(Lua4Formatter):
    def dump(self, lua_file, out_stream):
        pass

