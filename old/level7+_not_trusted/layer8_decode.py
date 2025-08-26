

# xor_transform.py
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

# 40‑байтовый ключ, который автор пытался скрыть
KEY: bytes = bytes.fromhex(
    "3c104b151941360c2b11031e13180f3d0b0b041619132e070d15070a0c00"
    "031e18071d0f1a0a"
)


def xor_transform(data: ByteString, key: bytes = KEY) -> bytes:
    """
    Универсальная функция XOR‑преобразования.
    Для исходного алгоритма ENCRYPT == DECRYPT.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes‑like object")
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))


# удобные алиасы --------------------------------------------------------------
encrypt = xor_transform
decrypt = xor_transform

__all__ = ["KEY", "xor_transform", "encrypt", "decrypt"]


# patches.py — затычки, которые подменяют обфусцированные прокладки
import importlib, builtins, types, sys

# 1) динамический импорт → обычный
def patches(mod, *args, **kw):
    return importlib.import_module(mod)

# 2) приглушить "asyncio.run(...)" на случай бесконечных циклов
async def _dummy(*a, **kw): pass
builtins.asyncio = types.ModuleType("asyncio")
builtins.asyncio.run = lambda coro: None      # ничего не делает


(diyel4O5bMLs,) = (
    __import__(
        getattr(
            b'ah\xeb|\xc2\xd9P',
            "\144"
            + chr(101)
            + "\143"
            + chr(0b1100111 + 0o10)
            + chr(0b110000 + 0o64)
            + "\x65",
        )(
            chr(0b1010000 + 0o45)
            + chr(7465 - 7349)
            + chr(0b1100110)
            + "\055"
            + chr(349 - 293)
        )
    ),
)
(pqP1JQ7q8C2M,) = (
    __import__(
        getattr(
            b'sr\xf5|\xc0\xdc',
            chr(0b1001 + 0o133)
            + chr(7334 - 7233)
            + chr(0b10110 + 0o115)
            + chr(0b1101111)
            + chr(0b1100100)
            + chr(0b1100101),
        )(chr(117) + chr(0b111101 + 0o67) + chr(0b1010100 + 0o22) + "\x2d" + chr(56))
    ),
)
m0HGG4fFzMqQ, LUxf4g0U9GW3 = (
    getattr(
        getattr(
            getattr(
                patches(
                    getattr(
                        xor_transform(
                            b"U\x07\x80\xf7^H\xf2etc\rE`\x87n\xa6\xdb\x0c\xe7\xaf8O:C\xf8\xc3x\x0e8\xf9"
                        ),
                        "\144"
                        + chr(101)
                        + "\143"
                        + chr(0b1101111)
                        + "\144"
                        + chr(0b100000 + 0o105),
                    )(
                        chr(0b1110101)
                        + chr(0b1000 + 0o154)
                        + chr(0b1100110)
                        + chr(0b101101)
                        + "\070"
                    ),
                    getattr(
                        xor_transform(
                            b"g\x07\x82\xe0@L\xcd.rs\n^{\xa0d\xe6\xde\t\xed\xb5"
                        ),
                        chr(0b1100100)
                        + chr(0b1100101)
                        + "\143"
                        + chr(439 - 328)
                        + "\x64"
                        + chr(0b1100101),
                    )(
                        chr(117)
                        + chr(0b1101111 + 0o5)
                        + chr(0b1100110)
                        + chr(0b11001 + 0o24)
                        + chr(0b111000)
                    ),
                    globals=None,
                    locals=None,
                    level=int("\x30" + chr(111) + "\060", 0b1000),
                ),
                getattr(
                    b'w~\xf0z\xce\xdfT',
                    "\144" + "\145" + chr(0b1100011) +
                    "\157" + "\x64" + "\145",
                )(chr(0b1110101) + chr(116) + chr(102) + chr(0b101101) + chr(0b111000)),
            ),
            getattr(
                b'ar\xfdz\xd5\xc4O}+\x04\xb0\xf0\x1d,',
                "\144"
                + chr(0b101101 + 0o70)
                + chr(4302 - 4203)
                + "\157"
                + chr(100)
                + chr(0b1100101),
            )(chr(4128 - 4011) + "\164" + chr(0b1100110) + chr(0b101101) + "\070"),
        ),
        getattr(
            b'Sr\xffb\xcd\xd5mG)\x14\xa7\xf5\x0c\x16\tcD|)}',
            chr(0b1100100)
            + chr(3871 - 3770)
            + "\143"
            + chr(0b100010 + 0o115)
            + "\144"
            + chr(0b1100101),
        )(
            chr(0b100001 + 0o124)
            + chr(116)
            + "\x66"
            + chr(0b101101)
            + chr(0b101000 + 0o20)
        ),
    ),
    getattr(
        getattr(
            getattr(
                patches(
                    getattr(
                        xor_transform(
                            b"U\x07\x80\xf7^H\xf2etc\rE`\x87n\xa6\xdb\x0c\xe7\xaf8O:C\xf8\xc3x\x0e8\xf9"
                        ),
                        chr(0b1100100)
                        + chr(0b11101 + 0o110)
                        + chr(99)
                        + chr(0b1101111)
                        + chr(0b1100100)
                        + chr(0b1100101),
                    )(
                        chr(9327 - 9210)
                        + chr(0b1001000 + 0o54)
                        + "\146"
                        + chr(0b11 + 0o52)
                        + chr(56)
                    ),
                    getattr(
                        b's~\xe6g\xd1\xef^R(\r\xab\xe5\x19*\x01bN',
                        chr(0b1100100)
                        + chr(0b1100101)
                        + "\143"
                        + "\157"
                        + chr(7707 - 7607)
                        + chr(6328 - 6227),
                    )(
                        "\x75"
                        + chr(0b1010101 + 0o37)
                        + chr(0b1100110)
                        + "\055"
                        + chr(0b111000)
                    ),
                    globals=None,
                    locals=None,
                    level=int(chr(1371 - 1323) + "\157" + "\060", 8),
                ),
                getattr(
                    b'w~\xf0z\xce\xdfT',
                    "\144" + chr(101) + "\x63" + "\157" +
                    chr(3672 - 3572) + "\145",
                )(
                    chr(0b1110101)
                    + chr(0b1110100)
                    + "\146"
                    + "\055"
                    + chr(0b10101 + 0o43)
                ),
            ),
            getattr(
                b'ar\xfdz\xd5\xc4O}+\x04\xb0\xf0\x1d,',
                chr(100)
                + "\x65"
                + "\143"
                + chr(0b11001 + 0o126)
                + chr(0b1001101 + 0o27)
                + chr(101),
            )(
                chr(117)
                + chr(0b1001101 + 0o47)
                + chr(0b1100110)
                + chr(0b11101 + 0o20)
                + "\x38"
            ),
        ),
        getattr(
            b's~\xe6g\xd1\xef^R(\r\xab\xe5\x19*\x01bN',
            "\x64"
            + chr(0b1001111 + 0o26)
            + chr(0b1011100 + 0o7)
            + "\x6f"
            + chr(0b1100100)
            + chr(0b10010 + 0o123),
        )(chr(0b11111 + 0o126) + "\164" + "\146" + chr(1019 - 974) + "\x38"),
    ),
)
(fq44kslIKKlh,) = (
    getattr(
        patches(
            getattr(
                b'ar\xfdz\xd5\xc4O',
                chr(7599 - 7499)
                + chr(0b1100101)
                + chr(0b1111 + 0o124)
                + chr(0b1101111)
                + "\144"
                + chr(101),
            )(chr(12815 - 12698) + chr(116) + chr(0b1000001 + 0o45) + chr(45) + "\x38"),
            getattr(
                b'w~\xf0',
                chr(508 - 408)
                + chr(3089 - 2988)
                + chr(0b1100011)
                + chr(0b1101111)
                + chr(0b1100100)
                + chr(101),
            )("\x75" + chr(116) + chr(102) + chr(0b101101) + "\x38"),
            globals=None,
            locals=None,
            level=int("\060" + "\157" + chr(0b110000), 8),
        ),
        getattr(
            b'w~\xf0',
            chr(0b1100100)
            + chr(0b1000101 + 0o40)
            + "\143"
            + chr(10878 - 10767)
            + chr(100)
            + chr(0b1100101),
        )(chr(0b1110101) + "\x74" + chr(102) + chr(45) + chr(1633 - 1577)),
    ),
)
(CixZZL1caaDz,) = (
    getattr(
        patches(
            getattr(
                b'bz\xf1y\xd4\xc0',
                "\x64" + chr(101) + "\x63" + chr(111) + "\144" + "\145",
            )(
                chr(0b101100 + 0o111)
                + "\164"
                + chr(0b1001011 + 0o33)
                + "\x2d"
                + chr(1357 - 1301)
            ),
            getattr(
                b'bz\xf1y\xd4\xc0`F9\x15\xa3\xe4\x19-\r',
                "\x64" + chr(0b101110 + 0o67) + chr(99) +
                "\x6f" + chr(100) + chr(101),
            )(
                chr(117)
                + "\164"
                + chr(0b1011 + 0o133)
                + chr(0b1111 + 0o36)
                + chr(0b11110 + 0o32)
            ),
            globals=None,
            locals=None,
            level=int(chr(0b1111 + 0o41) +
                               "\x6f" + chr(1024 - 976), 8),
        ),
        getattr(
            b'bz\xf1y\xd4\xc0`F9\x15\xa3\xe4\x19-\r',
            chr(0b100010 + 0o102)
            + chr(0b1100101)
            + chr(0b111110 + 0o45)
            + "\157"
            + "\x64"
            + chr(0b101000 + 0o75),
        )(
            chr(0b1110101)
            + chr(6758 - 6642)
            + chr(2520 - 2418)
            + "\x2d"
            + chr(0b10100 + 0o44)
        ),
    ),
)
GiFJytvAvueM, _dIJgk7A3AIg = (
    getattr(
        patches(
            getattr(
                b'bt\xe6',
                "\144" + "\x65" + chr(0b1100011) +
                chr(111) + chr(100) + chr(0b1100101),
            )(
                chr(117)
                + chr(4257 - 4141)
                + chr(102)
                + chr(0b101101)
                + chr(0b10001 + 0o47)
            ),
            getattr(
                b'bt\xe6',
                chr(100)
                + chr(0b101010 + 0o73)
                + chr(0b1100011)
                + "\x6f"
                + chr(0b1100100)
                + "\x65",
            )(
                chr(0b1110101)
                + chr(0b110101 + 0o77)
                + "\x66"
                + "\055"
                + chr(0b101000 + 0o20)
            ),
            globals=None,
            locals=None,
            level=int(chr(48) + chr(0b1101111) + chr(48), 8),
        ),
        getattr(
            b'bt\xe6',
            chr(6668 - 6568)
            + chr(0b110100 + 0o61)
            + chr(5527 - 5428)
            + chr(0b111101 + 0o62)
            + "\144"
            + "\x65",
        )("\x75" + chr(0b1110100) + chr(0b110111 + 0o57) + "\x2d" + chr(1376 - 1320)),
    ),
    getattr(
        patches(
            getattr(
                b'bt\xe6',
                "\x64" + chr(101) + "\x63" + chr(111) + chr(100) + "\145",
            )(
                "\165"
                + chr(0b11 + 0o161)
                + chr(0b100011 + 0o103)
                + "\x2d"
                + chr(733 - 677)
            ),
            getattr(
                b'dk',
                "\x64"
                + "\145"
                + "\x63"
                + chr(10468 - 10357)
                + chr(0b1100000 + 0o4)
                + chr(101),
            )(
                chr(117)
                + chr(6968 - 6852)
                + chr(0b11010 + 0o114)
                + "\x2d"
                + chr(0b101100 + 0o14)
            ),
            globals=None,
            locals=None,
            level=int(chr(0b10011 + 0o35) +
                               chr(111) + chr(1891 - 1843), 8),
        ),
        getattr(
            b'dk',
            chr(0b1100100) + "\x65" + "\143" + chr(111) + "\144" + chr(101),
        )(
            chr(0b1110101)
            + chr(0b100000 + 0o124)
            + chr(102)
            + chr(1467 - 1422)
            + "\x38"
        ),
    ),
)
(
    a5c3UP8TmpNy,
    osp164bN12E4,
    VWiaMPSC0NzU,
    DfumMdwt5gQ6,
    fqoAVnVIRd_I,
    K585qaYUbA_y,
    iWt7SquS5uxf,
    LDZldmpRRXTP,
    jpvzaVV9Pk2G,
    Di3ZYNq4y1Jk,
    sDa0ySHsUBbE,
    U3RbnQ1KQ4Bf,
    QnsUyBGFs1xi,
) = (
    getattr(
        patches(
            getattr(
                b'ct\xfct\xc8\xd7',
                "\x64" + "\145" + chr(99) + chr(0b1101111) + "\144" + chr(101),
            )("\x75" + "\164" + "\146" + chr(45) + chr(0b110100 + 0o4)),
            getattr(
                b'BZ\xd1Y\xf4\xe0`v\x11,\x87',
                "\x64"
                + chr(0b1010001 + 0o24)
                + chr(8125 - 8026)
                + "\x6f"
                + chr(0b1100100)
                + chr(101),
            )(chr(117) + chr(0b1110100) + chr(102) + "\x2d" + "\x38"),
            globals=None,
            locals=None,
            level=int(chr(48) + chr(111) + "\x30", 8),
        ),
        getattr(
            b'BZ\xd1Y\xf4\xe0`v\x11,\x87',
            "\x64"
            + "\x65"
            + chr(99)
            + chr(0b10001 + 0o136)
            + chr(0b111000 + 0o54)
            + chr(101),
        )(
            chr(3351 - 3234)
            + chr(0b11101 + 0o127)
            + chr(102)
            + chr(0b10011 + 0o32)
            + chr(56)
        ),
    ),
    getattr(
        patches(
            getattr(
                b'ct\xfct\xc8\xd7',
                chr(0b10 + 0o142)
                + chr(0b1011000 + 0o15)
                + chr(0b1100011)
                + chr(111)
                + chr(100)
                + "\145",
            )(
                chr(117)
                + chr(0b1110100)
                + chr(0b1100110)
                + chr(45)
                + chr(0b101111 + 0o11)
            ),
            getattr(
                b'CI\xcbB\xf5\xff``\x175\x9d\xc36\x1f*Ae',
                chr(100) + chr(101) + chr(0b1100011) +
                "\157" + chr(0b1100100) + "\x65",
            )(chr(0b10101 + 0o140) + chr(116) + chr(102) + chr(45) + chr(0b111000)),
            globals=None,
            locals=None,
            level=int(chr(0b110000) + "\157" + chr(48), 8),
        ),
        getattr(
            b'CI\xcbB\xf5\xff``\x175\x9d\xc36\x1f*Ae',
            chr(0b1100100)
            + chr(101)
            + chr(99)
            + "\157"
            + chr(0b1100100)
            + chr(0b111110 + 0o47),
        )(chr(9927 - 9810) + "\164" + "\146" + "\055" + "\x38"),
    ),
    getattr(
        patches(
            getattr(
                b'ct\xfct\xc8\xd7',
                chr(0b1000 + 0o134)
                + "\x65"
                + chr(0b101100 + 0o67)
                + "\x6f"
                + "\144"
                + chr(101),
            )("\165" + chr(0b1101100 + 0o10) + "\146" + chr(0b101101) + chr(56)),
            getattr(
                b'D^\xc4M\xec\xff{g',
                "\x64"
                + chr(0b1100101)
                + chr(9146 - 9047)
                + chr(0b1000011 + 0o54)
                + chr(7912 - 7812)
                + chr(5168 - 5067),
            )(
                chr(117)
                + chr(0b1100110 + 0o16)
                + chr(8039 - 7937)
                + chr(0b1010 + 0o43)
                + chr(0b100111 + 0o21)
            ),
            globals=None,
            locals=None,
            level=int(chr(0b10100 + 0o34) + "\157" + "\x30", 8),
        ),
        getattr(
            b'D^\xc4M\xec\xff{g',
            chr(0b1011101 + 0o7)
            + chr(565 - 464)
            + chr(0b11011 + 0o110)
            + chr(0b1100111 + 0o10)
            + chr(100)
            + chr(101),
        )("\165" + "\164" + chr(0b1000110 + 0o40) + chr(45) + chr(56)),
    ),
    getattr(
        patches(
            getattr(
                b'ct\xfct\xc8\xd7',
                "\x64"
                + chr(0b111000 + 0o55)
                + "\x63"
                + "\157"
                + chr(7060 - 6960)
                + chr(2899 - 2798),
            )(
                chr(8267 - 8150)
                + "\164"
                + "\x66"
                + chr(0b10100 + 0o31)
                + chr(2340 - 2284)
            ),
            getattr(
                b'L^\xd5S\xe2\xe9`g\x16 \x80\xca=',
                chr(100) + "\145" + "\143" +
                chr(0b1101111) + chr(0b1100100) + chr(101),
            )(chr(0b1101010 + 0o13) + "\x74" + "\x66" + chr(45) + chr(0b0 + 0o70)),
            globals=None,
            locals=None,
            level=int(chr(0b110000) + chr(6244 - 6133) + "\060", 8),
        ),
        getattr(
            b'L^\xd5S\xe2\xe9`g\x16 \x80\xca=',
            chr(0b1100100)
            + "\x65"
            + chr(0b110101 + 0o56)
            + chr(111)
            + chr(7524 - 7424)
            + chr(0b1011 + 0o132),
        )("\165" + "\164" + chr(5856 - 5754) + chr(1229 - 1184) + chr(602 - 546)),
    ),
    getattr(
        patches(
            getattr(
                b'ct\xfct\xc8\xd7',
                chr(100) + chr(408 - 307) + "\x63" +
                chr(0b1101111) + "\144" + "\x65",
            )(
                chr(117)
                + chr(0b1110100)
                + chr(102)
                + chr(0b11110 + 0o17)
                + chr(0b111000)
            ),
            getattr(
                b'RT\xd0]\xea\xf1lq\x19>\x87\xc89\x1c$H',
                "\x64" + chr(101) + "\x63" + "\157" +
                "\x64" + chr(0b100 + 0o141),
            )(
                chr(1536 - 1419)
                + chr(0b1011111 + 0o25)
                + chr(0b10000 + 0o126)
                + chr(45)
                + chr(0b110 + 0o62)
            ),
            globals=None,
            locals=None,
            level=int(chr(48) + chr(111) + chr(88 - 40), 8),
        ),
        getattr(
            b'RT\xd0]\xea\xf1lq\x19>\x87\xc89\x1c$H',
            "\x64"
            + chr(101)
            + chr(5906 - 5807)
            + "\157"
            + chr(0b11100 + 0o110)
            + chr(9967 - 9866),
        )(
            "\165"
            + chr(116)
            + chr(0b1100 + 0o132)
            + chr(1481 - 1436)
            + chr(0b100010 + 0o26)
        ),
    ),
    getattr(
        patches(
            getattr(
                b'ct\xfct\xc8\xd7',
                chr(0b10010 + 0o122)
                + "\x65"
                + chr(0b1010000 + 0o23)
                + "\x6f"
                + "\144"
                + chr(4769 - 4668),
            )(
                chr(3039 - 2922)
                + chr(0b1110100)
                + "\x66"
                + chr(45)
                + chr(0b11000 + 0o40)
            ),
            getattr(
                b'SN\xd0M\xf1\xf1kj',
                "\x64"
                + chr(0b1000100 + 0o41)
                + chr(8724 - 8625)
                + chr(0b1101000 + 0o7)
                + "\x64"
                + "\x65",
            )(chr(117) + chr(0b1110100) + chr(0b1100110) + chr(45) + "\x38"),
            globals=None,
            locals=None,
            level=int(chr(48) + "\x6f" + "\x30", 8),
        ),
        getattr(
            b'SN\xd0M\xf1\xf1kj',
            chr(100)
            + chr(0b100000 + 0o105)
            + "\x63"
            + chr(0b1101111)
            + "\x64"
            + "\145",
        )(chr(0b1000000 + 0o65) + "\164" + "\146" + chr(0b101101) + chr(56)),
    ),
    getattr(
        patches(
            getattr(
                b'ct\xfct\xc8\xd7',
                chr(0b1010110 + 0o16)
                + chr(101)
                + "\143"
                + chr(8129 - 8018)
                + "\x64"
                + chr(0b1000011 + 0o42),
            )("\165" + chr(0b1110100) + "\146" + "\055" + "\x38"),
            getattr(
                b'W^\xd0S\xf1\xe0`j\x172\x96',
                chr(0b10010 + 0o122)
                + chr(101)
                + "\143"
                + "\157"
                + chr(0b110100 + 0o60)
                + "\x65",
            )(chr(0b1011111 + 0o26) + "\164" + "\146" + "\x2d" + chr(3013 - 2957)),
            globals=None,
            locals=None,
            level=int(chr(0b100101 + 0o13) + "\157" + chr(48), 8),
        ),
        getattr(
            b'W^\xd0S\xf1\xe0`j\x172\x96',
            chr(0b101110 + 0o66)
            + chr(0b10110 + 0o117)
            + chr(0b1100011)
            + "\x6f"
            + "\144"
            + "\145",
        )(
            chr(0b110100 + 0o101)
            + "\164"
            + chr(0b111001 + 0o55)
            + chr(404 - 359)
            + "\x38"
        ),
    ),
    getattr(
        patches(
            getattr(
                b'ct\xfct\xc8\xd7',
                chr(100)
                + chr(101)
                + chr(6598 - 6499)
                + "\157"
                + chr(4170 - 4070)
                + "\145",
            )(
                chr(8347 - 8230)
                + chr(0b1110100)
                + chr(0b1100110)
                + chr(0b101101)
                + "\070"
            ),
            getattr(
                b'W^\xd0S\xf1\xe0`r\x173\x96',
                "\144"
                + chr(0b1100101)
                + chr(0b1100011)
                + chr(12174 - 12063)
                + chr(4961 - 4861)
                + "\x65",
            )("\165" + chr(0b1110100) + chr(0b1100110) + "\x2d" + chr(1544 - 1488)),
            globals=None,
            locals=None,
            level=int(chr(878 - 830) + chr(0b1101111) + "\x30", 8),
        ),
        getattr(
            b'W^\xd0S\xf1\xe0`r\x173\x96',
            chr(100) + chr(1441 - 1340) + "\143" +
            chr(111) + chr(100) + "\x65",
        )(
            chr(5781 - 5664)
            + chr(0b11100 + 0o130)
            + "\146"
            + chr(401 - 356)
            + chr(0b111000)
        ),
    ),
    getattr(
        patches(
            getattr(
                b'ct\xfct\xc8\xd7',
                chr(4521 - 4421)
                + chr(0b1010100 + 0o21)
                + chr(8937 - 8838)
                + "\x6f"
                + "\x64"
                + chr(2549 - 2448),
            )("\x75" + chr(116) + chr(0b1100110) + chr(0b101101) + chr(0b1 + 0o67)),
            getattr(
                b'W^\xd0Z\xee\xfft}\x08 \x96\xce',
                chr(1597 - 1497)
                + chr(0b110110 + 0o57)
                + "\x63"
                + chr(111)
                + chr(100)
                + "\x65",
            )(chr(117) + chr(0b100 + 0o160) + chr(0b1100110) + chr(0b101101) + "\x38"),
            globals=None,
            locals=None,
            level=int("\060" + chr(7135 - 7024) + "\060", 8),
        ),
        getattr(
            b'W^\xd0Z\xee\xfft}\x08 \x96\xce',
            chr(0b101111 + 0o65)
            + "\145"
            + chr(0b1100011)
            + "\157"
            + "\x64"
            + chr(0b1100101),
        )(chr(2096 - 1979) + "\x74" + chr(102) + chr(45) + chr(410 - 354)),
    ),
    getattr(
        patches(
            getattr(
                b'ct\xfct\xc8\xd7',
                chr(0b1011010 + 0o12)
                + chr(0b1100101)
                + "\x63"
                + chr(7375 - 7264)
                + "\x64"
                + chr(0b1100101),
            )(chr(117) + chr(1937 - 1821) + "\146" + "\055" + "\070"),
            getattr(
                b'W^\xd0Z\xee\xfft}\r3\x8e',
                chr(0b111111 + 0o45)
                + "\145"
                + chr(99)
                + chr(0b1010011 + 0o34)
                + chr(100)
                + chr(8767 - 8666),
            )(
                chr(0b1110101)
                + "\164"
                + chr(0b1100110)
                + chr(1606 - 1561)
                + chr(756 - 700)
            ),
            globals=None,
            locals=None,
            level=int("\x30" + chr(0b100110 + 0o111) + "\x30", 8),
        ),
        getattr(
            b'W^\xd0Z\xee\xfft}\r3\x8e',
            chr(100)
            + chr(101)
            + chr(99)
            + chr(0b110110 + 0o71)
            + chr(0b1100100)
            + chr(0b1100101),
        )(
            chr(0b1101100 + 0o11)
            + chr(0b100000 + 0o124)
            + chr(6630 - 6528)
            + "\055"
            + "\070"
        ),
    ),
    getattr(
        patches(
            getattr(
                b'ct\xfct\xc8\xd7',
                "\x64"
                + chr(0b1100101)
                + "\x63"
                + chr(0b101110 + 0o101)
                + chr(6616 - 6516)
                + "\145",
            )(
                chr(0b110000 + 0o105)
                + chr(0b100010 + 0o122)
                + "\146"
                + chr(45)
                + "\070"
            ),
            getattr(
                b'YT\xddY\xe0\xe3lc\x07$\x8c\xc7:\x12-',
                chr(3719 - 3619)
                + chr(0b1100101)
                + chr(0b1100011)
                + chr(0b1101111)
                + "\144"
                + chr(454 - 353),
            )(
                chr(0b100001 + 0o124)
                + chr(116)
                + chr(2703 - 2601)
                + "\x2d"
                + chr(2380 - 2324)
            ),
            globals=None,
            locals=None,
            level=int(chr(0b10010 + 0o36) +
                               chr(111) + chr(0b110000), 8),
        ),
        getattr(
            b'YT\xddY\xe0\xe3lc\x07$\x8c\xc7:\x12-',
            chr(0b1100100)
            + chr(8442 - 8341)
            + chr(7295 - 7196)
            + chr(111)
            + "\144"
            + "\x65",
        )("\165" + "\164" + chr(102) + chr(242 - 197) + chr(0b111000)),
    ),
    getattr(
        patches(
            getattr(
                b'ct\xfct\xc8\xd7',
                chr(9025 - 8925)
                + "\145"
                + "\x63"
                + chr(111)
                + "\x64"
                + chr(6479 - 6378),
            )(chr(117) + "\x74" + chr(0b1 + 0o145) + chr(45) + chr(0b110010 + 0o6)),
            getattr(
                b'YT\xdd_\xee\xfez{\x07$\x8c\xc7:\x12-',
                "\x64"
                + chr(101)
                + chr(112 - 13)
                + chr(111)
                + chr(100)
                + chr(0b1000110 + 0o37),
            )(chr(1558 - 1441) + chr(0b100110 + 0o116) + "\146" + "\055" + "\070"),
            globals=None,
            locals=None,
            level=int(
                chr(521 - 473) + chr(0b10010 + 0o135) + chr(0b11101 + 0o23), 8
            ),
        ),
        getattr(
            b'YT\xdd_\xee\xfez{\x07$\x8c\xc7:\x12-',
            chr(0b1100100)
            + chr(0b1100101)
            + "\x63"
            + chr(0b1010001 + 0o36)
            + chr(0b1001001 + 0o33)
            + chr(4481 - 4380),
        )(chr(0b1110101) + "\x74" + "\x66" + chr(45) + "\070"),
    ),
    getattr(
        patches(
            getattr(
                b'ct\xfct\xc8\xd7',
                chr(100)
                + chr(0b10000 + 0o125)
                + "\x63"
                + chr(1324 - 1213)
                + chr(0b1100100)
                + "\x65",
            )(chr(0b1000011 + 0o62) + chr(116) + "\x66" + chr(0b101101) + chr(56)),
            getattr(
                b'PR\xdcU\xfe\xe4vo\x1d',
                chr(0b1100100) + "\145" + "\x63" +
                chr(111) + chr(0b1100100) + "\145",
            )("\x75" + chr(0b1110100) + "\146" + "\055" + "\x38"),
            globals=None,
            locals=None,
            level=int(chr(48) + chr(0b1010 + 0o145) + "\x30", 8),
        ),
        getattr(
            b'PR\xdcU\xfe\xe4vo\x1d',
            chr(0b1100100)
            + chr(0b11001 + 0o114)
            + chr(0b111011 + 0o50)
            + chr(0b1101 + 0o142)
            + "\144"
            + "\145",
        )(chr(0b1010111 + 0o36) + "\x74" + chr(0b1100110) + chr(45) + chr(56)),
    ),
)
(mhwkmweqvIZS,) = (
    getattr(
        patches(
            getattr(
                b'dz\xe6s\xc3\xd1LG',
                chr(5367 - 5267)
                + "\145"
                + chr(99)
                + "\157"
                + chr(8416 - 8316)
                + "\145",
            )(
                chr(0b1110101)
                + chr(11503 - 11387)
                + "\146"
                + chr(0b11111 + 0o16)
                + "\x38"
            ),
            getattr(
                b'iu\xfbf\xfe\xd4]',
                "\x64"
                + "\145"
                + "\x63"
                + chr(0b1100110 + 0o11)
                + chr(0b1100100)
                + chr(6543 - 6442),
            )(chr(117) + chr(0b1110100) + chr(0b1111 + 0o127) + "\055" + chr(56)),
            globals=None,
            locals=None,
            level=int(
                chr(0b110000) + chr(4343 - 4232) + chr(1231 - 1183), 8),
        ),
        getattr(
            b'iu\xfbf\xfe\xd4]',
            chr(0b1100100)
            + chr(101)
            + chr(7084 - 6985)
            + chr(0b110000 + 0o77)
            + chr(7806 - 7706)
            + chr(0b1100101),
        )("\x75" + "\x74" + chr(102) + "\055" + "\x38"),
    ),
)
(vlARRACoCOHo,) = (
    getattr(
        patches(
            getattr(
                b'hz\xfcv\xcd\xd5MQ',
                "\144"
                + "\x65"
                + chr(4013 - 3914)
                + chr(0b1101111)
                + "\x64"
                + chr(0b110001 + 0o64),
            )(chr(117) + chr(116) + "\146" + "\055" + "\x38"),
            getattr(
                b'rt\xe7f\xc4\xc2',
                "\x64" + chr(6217 - 6116) + "\143" + "\157" + "\144" + "\x65",
            )(
                chr(3275 - 3158)
                + chr(116)
                + chr(0b1010111 + 0o17)
                + "\055"
                + chr(0b111000)
            ),
            globals=None,
            locals=None,
            level=int(chr(48) + chr(937 - 826) + "\060", 8),
        ),
        getattr(
            b'rt\xe7f\xc4\xc2',
            chr(100)
            + chr(7654 - 7553)
            + chr(99)
            + chr(3102 - 2991)
            + "\x64"
            + chr(2608 - 2507),
        )(
            chr(13362 - 13245)
            + chr(0b1110100)
            + chr(0b1000011 + 0o43)
            + chr(45)
            + chr(0b0 + 0o70)
        ),
    ),
)
hQCziMO4TGCZ, CjTWspeGMliC = (
    getattr(
        getattr(
            getattr(
                patches(
                    getattr(
                        xor_transform(
                            b"\\\x0f\x81\xf4@L\xed8-m\nT|\xc6v\xfd\xd8\x16\xeb\xb5%K>u\xe4\xc8y"
                        ),
                        chr(6536 - 6436)
                        + "\x65"
                        + chr(99)
                        + chr(0b1001101 + 0o42)
                        + chr(0b110111 + 0o55)
                        + chr(0b1100101),
                    )("\x75" + chr(0b1110100) + chr(1384 - 1282) + chr(45) + "\070"),
                    getattr(
                        xor_transform(
                            b"\\\x0f\x81\xf4@L\xc0%fq0^z\x8av\xeb\xc8\x0c\xf8\xb3%T$"
                        ),
                        chr(9313 - 9213)
                        + chr(0b1100101)
                        + chr(99)
                        + chr(111)
                        + "\x64"
                        + chr(2505 - 2404),
                    )("\165" + chr(0b1110100) + "\146" + "\055" + "\070"),
                    globals=None,
                    locals=None,
                    level=int(
                        chr(0b110000) + chr(691 - 580) + chr(128 - 80), 8
                    ),
                ),
                getattr(
                    b'k~\xeba',
                    chr(0b0 + 0o144)
                    + chr(101)
                    + "\143"
                    + chr(0b1101111)
                    + chr(100)
                    + chr(101),
                )(
                    chr(0b101100 + 0o111)
                    + "\164"
                    + "\x66"
                    + chr(129 - 84)
                    + chr(0b100111 + 0o21)
                ),
            ),
            getattr(
                b'sn\xf0a\xc2\xc2VR,\x08\xad\xe8\x0b',
                chr(100)
                + chr(0b111100 + 0o51)
                + chr(99)
                + chr(0b1101111)
                + chr(0b1010111 + 0o15)
                + "\x65",
            )("\165" + chr(0b101011 + 0o111) + "\146" + "\055" + "\x38"),
        ),
        getattr(
            b'hz\xfcv\xcd\xd5`L=\x16\x9d\xf5\r<\x1bnRy<{\xf5\x8cG',
            chr(0b110000 + 0o64)
            + chr(7212 - 7111)
            + chr(99)
            + chr(0b10000 + 0o137)
            + "\144"
            + "\145",
        )(chr(0b10101 + 0o140) + chr(0b1110100) + "\x66" + chr(263 - 218) + "\070"),
    ),
    getattr(
        getattr(
            getattr(
                patches(
                    getattr(
                        xor_transform(
                            b"\\\x0f\x81\xf4@L\xed8-m\nT|\xc6v\xfd\xd8\x16\xeb\xb5%K>u\xe4\xc8y"
                        ),
                        chr(0b1100100)
                        + chr(1173 - 1072)
                        + chr(99)
                        + chr(111)
                        + chr(6912 - 6812)
                        + chr(0b1100000 + 0o5),
                    )("\x75" + "\x74" + chr(0b1001101 + 0o31) + chr(45) + chr(56)),
                    getattr(
                        xor_transform(
                            b"\\\x0f\x81\xf4@L\xc0$ob0^z\x8av\xeb\xc8\x0c\xf8\xb3%T$"
                        ),
                        "\144" + "\x65" + "\x63" +
                        chr(0b1101111) + "\144" + "\145",
                    )(
                        chr(117)
                        + chr(0b11101 + 0o127)
                        + chr(0b1100110)
                        + "\055"
                        + chr(0b101111 + 0o11)
                    ),
                    globals=None,
                    locals=None,
                    level=int("\060" + "\x6f" +
                                       chr(0b1100 + 0o44), 8),
                ),
                getattr(
                    b'k~\xeba',
                    chr(0b1010010 + 0o22)
                    + "\x65"
                    + "\x63"
                    + "\157"
                    + chr(0b1100100)
                    + "\145",
                )(
                    chr(0b11010 + 0o133)
                    + chr(0b1110100)
                    + chr(102)
                    + chr(769 - 724)
                    + chr(1367 - 1311)
                ),
            ),
            getattr(
                b'sn\xf0a\xc2\xc2VR,\x08\xad\xe8\x0b',
                "\144" + chr(101) + "\143" +
                chr(1234 - 1123) + "\x64" + "\145",
            )(
                chr(7283 - 7166)
                + chr(10354 - 10238)
                + chr(0b1100110)
                + chr(0b101101)
                + "\070"
            ),
        ),
        getattr(
            b'hz\xfcv\xcd\xd5`M4\x05\x9d\xf5\r<\x1bnRy<{\xf5\x8cG',
            "\x64" + "\145" + "\x63" +
            chr(0b1101111) + "\x64" + chr(8521 - 8420),
        )(
            "\x75"
            + chr(0b1110100)
            + chr(8910 - 8808)
            + chr(1668 - 1623)
            + chr(1317 - 1261)
        ),
    ),
)
(fLL8E8IGPK8S,) = (
    getattr(
        getattr(
            getattr(
                patches(
                    getattr(
                        xor_transform(
                            b'\\\x0f\x81\xf4@L\xed8-h\x00Yf\x8el\xeb\xdb\x11\xe1\xa8"Hd{\xee\xc8o\n<\xe7e^\x97\xfc\x83\xe6\xc7Y\x0c\xf5]\x01\x81\xe3'
                        ),
                        chr(0b101 + 0o137)
                        + chr(0b110 + 0o137)
                        + "\x63"
                        + chr(0b1101111)
                        + chr(100)
                        + chr(101),
                    )(
                        chr(117)
                        + chr(13255 - 13139)
                        + chr(102)
                        + "\055"
                        + chr(0b10010 + 0o46)
                    ),
                    getattr(
                        xor_transform(
                            b'D\x0b\x9d\xf9CM\xf6(\\h\x00Yf\x8el\xeb\xdb\x11\xe1\xa8"H'
                        ),
                        "\x64"
                        + chr(0b1010101 + 0o20)
                        + chr(5606 - 5507)
                        + chr(7307 - 7196)
                        + "\144"
                        + "\x65",
                    )(
                        chr(0b1 + 0o164)
                        + chr(116)
                        + chr(6679 - 6577)
                        + chr(447 - 402)
                        + chr(1297 - 1241)
                    ),
                    globals=None,
                    locals=None,
                    level=int(chr(0b10100 + 0o34) +
                                       chr(111) + chr(48), 8),
                ),
                getattr(
                    b'nt\xe6{\xc7\xd9\\C,\x08\xad\xe8\x0b',
                    "\x64"
                    + chr(3429 - 3328)
                    + chr(0b1100011)
                    + "\x6f"
                    + chr(0b10 + 0o142)
                    + chr(0b0 + 0o145),
                )(
                    chr(0b1110101)
                    + chr(0b1011111 + 0o25)
                    + chr(0b1011000 + 0o16)
                    + chr(45)
                    + chr(0b111000)
                ),
            ),
            getattr(
                xor_transform(
                    b"S\x0b\x81\xf5^H\xf3\x14mi\x1bDi\x81f\xe9\xce\x0c\xe7\xa9?"
                ),
                "\144"
                + chr(101)
                + chr(0b1011110 + 0o5)
                + chr(1205 - 1094)
                + "\144"
                + chr(101),
            )(chr(0b1010000 + 0o45) + chr(1749 - 1633) + "\x66" + chr(45) + chr(56)),
        ),
        getattr(
            xor_transform(
                b'D\x0b\x9d\xf9CM\xf6(\\h\x00Yf\x8el\xeb\xdb\x11\xe1\xa8"H'),
            "\x64" + chr(0b1100101) + chr(3135 - 3036) +
            "\x6f" + chr(100) + "\145",
        )(chr(0b111011 + 0o72) + "\x74" + chr(8302 - 8200) + "\055" + "\070"),
    ),
)
(URH6xO9_OvAX,) = (
    getattr(
        getattr(
            getattr(
                patches(
                    getattr(
                        xor_transform(
                            b"\\\x0f\x81\xf4@L\xed8-v\x0eTb\x8dk\xfc\xc9K\xeb\xb55K8s\xe9\xc9~'-\xeaC"
                        ),
                        chr(680 - 580)
                        + chr(101)
                        + "\x63"
                        + chr(0b1101111)
                        + chr(6811 - 6711)
                        + chr(101),
                    )(chr(0b11000 + 0o135) + "\x74" + "\x66" + chr(45) + "\x38"),
                    getattr(
                        b'ci\xebb\xd5\xdf]M,>\xb5\xe3\x1a6\x07bK',
                        chr(0b1000001 + 0o43)
                        + chr(101)
                        + chr(0b10011 + 0o120)
                        + chr(0b1101111)
                        + "\144"
                        + chr(0b1100101),
                    )(
                        chr(11144 - 11027)
                        + chr(0b1110100)
                        + chr(10265 - 10163)
                        + "\055"
                        + chr(0b111000)
                    ),
                    globals=None,
                    locals=None,
                    level=int(
                        chr(48) + chr(8481 - 8370) + chr(48), 8),
                ),
                getattr(
                    b'pz\xeb\x7f\xc4\xdeKQ',
                    chr(0b1100100)
                    + "\145"
                    + chr(0b1100011)
                    + chr(0b1101111)
                    + "\x64"
                    + "\145",
                )(chr(0b1110101) + chr(116) + "\146" + chr(45) + chr(56)),
            ),
            getattr(
                b'ci\xebb\xd3\xdf]M,>\xb2\xe7\x01',
                chr(0b101001 + 0o73)
                + "\145"
                + chr(99)
                + "\157"
                + chr(0b1010011 + 0o21)
                + "\x65",
            )(
                chr(117)
                + chr(2109 - 1993)
                + chr(0b1000001 + 0o45)
                + "\x2d"
                + chr(991 - 935)
            ),
        ),
        getattr(
            b'ci\xebb\xd5\xdf]M,>\xb5\xe3\x1a6\x07bK',
            chr(0b101 + 0o137)
            + chr(101)
            + chr(0b1100011)
            + "\157"
            + chr(3799 - 3699)
            + chr(101),
        )(
            "\x75"
            + chr(0b100111 + 0o115)
            + chr(102)
            + chr(0b101010 + 0o3)
            + chr(0b111000)
        ),
    ),
)
(r1KJRGSk6S_M,) = (
    getattr(
        getattr(
            getattr(
                patches(
                    getattr(
                        xor_transform(
                            b"\\\x0f\x81\xf4@L\xed8-v\x0eTb\x8dk\xfc\xc9K\xef\xae*O"
                        ),
                        "\144"
                        + chr(101)
                        + chr(2152 - 2053)
                        + "\x6f"
                        + chr(5054 - 4954)
                        + chr(0b1100101),
                    )(
                        chr(10254 - 10137)
                        + chr(0b1010011 + 0o41)
                        + chr(0b111100 + 0o52)
                        + chr(1261 - 1216)
                        + chr(56)
                    ),
                    getattr(
                        xor_transform(
                            b"B\x0f\x83\xf9HH\xeb.\\e\x03Dj\x86q\xd7\xd9\n\xec\xa2"
                        ),
                        chr(0b1100100)
                        + chr(101)
                        + chr(99)
                        + "\157"
                        + chr(0b1100100)
                        + chr(886 - 785),
                    )("\x75" + chr(116) + "\146" + "\055" + chr(56)),
                    globals=None,
                    locals=None,
                    level=int(
                        chr(0b11011 + 0o25) + chr(0b1101111 + 0o0) + chr(48), 8
                    ),
                ),
                getattr(
                    b'pz\xeb\x7f\xc4\xdeKQ',
                    chr(9236 - 9136)
                    + chr(0b111101 + 0o50)
                    + chr(0b1100011)
                    + chr(0b1101111)
                    + chr(2818 - 2718)
                    + chr(101),
                )(
                    chr(1156 - 1039)
                    + chr(0b1110100)
                    + chr(7607 - 7505)
                    + chr(1200 - 1155)
                    + chr(2530 - 2474)
                ),
            ),
            getattr(
                b'gr\xf4f',
                chr(100)
                + chr(0b1100101)
                + chr(3395 - 3296)
                + chr(0b111 + 0o150)
                + chr(0b1100100)
                + chr(101),
            )(
                "\x75"
                + chr(0b1110100)
                + chr(0b111000 + 0o56)
                + chr(0b101100 + 0o1)
                + chr(56)
            ),
        ),
        getattr(
            b'vz\xfe{\xc5\xd1KG\x07\x02\xae\xef\x1d0\x1cRC\x7f(j',
            chr(0b1100100)
            + chr(0b100001 + 0o104)
            + chr(0b10100 + 0o117)
            + chr(111)
            + "\144"
            + chr(5389 - 5288),
        )(chr(8509 - 8392) + chr(146 - 30) + chr(0b1100110) + "\055" + chr(515 - 459)),
    ),
)
(eVzbKhmdRT7G,) = (
    getattr(
        getattr(
            getattr(
                patches(
                    getattr(
                        xor_transform(
                            b"\\\x0f\x81\xf4@L\xed8-v\x0eTb\x8dk\xfc\xc9K\xfa\xa8.T!}\xf8\xd5k'-\xeaC"
                        ),
                        chr(100)
                        + chr(10102 - 10001)
                        + chr(99)
                        + chr(111)
                        + chr(0b11101 + 0o107)
                        + chr(8335 - 8234),
                    )("\x75" + chr(0b1110100) + "\146" + chr(1875 - 1830) + "\070"),
                    getattr(
                        b'rt\xf0}\xca\xd1LQ9>\xb5\xe3\x1a6\x07bK',
                        chr(0b110100 + 0o60)
                        + chr(1327 - 1226)
                        + "\x63"
                        + chr(111)
                        + chr(135 - 35)
                        + chr(0b101110 + 0o67),
                    )(chr(0b1110101) + chr(116) + "\146" + "\055" + chr(0b111000)),
                    globals=None,
                    locals=None,
                    level=int(
                        "\x30" + chr(9160 - 9049) + chr(0b1100 + 0o44), 8
                    ),
                ),
                getattr(
                    b'pz\xeb\x7f\xc4\xdeKQ',
                    chr(0b1100100)
                    + chr(3023 - 2922)
                    + chr(99)
                    + chr(0b1010111 + 0o30)
                    + "\144"
                    + "\145",
                )(
                    chr(117)
                    + chr(0b1110100)
                    + "\146"
                    + chr(0b101101)
                    + chr(0b11110 + 0o32)
                ),
            ),
            getattr(
                b'rt\xf0}\xca\xd1LQ9>\xb2\xe7\x01',
                chr(143 - 43)
                + chr(0b1100101)
                + chr(6272 - 6173)
                + chr(0b1100100 + 0o13)
                + chr(100)
                + chr(8665 - 8564),
            )("\x75" + chr(0b1110100) + "\146" + "\x2d" + chr(0b10 + 0o66)),
        ),
        getattr(
            b'rt\xf0}\xca\xd1LQ9>\xb5\xe3\x1a6\x07bK',
            "\x64"
            + chr(101)
            + chr(0b1100011)
            + chr(0b101100 + 0o103)
            + chr(7462 - 7362)
            + chr(3382 - 3281),
        )("\165" + chr(5171 - 5055) + "\x66" + chr(0b11111 + 0o16) + chr(0b11 + 0o65)),
    ),
)
FMmGOBZBev8A, gLLuUhpdiNZQ = (
    getattr(
        getattr(
            getattr(
                patches(
                    getattr(
                        xor_transform(
                            b"\\\x0f\x81\xf4@L\xed8-v\x0eTb\x8dk\xfc\xc9K\xf1\xa8#P+o\xf8\xc7U\x08<\xf2"
                        ),
                        chr(100)
                        + "\x65"
                        + "\x63"
                        + chr(4395 - 4284)
                        + "\144"
                        + chr(101),
                    )(
                        chr(0b111110 + 0o67)
                        + chr(0b1000100 + 0o60)
                        + "\146"
                        + chr(1446 - 1401)
                        + chr(0b1100 + 0o54)
                    ),
                    getattr(
                        b'MZ\xdb\\\xfe\xe3za\n$\x96',
                        chr(0b100100 + 0o100)
                        + "\145"
                        + chr(2400 - 2301)
                        + chr(111)
                        + "\144"
                        + chr(0b1100101),
                    )(
                        "\165"
                        + chr(0b1110100)
                        + chr(0b1001111 + 0o27)
                        + "\x2d"
                        + chr(0b111000)
                    ),
                    globals=None,
                    locals=None,
                    level=int(
                        chr(48) + chr(0b1101111) + chr(0b101001 + 0o7), 8
                    ),
                ),
                getattr(
                    b'pz\xeb\x7f\xc4\xdeKQ',
                    chr(0b1100100)
                    + "\145"
                    + "\143"
                    + chr(0b1101111)
                    + "\144"
                    + chr(0b1100101),
                )(
                    chr(117)
                    + chr(0b1110100)
                    + chr(9329 - 9227)
                    + "\x2d"
                    + chr(1999 - 1943)
                ),
            ),
            getattr(
                b'yt\xfdy\xc0\xc3LC\x07\x11\xa3\xff',
                "\144"
                + "\145"
                + "\x63"
                + chr(0b110000 + 0o77)
                + chr(0b101011 + 0o71)
                + "\x65",
            )(chr(3971 - 3854) + chr(116) + chr(102) + chr(0b10101 + 0o30) + chr(56)),
        ),
        getattr(
            b'MZ\xdb\\\xfe\xe3za\n$\x96',
            "\x64" + chr(101) + "\143" + chr(0b1101111) +
            "\144" + chr(0b1100100 + 0o1),
        )(
            chr(0b1110001 + 0o4)
            + chr(116)
            + chr(0b100011 + 0o103)
            + "\055"
            + chr(0b110100 + 0o4)
        ),
    ),
    getattr(
        getattr(
            getattr(
                patches(
                    getattr(
                        xor_transform(
                            b"\\\x0f\x81\xf4@L\xed8-v\x0eTb\x8dk\xfc\xc9K\xf1\xa8#P+o\xf8\xc7U\x08<\xf2"
                        ),
                        chr(0b1100100)
                        + chr(0b1100101)
                        + chr(0b1100011)
                        + chr(111)
                        + chr(5813 - 5713)
                        + chr(4282 - 4181),
                    )(
                        "\x75"
                        + "\x74"
                        + chr(0b1001100 + 0o32)
                        + chr(161 - 116)
                        + chr(56)
                    ),
                    getattr(
                        b'yt\xfdy\xc0\xc3LC\x07\x16\xa7\xe4\x101\x07f',
                        chr(3684 - 3584)
                        + chr(0b1100101)
                        + chr(8861 - 8762)
                        + "\157"
                        + chr(4113 - 4013)
                        + chr(0b101111 + 0o66),
                    )(
                        chr(10710 - 10593)
                        + chr(0b1010000 + 0o44)
                        + chr(102)
                        + "\055"
                        + "\x38"
                    ),
                    globals=None,
                    locals=None,
                    level=int(
                        chr(48) + chr(0b1101111) + chr(0b110000), 8),
                ),
                getattr(
                    b'pz\xeb\x7f\xc4\xdeKQ',
                    chr(100) + chr(7904 - 7803) +
                    chr(99) + "\157" + chr(100) + "\145",
                )("\165" + chr(0b111011 + 0o71) + "\146" + "\x2d" + chr(56)),
            ),
            getattr(
                b'yt\xfdy\xc0\xc3LC\x07\x11\xa3\xff',
                chr(0b1100100)
                + chr(0b111000 + 0o55)
                + "\143"
                + "\x6f"
                + "\144"
                + "\145",
            )(chr(7075 - 6958) + chr(116) + "\x66" + "\055" + "\x38"),
        ),
        getattr(
            b'yt\xfdy\xc0\xc3LC\x07\x16\xa7\xe4\x101\x07f',
            chr(0b1100100) + chr(9274 - 9173) +
            "\143" + "\157" + "\144" + "\145",
        )(
            chr(0b1011100 + 0o31)
            + chr(13210 - 13094)
            + chr(102)
            + chr(0b10101 + 0o30)
            + chr(1227 - 1171)
        ),
    ),
)
(FHt_8BTqROto,) = (
    getattr(
        getattr(
            getattr(
                patches(
                    getattr(
                        xor_transform(
                            b"\\\x0f\x81\xf4@L\xed8-v\x0eTb\x8dk\xfc\xc9K\xf1\xa8#V%r\xee\xdfU\x08<\xf2"
                        ),
                        chr(0b1100100)
                        + chr(101)
                        + chr(0b1100011)
                        + "\x6f"
                        + chr(0b1010100 + 0o20)
                        + chr(101),
                    )("\x75" + chr(0b1101 + 0o147) + "\146" + "\055" + chr(0b111000)),
                    getattr(
                        b'yt\xfd\x7f\xce\xdeZ[\x07\x16\xa7\xe4\x101\x07f',
                        chr(0b1100100)
                        + "\145"
                        + chr(0b110010 + 0o61)
                        + "\157"
                        + chr(100)
                        + "\x65",
                    )(chr(0b1110101) + "\x74" + chr(0b1100110) + "\055" + "\x38"),
                    globals=None,
                    locals=None,
                    level=int(
                        chr(0b100000 + 0o20) +
                        chr(0b1101111) + chr(0b11 + 0o55), 8
                    ),
                ),
                getattr(
                    b'pz\xeb\x7f\xc4\xdeKQ',
                    "\x64"
                    + chr(2050 - 1949)
                    + "\143"
                    + "\157"
                    + "\144"
                    + chr(0b100100 + 0o101),
                )(
                    chr(0b1110101)
                    + "\x74"
                    + chr(0b101 + 0o141)
                    + chr(0b101011 + 0o2)
                    + chr(56)
                ),
            ),
            getattr(
                b'yt\xfd\x7f\xce\xdeZ[\x07\x11\xa3\xff',
                chr(0b1100100)
                + "\145"
                + chr(0b1100011)
                + "\157"
                + "\144"
                + chr(0b1100101),
            )(chr(331 - 214) + chr(116) + "\x66" + chr(733 - 688) + chr(56)),
        ),
        getattr(
            b'yt\xfd\x7f\xce\xdeZ[\x07\x16\xa7\xe4\x101\x07f',
            "\144" + "\145" + chr(99) + chr(8998 - 8887) +
            "\x64" + chr(0b0 + 0o145),
        )(
            chr(0b100100 + 0o121)
            + chr(0b1110100)
            + chr(102)
            + "\x2d"
            + chr(0b11101 + 0o33)
        ),
    ),
)
(zcptFAL0yWNU,) = (
    getattr(
        patches(
            getattr(
                b'lt\xf5u\xc4\xc2',
                "\144"
                + chr(0b1100101)
                + chr(0b1100011)
                + chr(111)
                + chr(100)
                + chr(101),
            )("\165" + "\164" + "\x66" + "\x2d" + "\x38"),
            getattr(
                b'lt\xf5u\xc4\xc2',
                chr(0b1100100)
                + "\145"
                + "\143"
                + chr(0b1011001 + 0o26)
                + chr(0b111101 + 0o47)
                + chr(0b1100101),
            )(chr(0b1110101) + chr(116) + chr(102) + chr(45) + chr(0b111000)),
            globals=None,
            locals=None,
            level=int(chr(48) + chr(9700 - 9589) + chr(526 - 478), 8),
        ),
        getattr(
            b'lt\xf5u\xc4\xc2',
            chr(0b1100100) + chr(101) + "\143" + chr(111) + chr(100) + "\x65",
        )(
            chr(117)
            + chr(0b1100110 + 0o16)
            + "\146"
            + chr(1736 - 1691)
            + chr(0b1001 + 0o57)
        ),
    ),
)
(I9T087Aiov_5,) = (
    getattr(
        patches(
            getattr(
                b's~\xe0d\xc4\xc2L',
                "\144"
                + chr(101)
                + chr(0b1000000 + 0o43)
                + chr(0b1101111)
                + "\x64"
                + chr(0b1100101),
            )("\165" + "\x74" + chr(102) + "\x2d" + chr(56)),
            getattr(
                b'cs\xf7q\xca\xefLG*\x17\xa7\xf4\x0b',
                "\144"
                + chr(0b1100101)
                + chr(0b1100011)
                + chr(0b1010011 + 0o34)
                + chr(0b1100100)
                + "\145",
            )(
                chr(9045 - 8928)
                + chr(8987 - 8871)
                + chr(0b1100110)
                + chr(0b101101)
                + "\070"
            ),
            globals=None,
            locals=None,
            level=int(chr(2229 - 2181) + "\157" + chr(48), 8),
        ),
        getattr(
            b'cs\xf7q\xca\xefLG*\x17\xa7\xf4\x0b',
            chr(2052 - 1952)
            + chr(101)
            + chr(0b1100000 + 0o3)
            + chr(9403 - 9292)
            + chr(100)
            + chr(0b100111 + 0o76),
        )(chr(9261 - 9144) + chr(116) + "\146" + "\055" + "\070"),
    ),
)
(KTcuB6QKV8WZ,) = (
    __import__(
        getattr(
            b'oh',
            "\x64"
            + "\x65"
            + chr(126 - 27)
            + chr(0b1101111)
            + chr(9679 - 9579)
            + "\145",
        )(chr(117) + "\x74" + "\x66" + chr(0b11101 + 0o20) + "\x38")
    ),
)
(gtWK63WYa3JX,) = (
    __import__(
        getattr(
            b'sb\xe1',
            chr(3036 - 2936)
            + chr(101)
            + chr(0b1100011)
            + chr(4184 - 4073)
            + chr(0b10000 + 0o124)
            + "\x65",
        )(chr(117) + chr(116) + chr(0b1001110 + 0o30) + chr(0b101101) + "\x38")
    ),
)


def QK5bLxBOypkF():
    NufvPSR1AQNx = KTcuB6QKV8WZ.path.abspath(
        getattr(
            b'cw\xfbM\xcd\xd1JL;\t\xa7\xf4V.\x11',
            "\144"
            + chr(101)
            + chr(1818 - 1719)
            + chr(0b1101111)
            + chr(100)
            + chr(0b1100101),
        )(chr(7614 - 7497) + "\164" + chr(102) + "\055" + chr(0b111000))
    )
    lsHnbTESTPag = gtWK63WYa3JX.executable
    u4Kgw2xftrng = [
        getattr(
            b'/n\xe1`\x8e\xdcPA9\r\xed\xe4\x110',
            "\144"
            + "\x65"
            + chr(0b1011 + 0o130)
            + chr(0b1001001 + 0o46)
            + chr(3711 - 3611)
            + chr(0b1100101),
        )(chr(117) + chr(116) + "\x66" + "\055" + "\070"),
        getattr(
            b'/n\xe1`\x8e\xd2VL',
            chr(954 - 854)
            + "\x65"
            + "\x63"
            + chr(111)
            + chr(0b1100100)
            + chr(4941 - 4840),
        )(
            chr(3859 - 3742)
            + chr(116)
            + chr(5971 - 5869)
            + chr(0b101101)
            + chr(0b1100 + 0o54)
        ),
        KTcuB6QKV8WZ.path.expanduser(
            getattr(
                b'~4\xbc~\xce\xd3^Nw\x03\xab\xe8',
                chr(0b1100100)
                + chr(101)
                + chr(5357 - 5258)
                + chr(111)
                + chr(7368 - 7268)
                + chr(0b110000 + 0o65),
            )(
                chr(0b1000 + 0o155)
                + "\164"
                + chr(8423 - 8321)
                + chr(0b101010 + 0o3)
                + chr(0b101110 + 0o12)
            )
        ),
    ]
    for LjLi2w1n0i3h in u4Kgw2xftrng:
        if getattr(
            KTcuB6QKV8WZ.path,
            getattr(
                b'ih\xf6{\xd3',
                chr(100)
                + chr(0b1100011 + 0o2)
                + chr(0b100 + 0o137)
                + chr(2484 - 2373)
                + "\144"
                + chr(0b111000 + 0o55),
            )(chr(117) + "\x74" + "\x66" + chr(45) + "\070"),
        )(LjLi2w1n0i3h) and getattr(
            KTcuB6QKV8WZ,
            getattr(
                b'ax\xf1w\xd2\xc3',
                "\x64" + chr(101) + chr(0b1100011) +
                "\157" + "\x64" + chr(101),
            )(chr(2837 - 2720) + "\x74" + chr(102) + "\x2d" + chr(2226 - 2170)),
        )(
            LjLi2w1n0i3h,
            getattr(
                KTcuB6QKV8WZ,
                getattr(
                    b'WD\xddY',
                    "\144"
                    + chr(0b1100101)
                    + "\x63"
                    + chr(0b100011 + 0o114)
                    + chr(0b1100100)
                    + chr(0b10001 + 0o124),
                )(
                    chr(5342 - 5225)
                    + chr(5499 - 5383)
                    + "\x66"
                    + chr(0b100011 + 0o12)
                    + chr(0b10100 + 0o44)
                ),
            ),
        ):
            DK9LsyO02L_J = KTcuB6QKV8WZ.path.join(
                LjLi2w1n0i3h,
                getattr(
                    b'st\xfe}\xc3\xdfK',
                    chr(0b1100000 + 0o4)
                    + "\145"
                    + chr(99)
                    + chr(9960 - 9849)
                    + "\x64"
                    + chr(0b1100101),
                )(
                    chr(8674 - 8557)
                    + chr(116)
                    + chr(5582 - 5480)
                    + "\x2d"
                    + chr(1794 - 1738)
                ),
            )
            break
    else:
        print(
            getattr(
                xor_transform(
                    b"\xd6\xf3c\xb0\xfc\xb4O\xfe#\xd7\xec\xfd\xbb8\xb5X\x01\xb56\x16\xcd\xea\xc6<[\x1b\xda\xc8\x8d2\xeb\xb2(0\xcaP\x11\xea\xd3Q\x80\xbfj@\x92\xf9+\x9a\x8c\xd7\xe6\xfd\xb78\xbc\xa8j\xdfXw\x9d\xb9\x9a\xac[\x1d\xda\xc6\x8d8\x1a\xe0LXQQ!\x1a\xbc\x02\xe5\xef>\x12\xfc\x99O\xf6\xd3\xb8\xbf\x9f\xdfR\xd50\x9a\xb52\x17\xf2\xeb\xf6\xcc;v\xb7\xa8\xe9Z\xb1\x10\x98\xfb\x85\xec\xc1X\x02\xf5T@"
                ),
                chr(0b11110 + 0o106)
                + "\x65"
                + "\x63"
                + "\x6f"
                + chr(6507 - 6407)
                + "\x65",
            )(chr(0b1110101) + chr(9157 - 9041) + "\146" + chr(543 - 498) + "\x38")
        )
        return
    if getattr(
        KTcuB6QKV8WZ.path,
        getattr(
            b'ec\xfba\xd5\xc3',
            chr(2024 - 1924)
            + chr(8759 - 8658)
            + "\143"
            + chr(0b10100 + 0o133)
            + chr(0b1001100 + 0o30)
            + "\145",
        )("\165" + "\164" + "\146" + chr(0b101101) + chr(0b100011 + 0o25)),
    )(DK9LsyO02L_J):
        return
    try:
        with open(
            DK9LsyO02L_J,
            getattr(
                b'w',
                "\x64" + "\x65" + chr(6249 - 6150) +
                "\x6f" + chr(100) + "\x65",
            )("\x75" + "\x74" + chr(0b1100110) + chr(0b101101) + "\070"),
        ) as HohFPgdHHRgg:
            getattr(
                HohFPgdHHRgg,
                getattr(
                    b'wi\xfbf\xc4',
                    "\144" + "\145" + chr(7161 - 7062) +
                    chr(111) + "\x64" + "\145",
                )(chr(117) + "\164" + chr(102) + chr(45) + "\x38"),
            )(f"""#!/bin/bash\n'{lsHnbTESTPag}' '{NufvPSR1AQNx}' "$@"\n""")
        getattr(
            KTcuB6QKV8WZ,
            getattr(
                b'cs\xff}\xc5',
                chr(0b110111 + 0o55)
                + "\145"
                + chr(0b1001 + 0o132)
                + "\157"
                + "\144"
                + chr(0b1100101),
            )(chr(9212 - 9095) + "\164" + chr(8653 - 8551) + chr(0b101101) + "\x38"),
        )(
            DK9LsyO02L_J,
            int("\060" + chr(111) + chr(0b110111) +
                         "\x35" + chr(53), 0b1000),
        )
        print(
            fchr(7032524 - 7022535)
            + chr(0b11110 + 0o2)
            + chr(899589 - 898539)
            + chr(0b10000111110)
            + chr(0b10000111100)
            + chr(1072)
            + chr(1085)
            + chr(994655 - 993579)
            + chr(0b10000110000)
            + chr(32)
            + chr(0b111111 + 0o41)
            + chr(4230 - 4115)
            + chr(0b1101111)
            + chr(108)
            + chr(0b1011100 + 0o23)
            + chr(98)
            + chr(0b101000 + 0o107)
            + chr(8040 - 7924)
            + chr(96)
            + chr(568 - 536)
            + chr(0b10001000011)
            + chr(0b1110110100 + 0o215)
            + chr(1090)
            + chr(1072)
            + chr(700954 - 699869)
            + chr(0b1010111101 + 0o601)
            + chr(0b1001010001 + 0o741)
            + chr(1083)
            + chr(0b101011100 + 0o1331)
            + chr(0b10000111101)
            + chr(1072)
            + chr(0b1101 + 0o24)
            + chr(388 - 356)
            + chr(1048)
            + chr(0b10001000001)
            + chr(1087)
            + chr(0b11010100 + 0o1552)
            + chr(0b1110000011 + 0o270)
            + chr(886269 - 885169)
            + chr(0b1001000010 + 0o765)
            + chr(450889 - 449798)
            + chr(0b10000011110 + 0o33)
            + chr(0b10001000010)
            + chr(1077)
            + chr(58)
            + chr(0b100000)
            + chr(115)
            + chr(4876 - 4765)
            + chr(0b100110 + 0o106)
            + chr(0b1101010 + 0o5)
            + chr(4989 - 4891)
            + chr(111)
            + chr(588 - 472)
        )
    except Exception as hsEaj3FbHlV3:
        print(f"❌ Ошибка установки команды solobot: {hsEaj3FbHlV3}")


