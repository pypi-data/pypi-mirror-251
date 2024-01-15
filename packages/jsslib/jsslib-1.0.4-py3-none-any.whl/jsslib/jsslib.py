import os
import platform
import json
from ctypes import *

OS = platform.system()
if OS == "Windows":
    import win32api

class JSS:
    def __init__(self, log_level = 0, log_filename = ''):
        dll_name_jss = ''

        if OS == "Windows":
            dll_name_jss = 'jsslib.dll'
        elif OS == "Linux":
            dll_name_jss = 'libjsslib.so'
        else:
            dll_name_jss = 'libjsslib.dylib'
        self.log_level = log_level
        self.log_filename = log_filename
        self.buf_max_size = 1024 * 1024 * 10
        self.RetBuff = create_string_buffer(''.encode(), self.buf_max_size)
        self.is_init = False
        dll_file_jss = os.path.join(os.path.dirname(os.path.abspath(__file__)), dll_name_jss)
        self.library_jss = cdll.LoadLibrary(dll_file_jss)
        self.handle = None

        if OS == "Windows":
            self.dll_close = win32api.FreeLibrary
        elif OS == "Linux":
            try:
                stdlib = CDLL("")
            except OSError:
                stdlib = CDLL("libc.so")
            self.dll_close = stdlib.dlclose
            self.dll_close.argtypes = [c_void_p]
        else:
            self.dll_close = None

    def __del__(self):
        if self.handle is not None:
            self.Terminate()
        if self.dll_close is not None:
            self.dll_close(self.library_jss._handle)

    def CreateTable(self, cfg_filename, dat_pathname, out_pathname, seg_filename = ''):
        if not self.is_init:
            if (os.path.isfile(seg_filename)):
                seg_fullname = os.path.abspath(seg_filename)
            else:
                seg_fullname = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'base.lex')

            self.library_jss.JL_CreateTable.restype = c_int
            self.library_jss.JL_CreateTable.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_int, c_char_p]
            ret = self.library_jss.JL_CreateTable(cfg_filename.encode(), seg_fullname.encode(), dat_pathname.encode(), out_pathname.encode(), self.log_level, self.log_filename.encode())
            return ret
        return 0
    
    def LoadTable(self, filename):
        self.Terminate()

        self.is_init = True  
        self.library_jss.JL_Initialize.restype  = c_void_p
        self.library_jss.JL_Initialize.argtypes = [c_char_p, c_int, c_char_p]
        self.handle = self.library_jss.JL_Initialize(filename.encode(), self.log_level, self.log_filename.encode())
        return self.handle
    
    def RunSql(self, sql_statement):
        if self.is_init:
            self.library_jss.JL_RunSql.restype = c_int
            self.library_jss.JL_RunSql.argtypes = [c_void_p, c_char_p, c_char_p, c_int]
            str_len = self.library_jss.JL_RunSql(self.handle, sql_statement.encode(), self.RetBuff, self.buf_max_size)
            ret = string_at(self.RetBuff, str_len)
            json_data = json.loads(ret.decode())
            return json_data['results']
        return []
    
    def Terminate(self):
        if self.is_init:
            self.library_jss.JL_Terminate.argtypes = [c_void_p]
            self.library_jss.JL_Terminate(self.handle)
            self.is_init = False

if __name__ == '__main__':

    jss = JSS(log_level=1)
    jss.CreateTable('../../release/lang/table/zi.json', '../../../data/jss/lang/json/zi', '../../../data/jss/lang/table/zi')
    
    jss.LoadTable('../../../data/jss/lang/table/zi')
    print(jss.RunSql("SELECT TOP 10 id, Zi FROM zi WHERE PinYin = 'ding1' and id > 2;"))


