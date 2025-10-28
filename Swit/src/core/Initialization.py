#MIT License

#Copyright (c) 2025 kenftr

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

import os
from Swit.src.handler.file.path_manager import path
async def initialization():
    """
    VI:
        Tự tạo folder cần thiết để Swit hoạt động nếu chưa có
    EN:
        Automatically create the necessary folder for Swit to operate if it does not exist
    """
    root = path.root()
    if not os.path.exists(os.path.join(root,'cache')):
        os.makedirs(name=f'{root}/cache',exist_ok=True)
    if not os.path.exists(os.path.join(root,'logs')):
        os.makedirs(name=f'{root}/logs',exist_ok=True)
    if not os.path.exists(os.path.join(root,'plugins')):
        os.makedirs(name=f'{root}/plugins',exist_ok=True)
    if not os.path.exists(os.path.join(root,'plugins','Plugin configs')):
        os.makedirs(name=f'{root}/plugins/Plugin configs',exist_ok=True)