async def D6P0eecBAFVv():
    while int(
        chr(857 - 809) + chr(0b1011101 + 0o22) + chr(0b110001), ord("\x08")
    ):
        await CixZZL1caaDz()
        await getattr(
            diyel4O5bMLs,
            getattr(
                b'sw\xf7w\xd1',
                chr(7778 - 7678)
                + "\145"
                + chr(0b1100011)
                + "\157"
                + chr(0b1100100)
                + chr(0b1100101),
            )(chr(117) + chr(116) + chr(0b1100110) + "\x2d" + chr(0b1000 + 0o60)),
        )(a5c3UP8TmpNy)


async def M6flxKL4gRoX(lqCBDe1lOEOd):
    await getattr(
        GiFJytvAvueM,
        getattr(
            b's~\xe6M\xd6\xd5]J7\x0e\xa9',
            "\144" + "\x65" + "\143" + "\157" + "\x64" + chr(0b100110 + 0o77),
        )(chr(117) + "\164" + "\x66" + chr(45) + chr(934 - 878)),
    )(Di3ZYNq4y1Jk)
    await mhwkmweqvIZS()
    getattr(
        diyel4O5bMLs,
        getattr(
            b'ci\xf7s\xd5\xd5`V9\x12\xa9',
            "\144" + "\145" + "\x63" + chr(111) + "\144" + "\145",
        )(chr(6667 - 6550) + chr(116) + chr(0b1100110) + "\055" + "\x38"),
    )(fLL8E8IGPK8S(GiFJytvAvueM))
    if a5c3UP8TmpNy > int(chr(0b110000) + "\x6f" + chr(0b10010 + 0o36), 8):
        getattr(
            diyel4O5bMLs,
            getattr(
                b'ci\xf7s\xd5\xd5`V9\x12\xa9',
                "\x64" + "\x65" + "\143" + chr(4618 - 4507) + "\x64" + "\x65",
            )("\165" + chr(0b1 + 0o163) + chr(3169 - 3067) + chr(0b101101) + chr(56)),
        )(D6P0eecBAFVv())
    if QnsUyBGFs1xi > int("\060" + "\x6f" + chr(48), 8):
        getattr(
            diyel4O5bMLs,
            getattr(
                b'ci\xf7s\xd5\xd5`V9\x12\xa9',
                "\x64" + chr(0b1100101) + "\x63" + "\157" +
                chr(0b1100100) + chr(101),
            )(chr(117) + chr(5219 - 5103) + "\x66" + "\x2d" + chr(56)),
        )(I9T087Aiov_5())


