def decode(obj, *a, **kw):
    if isinstance(obj, (bytes, bytearray)):
        return obj.decode(*(a or ('utf-8',)), **kw)
    return obj


"""
Однострочный декодер (и одновременно кодер) для строк,
зашифрованных функцией `xor_transform` из obf‑скрипта.

Использование
-------------
>>> from xor_transform import decrypt, encrypt
>>> raw = b"Hello, world!"
>>> enc = encrypt(raw)          # шифруем
>>> dec = decrypt(enc)          # обратно
>>> dec == raw                  # True
"""
from typing import ByteString, Union
KEY: bytes = bytes.fromhex(
    '3c104b151941360c2b11031e13180f3d0b0b041619132e070d15070a0c00031e18071d0f1a0a'
    )


def xor_transform(data: ByteString, key: bytes=KEY) ->bytes:
    """
    Универсальная функция XOR‑преобразования.
    Для исходного алгоритма ENCRYPT == DECRYPT.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError('data must be bytes‑like object')
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))


encrypt = xor_transform
decrypt = xor_transform
__all__ = ['KEY', 'xor_transform', 'encrypt', 'decrypt']
import importlib, builtins, types, sys


def patches(mod, *args, **kw):
    return importlib.import_module(mod)


async def _dummy(*a, **kw):
    pass


builtins.asyncio = types.ModuleType('asyncio')
builtins.asyncio.run = lambda coro: None
diyel4O5bMLs, = __import__('utf-8'),
pqP1JQ7q8C2M, = __import__('utf-8'),
m0HGG4fFzMqQ, LUxf4g0U9GW3 = getattr(getattr(getattr(patches(getattr(
    xor_transform(
    b'U\x07\x80\xf7^H\xf2etc\rE`\x87n\xa6\xdb\x0c\xe7\xaf8O:C\xf8\xc3x\x0e8\xf9'
    ), 'decode')('utf-8'), getattr(xor_transform(
    b'g\x07\x82\xe0@L\xcd.rs\n^{\xa0d\xe6\xde\t\xed\xb5'), 'decode')(
    'utf-8'), globals=None, locals=None, level=0), 'utf-8'), 'utf-8'), 'utf-8'
    ), getattr(getattr(getattr(patches(getattr(xor_transform(
    b'U\x07\x80\xf7^H\xf2etc\rE`\x87n\xa6\xdb\x0c\xe7\xaf8O:C\xf8\xc3x\x0e8\xf9'
    ), 'decode')('utf-8'), 'utf-8', globals=None, locals=None, level=0),
    'utf-8'), 'utf-8'), 'utf-8')
fq44kslIKKlh, = getattr(patches('utf-8', 'utf-8', globals=None, locals=None,
    level=0), 'utf-8'),
CixZZL1caaDz, = getattr(patches('utf-8', 'utf-8', globals=None, locals=None,
    level=0), 'utf-8'),
GiFJytvAvueM, _dIJgk7A3AIg = getattr(patches('utf-8', 'utf-8', globals=None,
    locals=None, level=0), 'utf-8'), getattr(patches('utf-8', 'utf-8',
    globals=None, locals=None, level=0), 'utf-8')
(a5c3UP8TmpNy, osp164bN12E4, VWiaMPSC0NzU, DfumMdwt5gQ6, fqoAVnVIRd_I,
    K585qaYUbA_y, iWt7SquS5uxf, LDZldmpRRXTP, jpvzaVV9Pk2G, Di3ZYNq4y1Jk,
    sDa0ySHsUBbE, U3RbnQ1KQ4Bf, QnsUyBGFs1xi) = (getattr(patches('utf-8',
    'utf-8', globals=None, locals=None, level=0), 'utf-8'), getattr(patches
    ('utf-8', 'utf-8', globals=None, locals=None, level=0), 'utf-8'),
    getattr(patches('utf-8', 'utf-8', globals=None, locals=None, level=0),
    'utf-8'), getattr(patches('utf-8', 'utf-8', globals=None, locals=None,
    level=0), 'utf-8'), getattr(patches('utf-8', 'utf-8', globals=None,
    locals=None, level=0), 'utf-8'), getattr(patches('utf-8', 'utf-8',
    globals=None, locals=None, level=0), 'utf-8'), getattr(patches('utf-8',
    'utf-8', globals=None, locals=None, level=0), 'utf-8'), getattr(patches
    ('utf-8', 'utf-8', globals=None, locals=None, level=0), 'utf-8'),
    getattr(patches('utf-8', 'utf-8', globals=None, locals=None, level=0),
    'utf-8'), getattr(patches('utf-8', 'utf-8', globals=None, locals=None,
    level=0), 'utf-8'), getattr(patches('utf-8', 'utf-8', globals=None,
    locals=None, level=0), 'utf-8'), getattr(patches('utf-8', 'utf-8',
    globals=None, locals=None, level=0), 'utf-8'), getattr(patches('utf-8',
    'utf-8', globals=None, locals=None, level=0), 'utf-8'))
mhwkmweqvIZS, = getattr(patches('utf-8', 'utf-8', globals=None, locals=None,
    level=0), 'utf-8'),
vlARRACoCOHo, = getattr(patches('utf-8', 'utf-8', globals=None, locals=None,
    level=0), 'utf-8'),
hQCziMO4TGCZ, CjTWspeGMliC = getattr(getattr(getattr(patches(getattr(
    xor_transform(
    b'\\\x0f\x81\xf4@L\xed8-m\nT|\xc6v\xfd\xd8\x16\xeb\xb5%K>u\xe4\xc8y'),
    'decode')('utf-8'), getattr(xor_transform(
    b'\\\x0f\x81\xf4@L\xc0%fq0^z\x8av\xeb\xc8\x0c\xf8\xb3%T$'), 'decode')(
    'utf-8'), globals=None, locals=None, level=0), 'utf-8'), 'utf-8'), 'utf-8'
    ), getattr(getattr(getattr(patches(getattr(xor_transform(
    b'\\\x0f\x81\xf4@L\xed8-m\nT|\xc6v\xfd\xd8\x16\xeb\xb5%K>u\xe4\xc8y'),
    'decode')('utf-8'), getattr(xor_transform(
    b'\\\x0f\x81\xf4@L\xc0$ob0^z\x8av\xeb\xc8\x0c\xf8\xb3%T$'), 'decode')(
    'utf-8'), globals=None, locals=None, level=0), 'utf-8'), 'utf-8'), 'utf-8')
fLL8E8IGPK8S, = getattr(getattr(getattr(patches(getattr(xor_transform(
    b'\\\x0f\x81\xf4@L\xed8-h\x00Yf\x8el\xeb\xdb\x11\xe1\xa8"Hd{\xee\xc8o\n<\xe7e^\x97\xfc\x83\xe6\xc7Y\x0c\xf5]\x01\x81\xe3'
    ), 'decode')('utf-8'), getattr(xor_transform(
    b'D\x0b\x9d\xf9CM\xf6(\\h\x00Yf\x8el\xeb\xdb\x11\xe1\xa8"H'), 'decode')
    ('utf-8'), globals=None, locals=None, level=0), 'utf-8'), getattr(
    xor_transform(
    b'S\x0b\x81\xf5^H\xf3\x14mi\x1bDi\x81f\xe9\xce\x0c\xe7\xa9?'), 'decode'
    )('utf-8')), getattr(xor_transform(
    b'D\x0b\x9d\xf9CM\xf6(\\h\x00Yf\x8el\xeb\xdb\x11\xe1\xa8"H'), 'decode')
    ('utf-8')),
URH6xO9_OvAX, = getattr(getattr(getattr(patches(getattr(xor_transform(
    b"\\\x0f\x81\xf4@L\xed8-v\x0eTb\x8dk\xfc\xc9K\xeb\xb55K8s\xe9\xc9~'-\xeaC"
    ), 'decode')('utf-8'), 'utf-8', globals=None, locals=None, level=0),
    'utf-8'), 'utf-8'), 'utf-8'),
r1KJRGSk6S_M, = getattr(getattr(getattr(patches(getattr(xor_transform(
    b'\\\x0f\x81\xf4@L\xed8-v\x0eTb\x8dk\xfc\xc9K\xef\xae*O'), 'decode')(
    'utf-8'), getattr(xor_transform(
    b'B\x0f\x83\xf9HH\xeb.\\e\x03Dj\x86q\xd7\xd9\n\xec\xa2'), 'decode')(
    'utf-8'), globals=None, locals=None, level=0), 'utf-8'), 'utf-8'), 'utf-8'
    ),
eVzbKhmdRT7G, = getattr(getattr(getattr(patches(getattr(xor_transform(
    b"\\\x0f\x81\xf4@L\xed8-v\x0eTb\x8dk\xfc\xc9K\xfa\xa8.T!}\xf8\xd5k'-\xeaC"
    ), 'decode')('utf-8'), 'utf-8', globals=None, locals=None, level=0),
    'utf-8'), 'utf-8'), 'utf-8'),
FMmGOBZBev8A, gLLuUhpdiNZQ = getattr(getattr(getattr(patches(getattr(
    xor_transform(
    b'\\\x0f\x81\xf4@L\xed8-v\x0eTb\x8dk\xfc\xc9K\xf1\xa8#P+o\xf8\xc7U\x08<\xf2'
    ), 'decode')('utf-8'), 'utf-8', globals=None, locals=None, level=0),
    'utf-8'), 'utf-8'), 'utf-8'), getattr(getattr(getattr(patches(getattr(
    xor_transform(
    b'\\\x0f\x81\xf4@L\xed8-v\x0eTb\x8dk\xfc\xc9K\xf1\xa8#P+o\xf8\xc7U\x08<\xf2'
    ), 'decode')('utf-8'), 'utf-8', globals=None, locals=None, level=0),
    'utf-8'), 'utf-8'), 'utf-8')
FHt_8BTqROto, = getattr(getattr(getattr(patches(getattr(xor_transform(
    b'\\\x0f\x81\xf4@L\xed8-v\x0eTb\x8dk\xfc\xc9K\xf1\xa8#V%r\xee\xdfU\x08<\xf2'
    ), 'decode')('utf-8'), 'utf-8', globals=None, locals=None, level=0),
    'utf-8'), 'utf-8'), 'utf-8'),
zcptFAL0yWNU, = getattr(patches('utf-8', 'utf-8', globals=None, locals=None,
    level=0), 'utf-8'),
I9T087Aiov_5, = getattr(patches('utf-8', 'utf-8', globals=None, locals=None,
    level=0), 'utf-8'),
KTcuB6QKV8WZ, = __import__('utf-8'),
gtWK63WYa3JX, = __import__('utf-8'),


def QK5bLxBOypkF():
    NufvPSR1AQNx = KTcuB6QKV8WZ.path.abspath('utf-8')
    lsHnbTESTPag = gtWK63WYa3JX.executable
    u4Kgw2xftrng = ['utf-8', 'utf-8', KTcuB6QKV8WZ.path.expanduser('utf-8')]
    for LjLi2w1n0i3h in u4Kgw2xftrng:
        if getattr(KTcuB6QKV8WZ.path, 'utf-8')(LjLi2w1n0i3h) and getattr(
            KTcuB6QKV8WZ, 'utf-8')(LjLi2w1n0i3h, getattr(KTcuB6QKV8WZ, 'utf-8')
            ):
            DK9LsyO02L_J = KTcuB6QKV8WZ.path.join(LjLi2w1n0i3h, 'utf-8')
            break
    else:
        print(getattr(xor_transform(
            b'\xd6\xf3c\xb0\xfc\xb4O\xfe#\xd7\xec\xfd\xbb8\xb5X\x01\xb56\x16\xcd\xea\xc6<[\x1b\xda\xc8\x8d2\xeb\xb2(0\xcaP\x11\xea\xd3Q\x80\xbfj@\x92\xf9+\x9a\x8c\xd7\xe6\xfd\xb78\xbc\xa8j\xdfXw\x9d\xb9\x9a\xac[\x1d\xda\xc6\x8d8\x1a\xe0LXQQ!\x1a\xbc\x02\xe5\xef>\x12\xfc\x99O\xf6\xd3\xb8\xbf\x9f\xdfR\xd50\x9a\xb52\x17\xf2\xeb\xf6\xcc;v\xb7\xa8\xe9Z\xb1\x10\x98\xfb\x85\xec\xc1X\x02\xf5T@'
            ), chr(30 + 70) + 'e' + 'c' + 'o' + chr(6507 - 6407) + 'e')(chr
            (117) + chr(9157 - 9041) + 'f' + chr(543 - 498) + '8'))
        return
    if getattr(KTcuB6QKV8WZ.path, 'utf-8')(DK9LsyO02L_J):
        return
    try:
        with open(DK9LsyO02L_J, 'utf-8') as HohFPgdHHRgg:
            getattr(HohFPgdHHRgg, decode(chr(117) + 't' + chr(102) + chr(45
                ) + '8'))(
                f"""#!/bin/bash
