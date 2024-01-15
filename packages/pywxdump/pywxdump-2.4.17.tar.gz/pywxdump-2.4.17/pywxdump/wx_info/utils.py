# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         utils.py
# Description:  
# Author:       xaoyaoo
# Date:         2023/12/25
# -------------------------------------------------------------------------------
import re
import sys

import pymem
from win32com.client import Dispatch
import hmac
import hashlib


def verify_key(key, wx_db_path):
    KEY_SIZE = 32
    DEFAULT_PAGESIZE = 4096
    DEFAULT_ITER = 64000
    with open(wx_db_path, "rb") as file:
        blist = file.read(5000)
    salt = blist[:16]
    byteKey = hashlib.pbkdf2_hmac("sha1", key, salt, DEFAULT_ITER, KEY_SIZE)
    first = blist[16:DEFAULT_PAGESIZE]

    mac_salt = bytes([(salt[i] ^ 58) for i in range(16)])
    mac_key = hashlib.pbkdf2_hmac("sha1", byteKey, mac_salt, 2, KEY_SIZE)
    hash_mac = hmac.new(mac_key, first[:-32], hashlib.sha1)
    hash_mac.update(b'\x01\x00\x00\x00')

    if hash_mac.digest() != first[-32:-12]:
        return False
    return True


def get_exe_version(file_path):
    """
    获取 PE 文件的版本号
    :param file_path:  PE 文件路径(可执行文件)
    :return: 如果遇到错误则返回
    """
    file_version = Dispatch("Scripting.FileSystemObject").GetFileVersion(file_path)
    return file_version


def find_all(c: bytes, string: bytes, base_addr=0):
    """
    查找字符串中所有子串的位置
    :param c: 子串 b'123'
    :param string: 字符串 b'123456789123'
    :return:
    """
    return [base_addr + m.start() for m in re.finditer(re.escape(c), string)]


# 获取exe文件的位数
def get_exe_bit(file_path):
    """
    获取 PE 文件的位数: 32 位或 64 位
    :param file_path:  PE 文件路径(可执行文件)
    :return: 如果遇到错误则返回 64
    """
    try:
        with open(file_path, 'rb') as f:
            dos_header = f.read(2)
            if dos_header != b'MZ':
                print('get exe bit error: Invalid PE file')
                return 64
            # Seek to the offset of the PE signature
            f.seek(60)
            pe_offset_bytes = f.read(4)
            pe_offset = int.from_bytes(pe_offset_bytes, byteorder='little')

            # Seek to the Machine field in the PE header
            f.seek(pe_offset + 4)
            machine_bytes = f.read(2)
            machine = int.from_bytes(machine_bytes, byteorder='little')

            if machine == 0x14c:
                return 32
            elif machine == 0x8664:
                return 64
            else:
                print('get exe bit error: Unknown architecture: %s' % hex(machine))
                return 64
    except IOError:
        print('get exe bit error: File not found or cannot be opened')
        return 64


def pattern_scan_all(handle, pattern, *, return_multiple=False, find_num=100):
    next_region = 0
    found = []
    user_space_limit = 0x7FFFFFFF0000 if sys.maxsize > 2 ** 32 else 0x7fff0000
    while next_region < user_space_limit:
        try:
            next_region, page_found = pymem.pattern.scan_pattern_page(
                handle,
                next_region,
                pattern,
                return_multiple=return_multiple
            )
        except Exception as e:
            print(e)
            break
        if not return_multiple and page_found:
            return page_found
        if page_found:
            found += page_found
        if len(found) > find_num:
            break
    return found