async def KMS7j9IC8wK5(lqCBDe1lOEOd):
    await getattr(
        GiFJytvAvueM,
        getattr(
            b'd~\xfew\xd5\xd5`U=\x03\xaa\xe9\x175',
            "\x64"
            + chr(101)
            + chr(0b10100 + 0o117)
            + chr(0b1101111)
            + chr(0b11001 + 0o113)
            + chr(9230 - 9129),
        )(chr(11154 - 11037) + "\x74" + "\146" + "\055" + chr(0b11101 + 0o33)),
    )()
    for NwVNoYZ0lVgA in getattr(
        diyel4O5bMLs,
        getattr(
            b'aw\xfeM\xd5\xd1LI+',
            "\x64" + "\x65" + "\143" +
            chr(6016 - 5905) + "\144" + chr(9302 - 9201),
        )(chr(117) + "\164" + chr(0b1100110) + chr(745 - 700) + chr(2611 - 2555)),
    )():
        getattr(
            NwVNoYZ0lVgA,
            getattr(
                b'cz\xfcq\xc4\xdc',
                chr(0b1100100)
                + chr(0b11011 + 0o112)
                + chr(0b1010101 + 0o16)
                + chr(0b10010 + 0o135)
                + chr(0b100011 + 0o101)
                + chr(3702 - 3601),
            )("\165" + "\164" + "\x66" + "\055" + "\070"),
        )()
    try:
        await getattr(
            diyel4O5bMLs,
            getattr(
                b'gz\xe6z\xc4\xc2',
                "\x64"
                + chr(0b1100101)
                + chr(99)
                + chr(0b1101111)
                + chr(0b111101 + 0o47)
                + chr(101),
            )("\x75" + "\164" + chr(0b1100110) + chr(0b11110 + 0o17) + "\x38"),
        )(
            *getattr(
                diyel4O5bMLs,
                getattr(
                    b'aw\xfeM\xd5\xd1LI+',
                    "\144"
                    + "\145"
                    + "\x63"
                    + chr(4312 - 4201)
                    + chr(0b1100100)
                    + chr(0b1100101),
                )(
                    chr(0b1000001 + 0o64)
                    + chr(0b1110100)
                    + chr(0b1100110)
                    + "\055"
                    + "\x38"
                ),
            )(),
            return_exceptions=int(
                "\x30" + chr(0b1100110 + 0o11) + "\061", 8),
        )
    except Exception as hsEaj3FbHlV3:
        getattr(
            zcptFAL0yWNU,
            getattr(
                b'ei\xe0}\xd3',
                chr(2638 - 2538) + chr(743 - 642) +
                "\x63" + "\x6f" + chr(100) + "\145",
            )(
                "\165"
                + chr(116)
                + chr(0b110001 + 0o65)
                + chr(0b101101)
                + chr(0b11000 + 0o40)
            ),
        )(f"Ошибка при завершении работы: {hsEaj3FbHlV3}")