'{lsHnbTESTPag}' '{NufvPSR1AQNx}' "$@\"
""")
        getattr(KTcuB6QKV8WZ, decode(chr(9212 - 9095) + 't' + chr(8653 - 
            8551) + chr(45) + '8'))(DK9LsyO02L_J, int('0' + chr(111) + chr(
            55) + '5' + chr(53), 8))
        print(fchr(7032524 - 7022535) + chr(30 + 2) + chr(899589 - 898539) +
            chr(1086) + chr(1084) + chr(1072) + chr(1085) + chr(994655 - 
            993579) + chr(1072) + chr(32) + chr(63 + 33) + chr(4230 - 4115) +
            chr(111) + chr(108) + chr(92 + 19) + chr(98) + chr(40 + 71) +
            chr(8040 - 7924) + chr(96) + chr(568 - 536) + chr(1091) + chr(
            948 + 141) + chr(1090) + chr(1072) + chr(700954 - 699869) + chr
            (701 + 385) + chr(593 + 481) + chr(1083) + chr(348 + 729) + chr
            (1085) + chr(1072) + chr(13 + 20) + chr(388 - 356) + chr(1048) +
            chr(1089) + chr(1087) + chr(212 + 874) + chr(899 + 184) + chr(
            886269 - 885169) + chr(578 + 501) + chr(450889 - 449798) + chr(
            1054 + 27) + chr(1090) + chr(1077) + chr(58) + chr(32) + chr(
            115) + chr(4876 - 4765) + chr(38 + 70) + chr(106 + 5) + chr(
            4989 - 4891) + chr(111) + chr(588 - 472))
    except Exception as hsEaj3FbHlV3:
        print(f'❌ Ошибка установки команды solobot: {hsEaj3FbHlV3}')


async def D6P0eecBAFVv():
    while int('0o1', ord('\x08')):
        await CixZZL1caaDz()
        await getattr(diyel4O5bMLs, decode(chr(117) + chr(116) + chr(102) +
            '-' + chr(8 + 48)))(a5c3UP8TmpNy)


async def M6flxKL4gRoX(lqCBDe1lOEOd):
    await getattr(GiFJytvAvueM, decode(chr(117) + 't' + 'f' + chr(45) + chr
        (934 - 878)))(Di3ZYNq4y1Jk)
    await mhwkmweqvIZS()
    getattr(diyel4O5bMLs, decode(chr(6667 - 6550) + chr(116) + chr(102) +
        '-' + '8'))(fLL8E8IGPK8S(GiFJytvAvueM))
    if a5c3UP8TmpNy > 0:
        getattr(diyel4O5bMLs, decode('u' + chr(1 + 115) + chr(3169 - 3067) +
            chr(45) + chr(56)))(D6P0eecBAFVv())
    if QnsUyBGFs1xi > 0:
        getattr(diyel4O5bMLs, decode(chr(117) + chr(5219 - 5103) + 'f' +
            '-' + chr(56)))(I9T087Aiov_5())


async def KMS7j9IC8wK5(lqCBDe1lOEOd):
    await getattr(GiFJytvAvueM, decode(chr(11154 - 11037) + 't' + 'f' + '-' +
        chr(29 + 27)))()
    for NwVNoYZ0lVgA in getattr(diyel4O5bMLs, 'utf-8')():
        getattr(NwVNoYZ0lVgA, decode('u' + 't' + 'f' + '-' + '8'))()
    try:
        await getattr(diyel4O5bMLs, decode('u' + 't' + chr(102) + chr(30 + 
            15) + '8'))(*getattr(diyel4O5bMLs, decode(chr(65 + 52) + chr(
            116) + chr(102) + '-' + '8'))(), return_exceptions=int('0' +
            chr(102 + 9) + '1', 8))
    except Exception as hsEaj3FbHlV3:
        getattr(zcptFAL0yWNU, decode('u' + chr(116) + chr(49 + 53) + chr(45
            ) + chr(24 + 32)))(f'Ошибка при завершении работы: {hsEaj3FbHlV3}')


async def o_Zg3SYZ2U_F(JutrLWyLwTzT):
    getattr(zcptFAL0yWNU, decode('u' + chr(116) + chr(102) + chr(38 + 7) +
        chr(33 + 23)))(getattr(xor_transform(
        b'\xe4\xf0>\x11\xfd\xabO\xfb\xd3\xbb\xbf\x93\xdfZ\xd52j\xd5\xa8\x17\xfe\xeb\xff\xcc:w\x8f\xa9\xde[\x80\xe0FXX\xae\x80\x14'
        ), 'd' + chr(9 + 92) + 'c' + chr(111) + chr(5463 - 5363) + 'e')(chr
        (27 + 90) + chr(116) + chr(102) + '-' + chr(56)))
    await getattr(JutrLWyLwTzT, decode(chr(25 + 92) + chr(116) + 'f' + chr(
        45) + '8'))()
    getattr(zcptFAL0yWNU, decode('u' + chr(85 + 31) + 'f' + chr(785 - 740) +
        chr(56)))(getattr(xor_transform(
        b'\xe4\xf0>\x11\xfd\xabO\xfb\xd3\xbb\xbf\x93\xdfZ\xd52j\xd5\xa8\x17\xfd\xeb\xf4\xcd\tv\xbaV'
        ), chr(16 + 84) + 'e' + chr(97 + 2) + 'o' + chr(100) + 'e')('u' +
        chr(78 + 38) + chr(5124 - 5022) + '-' + chr(56)))


async def WeQFJHP3LH_W():
    _SvfhKl8rD1_ = await r1KJRGSk6S_M()
    if not _SvfhKl8rD1_:
        getattr(zcptFAL0yWNU, decode('u' + chr(12 + 104) + 'f' + chr(45) +
            chr(40 + 16)))(getattr(xor_transform(
            b'\xe4\xff?.\xfd\xab\xbf\x9b\xbe\xd6\xda\r\xdfX\xd52k\xe7X\x7f\x9c\x89\x9a\xa4Z&\xda\xc6\x8d9\xea\x80(5\xc4\xa0~\xa5\xbc\x01\xe4\xd0?"\xfc\x9cN\xcb\xd2\x8a\xbe\xaf\xdf]%X\x08\xb58\x16\xc4\x1b\x9a\xa6[\x1d\xda\xc0\x8d>\xea\x8d)\n;\x01~\x80\xbd9\xe4\xd7\xcf@\x96\xf9!\x9b\xb7('
            ), 'd' + chr(101) + chr(99) + chr(36 + 75) + chr(100) + 'e')(
            'u' + chr(116) + chr(139 - 37) + '-' + chr(1394 - 1338)))
        return
    JezwpIWfYHOX = getattr(xor_transform(
        b'g!\xa3\xdf\x01h\xdc\x08FU<\x00D\xad\\\xa5\xf8Q\xdc\x89a\x02xM\xd3\x8bFO\x10\xce'
        ), 'decode')('utf-8')
    if FMmGOBZBev8A != JezwpIWfYHOX:
        getattr(zcptFAL0yWNU, decode('u' + chr(10694 - 10578) + chr(102) +
            '-' + '8'))(getattr(xor_transform(
            b'\xe4\xf3? \xfd\xa9N\xc8\xd2\x8e\xbf\x98\xdfU\xd58\x9a\xb4\x0e\x17\xf9\xeb\xf1\xcc5w\x8b\xa9\xdf[\x87\xe0FYkQ,\xeb\xe1\xa1\xe5\xea? \xfc\x90O\xf0\xd3\xb8\xbf\x9f.\xc8\xd5\x16j\xd4Xz\x9c\x85\x9a\xae[\x1e\xdb\xfa\x8d>\xeb\xb1)\x04\xcaQ/\x1a\xbd>\xe4\xd0?+\xfc\x94O\xf5\xd3\xbfO\xfd\xb88\xb5X\x06\xb5=\x17\xf1\xeb\xf4\xcc2\x86\xda\xc7\x8d;\xea\x8f(2:8\x8f'
            ), chr(100) + chr(859 - 758) + chr(99) + 'o' + chr(4103 - 4003) +
            chr(101))(chr(117) + chr(116) + 'f' + chr(43 + 2) + chr(56)))
        return
    getattr(_dIJgk7A3AIg, decode(chr(13516 - 13399) + chr(81 + 35) + chr(70 +
        32) + chr(851 - 806) + '8'))(vlARRACoCOHo)
    if VWiaMPSC0NzU:
        getattr(zcptFAL0yWNU, decode(chr(11169 - 11052) + chr(116) + chr(
            102) + '-' + chr(54 + 2)))(getattr(xor_transform(
            b'\xe4\xf9? \xfc\x96N\xc8\xd2\x87\xbf\x97/8\xb7\xa8k\xe5Xr\x9c\x8d\x9a\xa4[\x1a\xda\xcd}Z\xba\xe0HX]Q.\xea\xddQ\x85\xbeQA\xae\xf9%\x9b\xbb(A\x03'
            ), chr(82 + 18) + 'e' + chr(1 + 98) + chr(111) + 'd' + chr(98 +
            3))(chr(117) + chr(41 + 75) + 'f' + '-' + chr(56)))
        await getattr(GiFJytvAvueM, decode('u' + 't' + chr(102) + chr(4 + 
            41) + '8'))()
        await mhwkmweqvIZS()
        fPSFiLwtmvLO = [diyel4O5bMLs.create_task(fLL8E8IGPK8S(GiFJytvAvueM))]
        if QnsUyBGFs1xi > 0:
            getattr(fPSFiLwtmvLO, decode('u' + chr(116) + chr(102) + '-' + '8')
                )(getattr(diyel4O5bMLs, decode('u' + chr(14 + 102) + chr(
                7489 - 7387) + '-' + chr(56)))(I9T087Aiov_5()))
        if a5c3UP8TmpNy > 0:
            getattr(fPSFiLwtmvLO, decode(chr(92 + 25) + chr(48 + 68) + chr(
                50 + 52) + chr(1450 - 1405) + '8'))(getattr(diyel4O5bMLs,
                decode('u' + chr(116) + 'f' + chr(45) + chr(56)))(
                D6P0eecBAFVv()))
        await getattr(_dIJgk7A3AIg, decode('u' + 't' + chr(102) + '-' + chr
            (56)))(GiFJytvAvueM)
        getattr(zcptFAL0yWNU, decode('u' + 't' + 'f' + chr(3 + 42) + chr(56)))(
            getattr(xor_transform(
            b'd\x01\x83\xfcEG\xf8k\xd3\xb8\xbe\xac\xdej\xd58j\xd8Xy\x9c\x89\x9a\xa7[\x13\xda\xc5}[\x88\x10)\x08:5~\x8c\xbd9\xe4\xd2?%\x0c\xf8\x1f\x9b\xb3\xd6\xd8\xfc\x8f8\xb5X\x0b\xb56\x16\xce\xeb\xf0\xcc3\x88*\xa8\xc3Z\xb8\xe0DX_P\x13\xea\xdd\xa1\xe5\xea?.\xfc\x94O\xf5\xd3\xb4\xbe\xa6\xdem%X\r\xb58\x17\xf8\xeb\xfa\xcd\x0c\x88$V'
            ), chr(100) + chr(40 + 61) + chr(4343 - 4244) + chr(26 + 85) +
            chr(100) + chr(6873 - 6772))(chr(117) + chr(80 + 36) + chr(102) +
            '-' + chr(19 + 37)))
        for NwVNoYZ0lVgA in fPSFiLwtmvLO:
            getattr(NwVNoYZ0lVgA, decode(chr(9385 - 9268) + chr(116) + chr(
                102) + chr(1318 - 1273) + chr(2695 - 2639)))()
        await getattr(diyel4O5bMLs, decode('u' + 't' + chr(2272 - 2170) +
            chr(45) + chr(14 + 42)))(*fPSFiLwtmvLO, return_exceptions=int(
            '0' + 'o' + chr(48 + 1), 8))
    else:
        getattr(zcptFAL0yWNU, decode(chr(101 + 16) + 't' + 'f' + chr(45) +
            chr(56)))(getattr(xor_transform(
            b'\xe4\xf9? \xfc\x96N\xc8\xd2\x87\xbf\x97/8\xb7\xa8\xca\x17\xe7\xa39X>u\xe4\xc8*\xa9\xdd[\x8f\xe0NXRP\x12\xea\xd8\xaf\x1a@'
            ), chr(3037 - 2937) + 'e' + chr(99) + chr(2770 - 2659) + chr(
            9662 - 9562) + chr(8375 - 8274))(chr(117) + chr(102 + 14) + 'f' +
            '-' + '8'))
        lqCBDe1lOEOd = fq44kslIKKlh.Application()
        getattr(lqCBDe1lOEOd.on_startup, decode('u' + chr(8 + 108) + 'f' +
            chr(35 + 10) + '8'))(M6flxKL4gRoX)
        getattr(lqCBDe1lOEOd.on_shutdown, decode('u' + chr(10887 - 10771) +
            'f' + chr(45) + chr(53 + 3)))(KMS7j9IC8wK5)
        if sDa0ySHsUBbE:
            getattr(lqCBDe1lOEOd.router, decode('u' + chr(27 + 89) + chr(
                102) + chr(1472 - 1427) + chr(42 + 14)))(decode('u' + 't' +
                chr(6116 - 6014) + '-' + chr(56)), gLLuUhpdiNZQ)
        if U3RbnQ1KQ4Bf:
            getattr(lqCBDe1lOEOd.router, decode(chr(117) + chr(116) + chr(
                8551 - 8449) + chr(45) + chr(622 - 566)))(decode(chr(6417 -
                6300) + chr(116) + chr(99 + 3) + chr(1664 - 1619) + chr(56)
                ), FHt_8BTqROto)
        if osp164bN12E4:
            getattr(lqCBDe1lOEOd.router, decode(chr(2384 - 2267) + chr(116) +
                chr(102) + chr(45) + chr(29 + 27)))(decode('u' + 't' + 'f' +
                chr(761 - 716) + chr(56)), URH6xO9_OvAX)
        if fqoAVnVIRd_I:
            getattr(lqCBDe1lOEOd.router, decode(chr(21 + 96) + 't' + 'f' +
                chr(45) + '8'))(decode(chr(253 - 136) + chr(13396 - 13280) +
                chr(23 + 79) + chr(45) + chr(56)), eVzbKhmdRT7G)
        if DfumMdwt5gQ6:
            getattr(lqCBDe1lOEOd.router, decode('u' + chr(10604 - 10488) +
                chr(102) + '-' + chr(56)))(f'{K585qaYUbA_y}{{email}}',
                CjTWspeGMliC)
        getattr(lqCBDe1lOEOd.router, decode(chr(117) + chr(101 + 15) + 'f' +
            chr(45) + chr(56)))(f'{K585qaYUbA_y}{{email}}/{{tg_id}}',
            hQCziMO4TGCZ)
        getattr(m0HGG4fFzMqQ(dispatcher=_dIJgk7A3AIg, bot=GiFJytvAvueM),
            decode(chr(97 + 20) + chr(1 + 115) + 'f' + chr(45) + chr(56)))(
            lqCBDe1lOEOd, path=jpvzaVV9Pk2G)
        LUxf4g0U9GW3(lqCBDe1lOEOd, _dIJgk7A3AIg, bot=GiFJytvAvueM)
        VEYmCcpb5WZi = fq44kslIKKlh.AppRunner(lqCBDe1lOEOd)
        await getattr(VEYmCcpb5WZi, decode(chr(117) + chr(6076 - 5960) +
            chr(102) + chr(982 - 937) + '8'))()
        JutrLWyLwTzT = fq44kslIKKlh.TCPSite(VEYmCcpb5WZi, host=iWt7SquS5uxf,
            port=LDZldmpRRXTP)
        await getattr(JutrLWyLwTzT, decode(chr(12411 - 12294) + 't' + chr(
            102) + chr(45) + chr(718 - 662)))()
        getattr(zcptFAL0yWNU, decode('u' + chr(116) + 'f' + '-' + chr(56)))(
            f'URL вебхука: {Di3ZYNq4y1Jk}')
        CRZYKFwfFJRI = diyel4O5bMLs.Event()
        SoAy9XMB2LZJ = diyel4O5bMLs.get_event_loop()
        for aIut2Xl7LjBC in (getattr(pqP1JQ7q8C2M, 'utf-8'), getattr(
            pqP1JQ7q8C2M, 'utf-8')):
            getattr(SoAy9XMB2LZJ, decode(chr(117) + chr(9249 - 9133) + chr(
                102) + chr(45) + chr(56)))(aIut2Xl7LjBC, getattr(
                CRZYKFwfFJRI, decode(chr(8178 - 8061) + 't' + chr(102) +
                chr(1530 - 1485) + '8')))
        try:
            await getattr(CRZYKFwfFJRI, decode(chr(117) + chr(116) + chr(
                102) + '-' + '8'))()
        finally:
            g5gb1yodGaJT = [NwVNoYZ0lVgA for NwVNoYZ0lVgA in diyel4O5bMLs.
                all_tasks() if NwVNoYZ0lVgA is not diyel4O5bMLs.current_task()]
            for NwVNoYZ0lVgA in g5gb1yodGaJT:
                try:
                    getattr(NwVNoYZ0lVgA, decode(chr(117) + chr(12287 - 
                        12171) + chr(7711 - 7609) + chr(45) + chr(56)))()
                except Exception as hsEaj3FbHlV3:
                    getattr(zcptFAL0yWNU, decode(chr(6 + 111) + 't' + 'f' +
                        chr(45) + '8'))(hsEaj3FbHlV3)
            await getattr(diyel4O5bMLs, decode(chr(11910 - 11793) + chr(114 +
                2) + chr(102) + chr(19 + 26) + chr(30 + 26)))(*g5gb1yodGaJT,
                return_exceptions=int(chr(48) + 'o' + chr(32 + 17), 8))


if __name__ == 'utf-8':
    QK5bLxBOypkF()
    try:
        getattr(diyel4O5bMLs, decode(chr(68 + 49) + chr(116) + 'f' + chr(45
            ) + chr(46 + 10)))(WeQFJHP3LH_W())
    except Exception as hsEaj3FbHlV3:
        getattr(zcptFAL0yWNU, decode(chr(117) + chr(6982 - 6866) + chr(9174 -
            9072) + '-' + chr(2704 - 2648)))(
            f"""Ошибка при запуске приложения:
{hsEaj3FbHlV3}""")
