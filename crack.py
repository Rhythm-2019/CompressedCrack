# MIT License

# Copyright (c) 2022 Rhythm-2019

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Crack Rar or Zip file

This is a simple script to crack rar or zip file with password

Basic Logic:
* Generate a series of passwords based on user input or default parameters and try them repeatedly
* Improve efficiency with multi-processing

Usage:

Run follow command in you shell:

$ crack.py <filepath>

or 

$ crack.py <filepath> <start len> <max len> [character]

"""

import zipfile
import rarfile
import os
import sys
from threading import Thread
import argparse
from itertools import product
import time
import urllib.request
import shutil

parser = argparse.ArgumentParser(description='CompressedCrack', epilog='Use the -h for help')
parser.add_argument('-i','--input', help='Insert the file path of compressed file', required=True)
parser.add_argument('rules', nargs='*', help='<min> <max> <character>')

# Const Character
_DEFAULT_CHARACTER = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_+=~`[]{}|\\:;\"'<>,.?/"

# UnRAR.exe download path
_UNRAR_WIN32_DOWNLOAD_URL = "https://www.rarlab.com/rar/unrarw32.exe"

# UnRAR file name
_UNRAR_FILE_NAME_IN_WIN32 = "UnRAR.exe"
_UNRAR_FILE_NAME_IN_LINUX = "unrar"

class CmdAgrs(object):
    """Command args holder
    
    Attributes:
        type: file type(rar or zip)
        if_use_custom_rules: if user use custom rule
        start_length: password start length
        max_length: password max length
        character: passwprd character
        location: file path
    """
        
    def __init__(self, location: str, rule: list(str)) -> None:
        self.type = None
        self.if_use_custom_rules = False
        self.start_length = None
        self.max_length = None
        self.character = None
        self.location = None

        def error_handle(msg: str = None):
            if msg is not None:
                print(msg)
            parser.print_help()
            parser.exit()

        if not location:
            error_handle()
        if rule and (len(rule) != 2 or len(rule != 3)):
            error_handle('rule is <start length> <max length> [character]')

        # Check Rules
        self.location = location
        if rule:
            # Normal input: crack.py filepath start_len max_len [character]
            try:
                self.start_length = int(rule[0])
                self.max_length = int(rule[1])
            except ValueError:
                error_handle('start length or max length Value Error')
            if self.start_length > self.max_length:
                error_handle('start length should lower than max lengthLength Error')

            self.character = rule[2]
            self.if_use_custom_rules = True

        # Check File Exist
        if not os.path.isfile(self.location):
            print('No such file or directory: ',args[1])
            parser.exit()

        if os.path.splitext(self.location)[1] == ".rar" or os.path.splitext(self.location)[1]==".zip":
            self.type = os.path.splitext(self.location)[1]
        else:
            error_handle('file extension should be rar or zip')

        # Check charactor
        if self.character is None:
            self.character = _DEFAULT_CHARACTER
    
class Handler(object):
    """ Commpressed file brute handler

    Attrubutes:
        _start_time: start time
        _cmd_args: a instance of CmdArgs
        _file_crack: decompression algorithm
    """

    """ find proganm location, just find in current dir or PATH
    Args:
        progarm: progarm name
    Return:
        str: progarm abs path
    """
    @staticmethod
    def which(program: str) -> str:
        def is_exe(fpath):
            return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

        fpath, fname = os.path.split(program)
        if fpath:
            if is_exe(program):
                return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    return exe_file
        return None


    def __init__(self, cmd_args: CmdAgrs) -> None:
        self._start_time = None
        self._cmd_args = cmd_args
        self.result = False

        self._file_crack = zipfile.ZipFile(self.location) if self._cmd_args.type == '.zip' else rarfile.RarFile(self.location)

        if self._cmd_args.type == '.rar':
            self._download_unrar()
        

    def _download_unrar(self) -> None:
        if sys.platform == "linux" or sys.platform == "linux2":
            # linux
            if self.__class__.which(_UNRAR_FILE_NAME_IN_LINUX) is None:
                print("please install unrar")
                parser.exit()
        elif sys.platform == "win32":
            # Windows...
            if os.path.exists(_UNRAR_FILE_NAME_IN_WIN32) is None:
                with urllib.request.urlopen(_UNRAR_WIN32_DOWNLOAD_URL) as response, open(_UNRAR_FILE_NAME_IN_WIN32, 'wb') as out_file:
                    shutil.copyfileobj(response, out_file)
            rarfile.UNRAR_TOOL = _UNRAR_FILE_NAME_IN_WIN32
        else:
            print("just support windows and centos, y")
            parser.exit()

    def _brute(self, password: str) -> None:
        try:
            if self._cmd_args.type == '.zip':
                tryPass = password.encode()
            else:
                tryPass = password
            print(tryPass)
            self._file_crack.extractall(pwd=tryPass)
            # Success
            print('Complete')
            print('Time:',time.process_time() - self._start_time,'s')
            print('Password:',password)
            self.result = True
        except:
            # Failed
            pass

    def execute(self) -> None:
        self._start_time = time.process_time()
        print('Cracking...')
        if not self._cmd_args.if_use_custom_rules:
            length = 1
            while True:
                self._send_request(length)
                if self.result:
                    return
                length += 1
        else:
            for length in range(self._cmd_args.start_length, self._cmd_args.max_length + 1):
                self._send_request(length)
                if self.result:
                    return
            if not self.result:
                print('Cannot find password with this rules')
                return

    def _send_request(self, length: int) -> None:
        # Use porduct to avoid out of memory
        listPass = product(self._cmd_args.character, repeat=length)
        for Pass in listPass:
            tryPass = ''.join(Pass)
            # Multi Thread:
            # nThread = Thread(target=self.Brute, args=(tryPass, ))
            # nThread.start()
            # TODO GPU 加速、多进程
            # Single Thread: 
            self._brute(tryPass)
            if self.result:
                return
def main():
    args = parser.parse_args()
    handler = Handler(CmdAgrs(args[0], args[1]))
    handler.execute()
    
if __name__ == '__main__':
    main()