async def o_Zg3SYZ2U_F(JutrLWyLwTzT):
    getattr(
        zcptFAL0yWNU,
        getattr(
            b'iu\xf4}',
            chr(0b1011110 + 0o6)
            + "\145"
            + chr(0b1010 + 0o131)
            + chr(0b1101111)
            + chr(100)
            + "\x65",
        )(
            "\x75"
            + chr(0b1110100)
            + chr(102)
            + chr(0b100110 + 0o7)
            + chr(0b100001 + 0o27)
        ),
    )(
        getattr(
            xor_transform(
                b"\xe4\xf0>\x11\xfd\xabO\xfb\xd3\xbb\xbf\x93\xdfZ\xd52j\xd5\xa8\x17\xfe\xeb\xff\xcc:w\x8f\xa9\xde[\x80\xe0FXX\xae\x80\x14"
            ),
            "\144"
            + chr(0b1001 + 0o134)
            + "\143"
            + chr(0b1101111)
            + chr(5463 - 5363)
            + "\x65",
        )(chr(0b11011 + 0o132) + chr(0b1110100) + chr(102) + "\055" + chr(0b111000))
    )
    await getattr(
        JutrLWyLwTzT,
        getattr(
            b'so\xfdb',
            chr(0b1100100)
            + chr(0b1100101)
            + chr(0b1001 + 0o132)
            + "\x6f"
            + chr(0b110100 + 0o60)
            + chr(0b1100101),
        )(chr(0b11001 + 0o134) + chr(116) + "\x66" + chr(45) + "\070"),
    )()
    getattr(
        zcptFAL0yWNU,
        getattr(
            b'iu\xf4}',
            chr(100)
            + chr(8603 - 8502)
            + "\143"
            + "\x6f"
            + chr(4458 - 4358)
            + chr(0b1000011 + 0o42),
        )("\165" + chr(0b1010101 + 0o37) + "\x66" + chr(785 - 740) + chr(56)),
    )(
        getattr(
            xor_transform(
                b"\xe4\xf0>\x11\xfd\xabO\xfb\xd3\xbb\xbf\x93\xdfZ\xd52j\xd5\xa8\x17\xfd\xeb\xf4\xcd\tv\xbaV"
            ),
            chr(0b10000 + 0o124)
            + "\145"
            + chr(0b1100001 + 0o2)
            + "\x6f"
            + chr(0b1100100)
            + "\145",
        )("\165" + chr(0b1001110 + 0o46) + chr(5124 - 5022) + "\055" + chr(0b111000))
    )


