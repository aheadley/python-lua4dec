#!/usr/bin/env python
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

import argparse

from lua4dec.parser import Lua4File
from lua4dec.formatter import Lua4DebugFormatter

def lua4_decompile():
    parser = argparse.ArgumentParser(prog='lua4dec',
        description='Decompile Lua 4 bytecode files')
    parser.add_argument('source')
    parser.add_argument('dest')

    args = parser.parse_args()

    with open(args.source, 'rb') as lua_file:
        lua_obj = Lua4File.parse_stream(lua_file)
        formatter = Lua4DebugFormatter()
        with open(args.dest, 'w') as out_f:
            formatter.dump(lua_obj, out_f)

if __name__ == '__main__':
    lua4_decompile()