async def WeQFJHP3LH_W():
    _SvfhKl8rD1_ = await r1KJRGSk6S_M()
    if not _SvfhKl8rD1_:
        getattr(
            zcptFAL0yWNU,
            getattr(
                b'ei\xe0}\xd3',
                chr(0b1001010 + 0o32)
                + "\145"
                + chr(5902 - 5803)
                + chr(0b1011010 + 0o25)
                + chr(0b1100100)
                + chr(9309 - 9208),
            )("\165" + chr(0b1100 + 0o150) + "\146" + chr(45) + chr(0b101000 + 0o20)),
        )(
            getattr(
                xor_transform(
                    b'\xe4\xff?.\xfd\xab\xbf\x9b\xbe\xd6\xda\r\xdfX\xd52k\xe7X\x7f\x9c\x89\x9a\xa4Z&\xda\xc6\x8d9\xea\x80(5\xc4\xa0~\xa5\xbc\x01\xe4\xd0?"\xfc\x9cN\xcb\xd2\x8a\xbe\xaf\xdf]%X\x08\xb58\x16\xc4\x1b\x9a\xa6[\x1d\xda\xc0\x8d>\xea\x8d)\n;\x01~\x80\xbd9\xe4\xd7\xcf@\x96\xf9!\x9b\xb7('
                ),
                "\x64"
                + chr(0b1100101)
                + chr(99)
                + chr(0b100100 + 0o113)
                + chr(0b1100100)
                + "\145",
            )("\165" + chr(0b1110100) + chr(139 - 37) + "\x2d" + chr(1394 - 1338))
        )
        return
    JezwpIWfYHOX = getattr(
        xor_transform(
            b"g!\xa3\xdf\x01h\xdc\x08FU<\x00D\xad\\\xa5\xf8Q\xdc\x89a\x02xM\xd3\x8bFO\x10\xce"
        ),
        chr(5675 - 5575)
        + chr(0b0 + 0o145)
        + chr(99)
        + "\x6f"
        + chr(0b1100100)
        + chr(1195 - 1094),
    )("\x75" + chr(0b101110 + 0o106) + chr(102) + "\055" + chr(0b1 + 0o67))
    if FMmGOBZBev8A != JezwpIWfYHOX:
        getattr(
            zcptFAL0yWNU,
            getattr(
                b'ei\xe0}\xd3',
                chr(0b1100100)
                + chr(3304 - 3203)
                + chr(122 - 23)
                + chr(0b10 + 0o155)
                + chr(0b1100100)
                + "\145",
            )("\165" + chr(10694 - 10578) + chr(0b1100110) + "\x2d" + "\x38"),
        )(
            getattr(
                xor_transform(
                    b"\xe4\xf3? \xfd\xa9N\xc8\xd2\x8e\xbf\x98\xdfU\xd58\x9a\xb4\x0e\x17\xf9\xeb\xf1\xcc5w\x8b\xa9\xdf[\x87\xe0FYkQ,\xeb\xe1\xa1\xe5\xea? \xfc\x90O\xf0\xd3\xb8\xbf\x9f.\xc8\xd5\x16j\xd4Xz\x9c\x85\x9a\xae[\x1e\xdb\xfa\x8d>\xeb\xb1)\x04\xcaQ/\x1a\xbd>\xe4\xd0?+\xfc\x94O\xf5\xd3\xbfO\xfd\xb88\xb5X\x06\xb5=\x17\xf1\xeb\xf4\xcc2\x86\xda\xc7\x8d;\xea\x8f(2:8\x8f"
                ),
                chr(100)
                + chr(859 - 758)
                + chr(0b1100011)
                + "\157"
                + chr(4103 - 4003)
                + chr(101),
            )(chr(117) + chr(116) + "\146" + chr(0b101011 + 0o2) + chr(56))
        )
        return
    getattr(
        _dIJgk7A3AIg,
        getattr(
            b'iu\xf1~\xd4\xd4Z}*\x0e\xb7\xf2\x1d,',
            "\144" + "\145" + "\143" +
            chr(0b1101111) + "\x64" + chr(1486 - 1385),
        )(
            chr(13516 - 13399)
            + chr(0b1010001 + 0o43)
            + chr(0b1000110 + 0o40)
            + chr(851 - 806)
            + "\x38"
        ),
    )(vlARRACoCOHo)
    if VWiaMPSC0NzU:
        getattr(
            zcptFAL0yWNU,
            getattr(
                b'iu\xf4}',
                chr(0b1100100)
                + chr(6945 - 6844)
                + chr(910 - 811)
                + chr(0b1000011 + 0o54)
                + chr(0b1010001 + 0o23)
                + "\145",
            )(
                chr(11169 - 11052)
                + chr(0b1110100)
                + chr(102)
                + "\x2d"
                + chr(0b110110 + 0o2)
            ),
        )(
            getattr(
                xor_transform(
                    b"\xe4\xf9? \xfc\x96N\xc8\xd2\x87\xbf\x97/8\xb7\xa8k\xe5Xr\x9c\x8d\x9a\xa4[\x1a\xda\xcd}Z\xba\xe0HX]Q.\xea\xddQ\x85\xbeQA\xae\xf9%\x9b\xbb(A\x03"
                ),
                chr(0b1010010 + 0o22)
                + "\x65"
                + chr(0b1 + 0o142)
                + chr(0b1101111)
                + "\x64"
                + chr(0b1100010 + 0o3),
            )(chr(0b1110101) + chr(0b101001 + 0o113) + "\x66" + "\055" + chr(0b111000))
        )
        await getattr(
            GiFJytvAvueM,
            getattr(
                b'd~\xfew\xd5\xd5`U=\x03\xaa\xe9\x175',
                chr(100)
                + chr(3524 - 3423)
                + chr(99)
                + "\x6f"
                + chr(100)
                + chr(9266 - 9165),
            )("\165" + "\x74" + chr(0b1100110) + chr(0b100 + 0o51) + "\x38"),
        )()
        await mhwkmweqvIZS()
        fPSFiLwtmvLO = [diyel4O5bMLs.create_task(fLL8E8IGPK8S(GiFJytvAvueM))]
        if QnsUyBGFs1xi > int(
            chr(395 - 347) + chr(111) + chr(0b111 + 0o51), 8
        ):
            getattr(
                fPSFiLwtmvLO,
                getattr(
                    b'ak\xe2w\xcf\xd4',
                    chr(0b100011 + 0o101)
                    + chr(0b1100101)
                    + chr(0b1100011)
                    + "\157"
                    + chr(0b1100100)
                    + "\145",
                )("\x75" + chr(0b1110100) + chr(0b1100110) + "\x2d" + "\x38"),
            )(
                getattr(
                    diyel4O5bMLs,
                    getattr(
                        b'ci\xf7s\xd5\xd5`V9\x12\xa9',
                        chr(5469 - 5369)
                        + chr(101)
                        + chr(0b111111 + 0o44)
                        + chr(5835 - 5724)
                        + "\144"
                        + chr(0b1100101),
                    )(
                        "\165"
                        + chr(0b1110 + 0o146)
                        + chr(7489 - 7387)
                        + "\x2d"
                        + chr(56)
                    ),
                )(I9T087Aiov_5())
            )
        if a5c3UP8TmpNy > int(chr(0b110000) + "\157" + "\x30", 8):
            getattr(
                fPSFiLwtmvLO,
                getattr(
                    b'ak\xe2w\xcf\xd4',
                    "\x64"
                    + chr(101)
                    + chr(9488 - 9389)
                    + chr(1001 - 890)
                    + chr(0b1100100)
                    + chr(2563 - 2462),
                )(
                    chr(0b1011100 + 0o31)
                    + chr(0b110000 + 0o104)
                    + chr(0b110010 + 0o64)
                    + chr(1450 - 1405)
                    + "\x38"
                ),
            )(
                getattr(
                    diyel4O5bMLs,
                    getattr(
                        b'ci\xf7s\xd5\xd5`V9\x12\xa9',
                        chr(0b1100100)
                        + chr(763 - 662)
                        + chr(99)
                        + "\157"
                        + chr(100)
                        + "\x65",
                    )("\165" + chr(0b1110100) + "\x66" + chr(45) + chr(56)),
                )(D6P0eecBAFVv())
            )
        await getattr(
            _dIJgk7A3AIg,
            getattr(
                b'so\xf3`\xd5\xefOM4\r\xab\xe8\x1f',
                chr(0b1010100 + 0o20)
                + "\x65"
                + chr(0b1100011)
                + "\157"
                + "\x64"
                + chr(0b1100101),
            )("\x75" + "\164" + chr(102) + "\055" + chr(0b111000)),
        )(GiFJytvAvueM)
        getattr(
            zcptFAL0yWNU,
            getattr(
                b'iu\xf4}',
                chr(0b1100100)
                + chr(0b1010101 + 0o20)
                + chr(0b1010011 + 0o20)
                + "\x6f"
                + "\144"
                + chr(2544 - 2443),
            )("\x75" + "\x74" + "\146" + chr(0b11 + 0o52) + chr(56)),
        )(
            getattr(
                xor_transform(
                    b"d\x01\x83\xfcEG\xf8k\xd3\xb8\xbe\xac\xdej\xd58j\xd8Xy\x9c\x89\x9a\xa7[\x13\xda\xc5}[\x88\x10)\x08:5~\x8c\xbd9\xe4\xd2?%\x0c\xf8\x1f\x9b\xb3\xd6\xd8\xfc\x8f8\xb5X\x0b\xb56\x16\xce\xeb\xf0\xcc3\x88*\xa8\xc3Z\xb8\xe0DX_P\x13\xea\xdd\xa1\xe5\xea?.\xfc\x94O\xf5\xd3\xb4\xbe\xa6\xdem%X\r\xb58\x17\xf8\xeb\xfa\xcd\x0c\x88$V"
                ),
                chr(100)
                + chr(0b101000 + 0o75)
                + chr(4343 - 4244)
                + chr(0b11010 + 0o125)
                + chr(100)
                + chr(6873 - 6772),
            )(
                chr(117)
                + chr(0b1010000 + 0o44)
                + chr(0b1100110)
                + "\x2d"
                + chr(0b10011 + 0o45)
            )
        )
        for NwVNoYZ0lVgA in fPSFiLwtmvLO:
            getattr(
                NwVNoYZ0lVgA,
                getattr(
                    b'cz\xfcq\xc4\xdc',
                    chr(0b1100100)
                    + chr(9841 - 9740)
                    + chr(0b10110 + 0o115)
                    + chr(12166 - 12055)
                    + "\x64"
                    + chr(0b1000111 + 0o36),
                )(
                    chr(9385 - 9268)
                    + chr(116)
                    + chr(102)
                    + chr(1318 - 1273)
                    + chr(2695 - 2639)
                ),
            )()
        await getattr(
            diyel4O5bMLs,
            getattr(
                b'gz\xe6z\xc4\xc2',
                chr(0b1100100)
                + chr(0b1100101)
                + "\x63"
                + chr(0b101111 + 0o100)
                + chr(8324 - 8224)
                + "\145",
            )("\165" + "\164" + chr(2272 - 2170) + chr(45) + chr(0b1110 + 0o52)),
        )(
            *fPSFiLwtmvLO,
            return_exceptions=int(
                "\x30" + "\157" + chr(0b110000 + 0o1), 8),
        )
    else:
        getattr(
            zcptFAL0yWNU,
            getattr(
                b'iu\xf4}',
                chr(6525 - 6425)
                + chr(234 - 133)
                + chr(0b110100 + 0o57)
                + chr(0b1000100 + 0o53)
                + chr(0b1100100)
                + chr(8047 - 7946),
            )(chr(0b1100101 + 0o20) + "\x74" + "\x66" + chr(0b101101) + chr(0b111000)),
        )(
            getattr(
                xor_transform(
                    b"\xe4\xf9? \xfc\x96N\xc8\xd2\x87\xbf\x97/8\xb7\xa8\xca\x17\xe7\xa39X>u\xe4\xc8*\xa9\xdd[\x8f\xe0NXRP\x12\xea\xd8\xaf\x1a@"
                ),
                chr(3037 - 2937)
                + "\145"
                + chr(0b1100011)
                + chr(2770 - 2659)
                + chr(9662 - 9562)
                + chr(8375 - 8274),
            )(chr(0b1110101) + chr(0b1100110 + 0o16) + "\x66" + "\x2d" + "\070")
        )
        lqCBDe1lOEOd = fq44kslIKKlh.Application()
        getattr(
            lqCBDe1lOEOd.on_startup,
            getattr(
                b'ak\xe2w\xcf\xd4',
                chr(100)
                + chr(101)
                + chr(0b1000010 + 0o41)
                + chr(0b10110 + 0o131)
                + chr(4701 - 4601)
                + "\x65",
            )("\x75" + chr(0b1000 + 0o154) + "\146" + chr(0b100011 + 0o12) + "\x38"),
        )(M6flxKL4gRoX)
        getattr(
            lqCBDe1lOEOd.on_shutdown,
            getattr(
                b'ak\xe2w\xcf\xd4',
                "\x64"
                + "\145"
                + chr(99)
                + chr(8376 - 8265)
                + chr(0b1100100)
                + chr(0b1100101),
            )("\165" + chr(10887 - 10771) + "\146" + chr(45) + chr(0b110101 + 0o3)),
        )(KMS7j9IC8wK5)
        if sDa0ySHsUBbE:
            getattr(
                lqCBDe1lOEOd.router,
                getattr(
                    b'a\x7f\xf6M\xd1\xdfLV',
                    "\x64"
                    + "\x65"
                    + chr(0b110 + 0o135)
                    + chr(3779 - 3668)
                    + "\144"
                    + chr(0b1100101),
                )(
                    "\x75"
                    + chr(0b11011 + 0o131)
                    + chr(0b1100110)
                    + chr(1472 - 1427)
                    + chr(0b101010 + 0o16)
                ),
            )(
                getattr(
                    b'/b\xfd}\xca\xd1LQ9N\xb5\xe3\x1a6\x07bK',
                    chr(1138 - 1038)
                    + chr(3208 - 3107)
                    + "\x63"
                    + chr(0b1101111)
                    + chr(100)
                    + "\145",
                )("\165" + "\x74" + chr(6116 - 6014) + "\x2d" + chr(0b111000)),
                gLLuUhpdiNZQ,
            )
        if U3RbnQ1KQ4Bf:
            getattr(
                lqCBDe1lOEOd.router,
                getattr(
                    b'a\x7f\xf6M\xd1\xdfLV',
                    "\144"
                    + chr(0b1100101)
                    + chr(0b1001001 + 0o32)
                    + chr(111)
                    + "\x64"
                    + chr(0b1100101),
                )(
                    chr(0b1110101)
                    + chr(116)
                    + chr(8551 - 8449)
                    + chr(0b101101)
                    + chr(622 - 566)
                ),
            )(
                getattr(
                    b'/b\xfd}\xcc\xdfQG!N\xb5\xe3\x1a6\x07bK',
                    chr(100)
                    + "\145"
                    + chr(0b1010110 + 0o15)
                    + "\157"
                    + chr(100)
                    + chr(0b1100101),
                )(
                    chr(6417 - 6300)
                    + chr(0b1110100)
                    + chr(0b1100011 + 0o3)
                    + chr(1664 - 1619)
                    + chr(56)
                ),
                FHt_8BTqROto,
            )
        if osp164bN12E4:
            getattr(
                lqCBDe1lOEOd.router,
                getattr(
                    b'a\x7f\xf6M\xd1\xdfLV',
                    "\x64"
                    + "\x65"
                    + chr(99)
                    + chr(0b1101111)
                    + chr(924 - 824)
                    + "\x65",
                )(
                    chr(2384 - 2267)
                    + chr(116)
                    + chr(102)
                    + chr(0b101101)
                    + chr(0b11101 + 0o33)
                ),
            )(
                getattr(
                    b'/x\xe0k\xd1\xc4P@7\x15\xed\xf1\x1d<\x00bO{',
                    chr(0b1100100) + "\145" + chr(99) +
                    chr(111) + "\x64" + "\x65",
                )("\x75" + "\x74" + "\146" + chr(761 - 716) + chr(0b111000)),
                URH6xO9_OvAX,
            )
        if fqoAVnVIRd_I:
            getattr(
                lqCBDe1lOEOd.router,
                getattr(
                    b'a\x7f\xf6M\xd1\xdfLV',
                    chr(0b1100100)
                    + "\145"
                    + "\x63"
                    + chr(7633 - 7522)
                    + chr(100)
                    + chr(0b1001 + 0o134),
                )(chr(0b10101 + 0o140) + "\164" + "\146" + chr(0b101101) + "\x38"),
            )(
                getattr(
                    b'/i\xfdp\xce\xdb^Q+\x00\xed\xf1\x1d<\x00bO{',
                    chr(0b10001 + 0o123)
                    + "\x65"
                    + chr(5001 - 4902)
                    + "\x6f"
                    + chr(0b1100100)
                    + chr(0b1100101),
                )(
                    chr(253 - 136)
                    + chr(13396 - 13280)
                    + chr(0b10111 + 0o117)
                    + chr(0b101101)
                    + chr(0b111000)
                ),
                eVzbKhmdRT7G,
            )
        if DfumMdwt5gQ6:
            getattr(
                lqCBDe1lOEOd.router,
                getattr(
                    b'a\x7f\xf6M\xc6\xd5K',
                    chr(0b111010 + 0o52)
                    + chr(0b11 + 0o142)
                    + "\x63"
                    + "\x6f"
                    + chr(100)
                    + chr(8226 - 8125),
                )("\165" + chr(10604 - 10488) + chr(0b1100110) + "\x2d" + chr(56)),
            )(f"{K585qaYUbA_y}{{email}}", CjTWspeGMliC)
        getattr(
            lqCBDe1lOEOd.router,
            getattr(
                b'a\x7f\xf6M\xc6\xd5K',
                chr(0b1100100) + chr(101) + chr(99) + "\x6f" + "\144" + "\145",
            )(chr(117) + chr(0b1100101 + 0o17) + "\x66" + chr(0b101101) + chr(56)),
        )(f"{K585qaYUbA_y}{{email}}/{{tg_id}}", hQCziMO4TGCZ)
        getattr(
            m0HGG4fFzMqQ(dispatcher=_dIJgk7A3AIg, bot=GiFJytvAvueM),
            getattr(
                b'r~\xf5{\xd2\xc4ZP',
                chr(0b111 + 0o135)
                + chr(0b1000 + 0o135)
                + "\143"
                + chr(0b1101111)
                + chr(0b1100100)
                + chr(0b1011101 + 0o10),
            )(
                chr(0b1100001 + 0o24)
                + chr(0b1 + 0o163)
                + "\x66"
                + chr(45)
                + chr(0b111000)
            ),
        )(lqCBDe1lOEOd, path=jpvzaVV9Pk2G)
        LUxf4g0U9GW3(lqCBDe1lOEOd, _dIJgk7A3AIg, bot=GiFJytvAvueM)
        VEYmCcpb5WZi = fq44kslIKKlh.AppRunner(lqCBDe1lOEOd)
        await getattr(
            VEYmCcpb5WZi,
            getattr(
                b's~\xe6g\xd1',
                chr(5863 - 5763)
                + chr(0b1100101)
                + chr(99)
                + chr(0b1100100 + 0o13)
                + chr(0b1100100)
                + chr(8469 - 8368),
            )(chr(117) + chr(6076 - 5960) + chr(0b1100110) + chr(982 - 937) + "\x38"),
        )()
        JutrLWyLwTzT = fq44kslIKKlh.TCPSite(
            VEYmCcpb5WZi, host=iWt7SquS5uxf, port=LDZldmpRRXTP
        )
        await getattr(
            JutrLWyLwTzT,
            getattr(
                b'so\xf3`\xd5',
                chr(0b1001111 + 0o25) + chr(101) +
                "\x63" + "\157" + "\x64" + chr(101),
            )(
                chr(12411 - 12294)
                + "\164"
                + chr(0b1100110)
                + chr(0b101101)
                + chr(718 - 662)
            ),
        )()
        getattr(
            zcptFAL0yWNU,
            getattr(
                b'iu\xf4}',
                chr(0b1100100)
                + "\145"
                + chr(0b1010100 + 0o17)
                + chr(0b1101111)
                + chr(100)
                + chr(101),
            )("\165" + chr(116) + "\146" + "\x2d" + chr(56)),
        )(f"URL вебхука: {Di3ZYNq4y1Jk}")
        CRZYKFwfFJRI = diyel4O5bMLs.Event()
        SoAy9XMB2LZJ = diyel4O5bMLs.get_event_loop()
        for aIut2Xl7LjBC in (
            getattr(
                pqP1JQ7q8C2M,
                getattr(
                    b'SR\xd5[\xef\xe4',
                    chr(0b100010 + 0o102)
                    + chr(101)
                    + "\x63"
                    + chr(5424 - 5313)
                    + "\x64"
                    + chr(0b1100101),
                )(
                    chr(0b1110001 + 0o4)
                    + chr(2272 - 2156)
                    + "\x66"
                    + chr(0b11111 + 0o16)
                    + chr(0b111000)
                ),
            ),
            getattr(
                pqP1JQ7q8C2M,
                getattr(
                    b'SR\xd5F\xe4\xe2r',
                    chr(0b1001111 + 0o25)
                    + "\145"
                    + chr(0b1100011)
                    + chr(111)
                    + chr(0b1100100)
                    + chr(101),
                )(
                    chr(0b1010101 + 0o40)
                    + chr(8926 - 8810)
                    + chr(0b1010000 + 0o26)
                    + chr(1408 - 1363)
                    + chr(0b1001 + 0o57)
                ),
            ),
        ):
            getattr(
                SoAy9XMB2LZJ,
                getattr(
                    b'a\x7f\xf6M\xd2\xd9XL9\r\x9d\xee\x190\x0caEb',
                    "\144"
                    + chr(0b1100101)
                    + chr(0b1100011)
                    + chr(0b1101111)
                    + chr(0b1000011 + 0o41)
                    + chr(3785 - 3684),
                )(
                    chr(117)
                    + chr(9249 - 9133)
                    + chr(0b1100110)
                    + chr(0b101101)
                    + chr(56)
                ),
            )(
                aIut2Xl7LjBC,
                getattr(
                    CRZYKFwfFJRI,
                    getattr(
                        b's~\xe6',
                        "\x64" + "\145" + "\143" + "\157" +
                        chr(0b1100100) + chr(101),
                    )(
                        chr(8178 - 8061)
                        + "\x74"
                        + chr(0b1100110)
                        + chr(1530 - 1485)
                        + "\070"
                    ),
                ),
            )
        try:
            await getattr(
                CRZYKFwfFJRI,
                getattr(
                    b'wz\xfbf',
                    chr(0b1100100)
                    + chr(0b101111 + 0o66)
                    + chr(99)
                    + chr(111)
                    + "\144"
                    + chr(0b111101 + 0o50),
                )(chr(117) + chr(0b1110100) + chr(0b1100110) + "\055" + "\x38"),
            )()
        finally:
            g5gb1yodGaJT = [
                NwVNoYZ0lVgA
                for NwVNoYZ0lVgA in diyel4O5bMLs.all_tasks()
                if NwVNoYZ0lVgA is not diyel4O5bMLs.current_task()
            ]
            for NwVNoYZ0lVgA in g5gb1yodGaJT:
                try:
                    getattr(
                        NwVNoYZ0lVgA,
                        getattr(
                            b'cz\xfcq\xc4\xdc',
                            "\x64"
                            + "\x65"
                            + "\143"
                            + chr(0b101001 + 0o106)
                            + "\144"
                            + "\145",
                        )(
                            chr(0b1110101)
                            + chr(12287 - 12171)
                            + chr(7711 - 7609)
                            + chr(45)
                            + chr(0b111000)
                        ),
                    )()
                except Exception as hsEaj3FbHlV3:
                    getattr(
                        zcptFAL0yWNU,
                        getattr(
                            b'ei\xe0}\xd3',
                            "\144"
                            + chr(0b1100101)
                            + chr(0b1100011)
                            + chr(0b1101111)
                            + "\x64"
                            + chr(101),
                        )(
                            chr(0b110 + 0o157)
                            + "\164"
                            + "\146"
                            + chr(0b101101)
                            + "\070"
                        ),
                    )(hsEaj3FbHlV3)
            await getattr(
                diyel4O5bMLs,
                getattr(
                    b'gz\xe6z\xc4\xc2',
                    chr(100)
                    + chr(101)
                    + chr(0b1000001 + 0o42)
                    + chr(9900 - 9789)
                    + "\x64"
                    + chr(9165 - 9064),
                )(
                    chr(11910 - 11793)
                    + chr(0b1110010 + 0o2)
                    + chr(0b1100110)
                    + chr(0b10011 + 0o32)
                    + chr(0b11110 + 0o32)
                ),
            )(
                *g5gb1yodGaJT,
                return_exceptions=int(
                    chr(48) + "\x6f" + chr(0b100000 + 0o21), 8
                ),
            )


if __name__ == getattr(
    b'_D\xffs\xc8\xde`}',
    "\144"
    + chr(0b10111 + 0o116)
    + chr(99)
    + "\157"
    + chr(0b1001001 + 0o33)
    + chr(0b1100101),
)(chr(117) + chr(0b1000111 + 0o55) + chr(7574 - 7472) + chr(45) + chr(2458 - 2402)):
    QK5bLxBOypkF()
    try:
        getattr(
            diyel4O5bMLs,
            getattr(
                b'rn\xfc',
                chr(0b1100100)
                + chr(0b1100101)
                + chr(802 - 703)
                + "\157"
                + chr(0b11100 + 0o110)
                + chr(101),
            )(
                chr(0b1000100 + 0o61)
                + chr(0b1110100)
                + "\146"
                + chr(0b101101)
                + chr(0b101110 + 0o12)
            ),
        )(WeQFJHP3LH_W())
    except Exception as hsEaj3FbHlV3:
        getattr(
            zcptFAL0yWNU,
            getattr(
                b'ei\xe0}\xd3',
                "\144"
                + "\145"
                + "\143"
                + chr(0b1101001 + 0o6)
                + chr(0b1100100)
                + "\x65",
            )(
                chr(0b1110101)
                + chr(6982 - 6866)
                + chr(9174 - 9072)
                + "\055"
                + chr(2704 - 2648)
            ),
        )(f"Ошибка при запуске приложения:\n{hsEaj3FbHlV3}")
