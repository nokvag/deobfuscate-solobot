

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
        decode(
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
        decode(chr(117) + chr(0b111101 + 0o67) + chr(0b1010100 + 0o22) + "\x2d" + chr(56))
    ),
)
m0HGG4fFzMqQ, LUxf4g0U9GW3 = (
    decode(
                        chr(0b1110101)
                        + chr(0b1000 + 0o154)
                        + chr(0b1100110)
                        + chr(0b101101)
                        + "\070"
                    ),
                    decode(
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
                decode(chr(0b1110101) + chr(116) + chr(102) + chr(0b101101) + chr(0b111000)),
            ),
            decode(chr(4128 - 4011) + "\164" + chr(0b1100110) + chr(0b101101) + "\070"),
        ),
        decode(
            chr(0b100001 + 0o124)
            + chr(116)
            + "\x66"
            + chr(0b101101)
            + chr(0b101000 + 0o20)
        ),
    ),
    decode(
                        chr(9327 - 9210)
                        + chr(0b1001000 + 0o54)
                        + "\146"
                        + chr(0b11 + 0o52)
                        + chr(56)
                    ),
                    decode(
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
                decode(
                    chr(0b1110101)
                    + chr(0b1110100)
                    + "\146"
                    + "\055"
                    + chr(0b10101 + 0o43)
                ),
            ),
            decode(
                chr(117)
                + chr(0b1001101 + 0o47)
                + chr(0b1100110)
                + chr(0b11101 + 0o20)
                + "\x38"
            ),
        ),
        decode(chr(0b11111 + 0o126) + "\164" + "\146" + chr(1019 - 974) + "\x38"),
    ),
)
(fq44kslIKKlh,) = (
    decode(chr(12815 - 12698) + chr(116) + chr(0b1000001 + 0o45) + chr(45) + "\x38"),
            decode("\x75" + chr(116) + chr(102) + chr(0b101101) + "\x38"),
            globals=None,
            locals=None,
            level=int("\060" + "\157" + chr(0b110000), 8),
        ),
        decode(chr(0b1110101) + "\x74" + chr(102) + chr(45) + chr(1633 - 1577)),
    ),
)
(CixZZL1caaDz,) = (
    decode(
                chr(0b101100 + 0o111)
                + "\164"
                + chr(0b1001011 + 0o33)
                + "\x2d"
                + chr(1357 - 1301)
            ),
            decode(
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
        decode(
            chr(0b1110101)
            + chr(6758 - 6642)
            + chr(2520 - 2418)
            + "\x2d"
            + chr(0b10100 + 0o44)
        ),
    ),
)
GiFJytvAvueM, _dIJgk7A3AIg = (
    decode(
                chr(117)
                + chr(4257 - 4141)
                + chr(102)
                + chr(0b101101)
                + chr(0b10001 + 0o47)
            ),
            decode(
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
        decode("\x75" + chr(0b1110100) + chr(0b110111 + 0o57) + "\x2d" + chr(1376 - 1320)),
    ),
    decode(
                "\165"
                + chr(0b11 + 0o161)
                + chr(0b100011 + 0o103)
                + "\x2d"
                + chr(733 - 677)
            ),
            decode(
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
        decode(
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
    decode("\x75" + "\164" + "\146" + chr(45) + chr(0b110100 + 0o4)),
            decode(chr(117) + chr(0b1110100) + chr(102) + "\x2d" + "\x38"),
            globals=None,
            locals=None,
            level=int(chr(48) + chr(111) + "\x30", 8),
        ),
        decode(
            chr(3351 - 3234)
            + chr(0b11101 + 0o127)
            + chr(102)
            + chr(0b10011 + 0o32)
            + chr(56)
        ),
    ),
    decode(
                chr(117)
                + chr(0b1110100)
                + chr(0b1100110)
                + chr(45)
                + chr(0b101111 + 0o11)
            ),
            decode(chr(0b10101 + 0o140) + chr(116) + chr(102) + chr(45) + chr(0b111000)),
            globals=None,
            locals=None,
            level=int(chr(0b110000) + "\157" + chr(48), 8),
        ),
        decode(chr(9927 - 9810) + "\164" + "\146" + "\055" + "\x38"),
    ),
    decode("\165" + chr(0b1101100 + 0o10) + "\146" + chr(0b101101) + chr(56)),
            decode(
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
        decode("\165" + "\164" + chr(0b1000110 + 0o40) + chr(45) + chr(56)),
    ),
    decode(
                chr(8267 - 8150)
                + "\164"
                + "\x66"
                + chr(0b10100 + 0o31)
                + chr(2340 - 2284)
            ),
            decode(chr(0b1101010 + 0o13) + "\x74" + "\x66" + chr(45) + chr(0b0 + 0o70)),
            globals=None,
            locals=None,
            level=int(chr(0b110000) + chr(6244 - 6133) + "\060", 8),
        ),
        decode("\165" + "\164" + chr(5856 - 5754) + chr(1229 - 1184) + chr(602 - 546)),
    ),
    decode(
                chr(117)
                + chr(0b1110100)
                + chr(102)
                + chr(0b11110 + 0o17)
                + chr(0b111000)
            ),
            decode(
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
        decode(
            "\165"
            + chr(116)
            + chr(0b1100 + 0o132)
            + chr(1481 - 1436)
            + chr(0b100010 + 0o26)
        ),
    ),
    decode(
                chr(3039 - 2922)
                + chr(0b1110100)
                + "\x66"
                + chr(45)
                + chr(0b11000 + 0o40)
            ),
            decode(chr(117) + chr(0b1110100) + chr(0b1100110) + chr(45) + "\x38"),
            globals=None,
            locals=None,
            level=int(chr(48) + "\x6f" + "\x30", 8),
        ),
        decode(chr(0b1000000 + 0o65) + "\164" + "\146" + chr(0b101101) + chr(56)),
    ),
    decode("\165" + chr(0b1110100) + "\146" + "\055" + "\x38"),
            decode(chr(0b1011111 + 0o26) + "\164" + "\146" + "\x2d" + chr(3013 - 2957)),
            globals=None,
            locals=None,
            level=int(chr(0b100101 + 0o13) + "\157" + chr(48), 8),
        ),
        decode(
            chr(0b110100 + 0o101)
            + "\164"
            + chr(0b111001 + 0o55)
            + chr(404 - 359)
            + "\x38"
        ),
    ),
    decode(
                chr(8347 - 8230)
                + chr(0b1110100)
                + chr(0b1100110)
                + chr(0b101101)
                + "\070"
            ),
            decode("\165" + chr(0b1110100) + chr(0b1100110) + "\x2d" + chr(1544 - 1488)),
            globals=None,
            locals=None,
            level=int(chr(878 - 830) + chr(0b1101111) + "\x30", 8),
        ),
        decode(
            chr(5781 - 5664)
            + chr(0b11100 + 0o130)
            + "\146"
            + chr(401 - 356)
            + chr(0b111000)
        ),
    ),
    decode("\x75" + chr(116) + chr(0b1100110) + chr(0b101101) + chr(0b1 + 0o67)),
            decode(chr(117) + chr(0b100 + 0o160) + chr(0b1100110) + chr(0b101101) + "\x38"),
            globals=None,
            locals=None,
            level=int("\060" + chr(7135 - 7024) + "\060", 8),
        ),
        decode(chr(2096 - 1979) + "\x74" + chr(102) + chr(45) + chr(410 - 354)),
    ),
    decode(chr(117) + chr(1937 - 1821) + "\146" + "\055" + "\070"),
            decode(
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
        decode(
            chr(0b1101100 + 0o11)
            + chr(0b100000 + 0o124)
            + chr(6630 - 6528)
            + "\055"
            + "\070"
        ),
    ),
    decode(
                chr(0b110000 + 0o105)
                + chr(0b100010 + 0o122)
                + "\146"
                + chr(45)
                + "\070"
            ),
            decode(
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
        decode("\165" + "\164" + chr(102) + chr(242 - 197) + chr(0b111000)),
    ),
    decode(chr(117) + "\x74" + chr(0b1 + 0o145) + chr(45) + chr(0b110010 + 0o6)),
            decode(chr(1558 - 1441) + chr(0b100110 + 0o116) + "\146" + "\055" + "\070"),
            globals=None,
            locals=None,
            level=int(
                chr(521 - 473) + chr(0b10010 + 0o135) + chr(0b11101 + 0o23), 8
            ),
        ),
        decode(chr(0b1110101) + "\x74" + "\x66" + chr(45) + "\070"),
    ),
    decode(chr(0b1000011 + 0o62) + chr(116) + "\x66" + chr(0b101101) + chr(56)),
            decode("\x75" + chr(0b1110100) + "\146" + "\055" + "\x38"),
            globals=None,
            locals=None,
            level=int(chr(48) + chr(0b1010 + 0o145) + "\x30", 8),
        ),
        decode(chr(0b1010111 + 0o36) + "\x74" + chr(0b1100110) + chr(45) + chr(56)),
    ),
)
(mhwkmweqvIZS,) = (
    decode(
                chr(0b1110101)
                + chr(11503 - 11387)
                + "\146"
                + chr(0b11111 + 0o16)
                + "\x38"
            ),
            decode(chr(117) + chr(0b1110100) + chr(0b1111 + 0o127) + "\055" + chr(56)),
            globals=None,
            locals=None,
            level=int(
                chr(0b110000) + chr(4343 - 4232) + chr(1231 - 1183), 8),
        ),
        decode("\x75" + "\x74" + chr(102) + "\055" + "\x38"),
    ),
)
(vlARRACoCOHo,) = (
    decode(chr(117) + chr(116) + "\146" + "\055" + "\x38"),
            decode(
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
        decode(
            chr(13362 - 13245)
            + chr(0b1110100)
            + chr(0b1000011 + 0o43)
            + chr(45)
            + chr(0b0 + 0o70)
        ),
    ),
)
hQCziMO4TGCZ, CjTWspeGMliC = (
    decode("\x75" + chr(0b1110100) + chr(1384 - 1282) + chr(45) + "\070"),
                    decode("\165" + chr(0b1110100) + "\146" + "\055" + "\070"),
                    globals=None,
                    locals=None,
                    level=int(
                        chr(0b110000) + chr(691 - 580) + chr(128 - 80), 8
                    ),
                ),
                decode(
                    chr(0b101100 + 0o111)
                    + "\164"
                    + "\x66"
                    + chr(129 - 84)
                    + chr(0b100111 + 0o21)
                ),
            ),
            decode("\165" + chr(0b101011 + 0o111) + "\146" + "\055" + "\x38"),
        ),
        decode(chr(0b10101 + 0o140) + chr(0b1110100) + "\x66" + chr(263 - 218) + "\070"),
    ),
    decode("\x75" + "\x74" + chr(0b1001101 + 0o31) + chr(45) + chr(56)),
                    decode(
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
                decode(
                    chr(0b11010 + 0o133)
                    + chr(0b1110100)
                    + chr(102)
                    + chr(769 - 724)
                    + chr(1367 - 1311)
                ),
            ),
            decode(
                chr(7283 - 7166)
                + chr(10354 - 10238)
                + chr(0b1100110)
                + chr(0b101101)
                + "\070"
            ),
        ),
        decode(
            "\x75"
            + chr(0b1110100)
            + chr(8910 - 8808)
            + chr(1668 - 1623)
            + chr(1317 - 1261)
        ),
    ),
)
(fLL8E8IGPK8S,) = (
    decode(
                        chr(117)
                        + chr(13255 - 13139)
                        + chr(102)
                        + "\055"
                        + chr(0b10010 + 0o46)
                    ),
                    decode(
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
                decode(
                    chr(0b1110101)
                    + chr(0b1011111 + 0o25)
                    + chr(0b1011000 + 0o16)
                    + chr(45)
                    + chr(0b111000)
                ),
            ),
            decode(chr(0b1010000 + 0o45) + chr(1749 - 1633) + "\x66" + chr(45) + chr(56)),
        ),
        decode(chr(0b111011 + 0o72) + "\x74" + chr(8302 - 8200) + "\055" + "\070"),
    ),
)
(URH6xO9_OvAX,) = (
    decode(chr(0b11000 + 0o135) + "\x74" + "\x66" + chr(45) + "\x38"),
                    decode(
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
                decode(chr(0b1110101) + chr(116) + "\146" + chr(45) + chr(56)),
            ),
            decode(
                chr(117)
                + chr(2109 - 1993)
                + chr(0b1000001 + 0o45)
                + "\x2d"
                + chr(991 - 935)
            ),
        ),
        decode(
            "\x75"
            + chr(0b100111 + 0o115)
            + chr(102)
            + chr(0b101010 + 0o3)
            + chr(0b111000)
        ),
    ),
)
(r1KJRGSk6S_M,) = (
    decode(
                        chr(10254 - 10137)
                        + chr(0b1010011 + 0o41)
                        + chr(0b111100 + 0o52)
                        + chr(1261 - 1216)
                        + chr(56)
                    ),
                    decode("\x75" + chr(116) + "\146" + "\055" + chr(56)),
                    globals=None,
                    locals=None,
                    level=int(
                        chr(0b11011 + 0o25) + chr(0b1101111 + 0o0) + chr(48), 8
                    ),
                ),
                decode(
                    chr(1156 - 1039)
                    + chr(0b1110100)
                    + chr(7607 - 7505)
                    + chr(1200 - 1155)
                    + chr(2530 - 2474)
                ),
            ),
            decode(
                "\x75"
                + chr(0b1110100)
                + chr(0b111000 + 0o56)
                + chr(0b101100 + 0o1)
                + chr(56)
            ),
        ),
        decode(chr(8509 - 8392) + chr(146 - 30) + chr(0b1100110) + "\055" + chr(515 - 459)),
    ),
)
(eVzbKhmdRT7G,) = (
    decode("\x75" + chr(0b1110100) + "\146" + chr(1875 - 1830) + "\070"),
                    decode(chr(0b1110101) + chr(116) + "\146" + "\055" + chr(0b111000)),
                    globals=None,
                    locals=None,
                    level=int(
                        "\x30" + chr(9160 - 9049) + chr(0b1100 + 0o44), 8
                    ),
                ),
                decode(
                    chr(117)
                    + chr(0b1110100)
                    + "\146"
                    + chr(0b101101)
                    + chr(0b11110 + 0o32)
                ),
            ),
            decode("\x75" + chr(0b1110100) + "\146" + "\x2d" + chr(0b10 + 0o66)),
        ),
        decode("\165" + chr(5171 - 5055) + "\x66" + chr(0b11111 + 0o16) + chr(0b11 + 0o65)),
    ),
)
FMmGOBZBev8A, gLLuUhpdiNZQ = (
    decode(
                        chr(0b111110 + 0o67)
                        + chr(0b1000100 + 0o60)
                        + "\146"
                        + chr(1446 - 1401)
                        + chr(0b1100 + 0o54)
                    ),
                    decode(
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
                decode(
                    chr(117)
                    + chr(0b1110100)
                    + chr(9329 - 9227)
                    + "\x2d"
                    + chr(1999 - 1943)
                ),
            ),
            decode(chr(3971 - 3854) + chr(116) + chr(102) + chr(0b10101 + 0o30) + chr(56)),
        ),
        decode(
            chr(0b1110001 + 0o4)
            + chr(116)
            + chr(0b100011 + 0o103)
            + "\055"
            + chr(0b110100 + 0o4)
        ),
    ),
    decode(
                        "\x75"
                        + "\x74"
                        + chr(0b1001100 + 0o32)
                        + chr(161 - 116)
                        + chr(56)
                    ),
                    decode(
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
                decode("\165" + chr(0b111011 + 0o71) + "\146" + "\x2d" + chr(56)),
            ),
            decode(chr(7075 - 6958) + chr(116) + "\x66" + "\055" + "\x38"),
        ),
        decode(
            chr(0b1011100 + 0o31)
            + chr(13210 - 13094)
            + chr(102)
            + chr(0b10101 + 0o30)
            + chr(1227 - 1171)
        ),
    ),
)
(FHt_8BTqROto,) = (
    decode("\x75" + chr(0b1101 + 0o147) + "\146" + "\055" + chr(0b111000)),
                    decode(chr(0b1110101) + "\x74" + chr(0b1100110) + "\055" + "\x38"),
                    globals=None,
                    locals=None,
                    level=int(
                        chr(0b100000 + 0o20) +
                        chr(0b1101111) + chr(0b11 + 0o55), 8
                    ),
                ),
                decode(
                    chr(0b1110101)
                    + "\x74"
                    + chr(0b101 + 0o141)
                    + chr(0b101011 + 0o2)
                    + chr(56)
                ),
            ),
            decode(chr(331 - 214) + chr(116) + "\x66" + chr(733 - 688) + chr(56)),
        ),
        decode(
            chr(0b100100 + 0o121)
            + chr(0b1110100)
            + chr(102)
            + "\x2d"
            + chr(0b11101 + 0o33)
        ),
    ),
)
(zcptFAL0yWNU,) = (
    decode("\165" + "\164" + "\x66" + "\x2d" + "\x38"),
            decode(chr(0b1110101) + chr(116) + chr(102) + chr(45) + chr(0b111000)),
            globals=None,
            locals=None,
            level=int(chr(48) + chr(9700 - 9589) + chr(526 - 478), 8),
        ),
        decode(
            chr(117)
            + chr(0b1100110 + 0o16)
            + "\146"
            + chr(1736 - 1691)
            + chr(0b1001 + 0o57)
        ),
    ),
)
(I9T087Aiov_5,) = (
    decode("\165" + "\x74" + chr(102) + "\x2d" + chr(56)),
            decode(
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
        decode(chr(9261 - 9144) + chr(116) + "\146" + "\055" + "\070"),
    ),
)
(KTcuB6QKV8WZ,) = (
    __import__(
        decode(chr(117) + "\x74" + "\x66" + chr(0b11101 + 0o20) + "\x38")
    ),
)
(gtWK63WYa3JX,) = (
    __import__(
        decode(chr(117) + chr(116) + chr(0b1001110 + 0o30) + chr(0b101101) + "\x38")
    ),
)


def QK5bLxBOypkF():
    NufvPSR1AQNx = KTcuB6QKV8WZ.path.abspath(
        decode(chr(7614 - 7497) + "\164" + chr(102) + "\055" + chr(0b111000))
    )
    lsHnbTESTPag = gtWK63WYa3JX.executable
    u4Kgw2xftrng = [
        decode(chr(117) + chr(116) + "\x66" + "\055" + "\070"),
        decode(
            chr(3859 - 3742)
            + chr(116)
            + chr(5971 - 5869)
            + chr(0b101101)
            + chr(0b1100 + 0o54)
        ),
        KTcuB6QKV8WZ.path.expanduser(
            decode(
                chr(0b1000 + 0o155)
                + "\164"
                + chr(8423 - 8321)
                + chr(0b101010 + 0o3)
                + chr(0b101110 + 0o12)
            )
        ),
    ]
    for LjLi2w1n0i3h in u4Kgw2xftrng:
        if decode(chr(117) + "\x74" + "\x66" + chr(45) + "\070"),
        )(LjLi2w1n0i3h) and decode(chr(2837 - 2720) + "\x74" + chr(102) + "\x2d" + chr(2226 - 2170)),
        )(
            LjLi2w1n0i3h,
            decode(
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
                decode(
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
            decode(chr(0b1110101) + chr(9157 - 9041) + "\146" + chr(543 - 498) + "\x38")
        )
        return
    if decode("\165" + "\164" + "\146" + chr(0b101101) + chr(0b100011 + 0o25)),
    )(DK9LsyO02L_J):
        return
    try:
        with open(
            DK9LsyO02L_J,
            decode("\x75" + "\x74" + chr(0b1100110) + chr(0b101101) + "\070"),
        ) as HohFPgdHHRgg:
            decode(chr(117) + "\164" + chr(102) + chr(45) + "\x38"),
            )(f"""#!/bin/bash\n'{lsHnbTESTPag}' '{NufvPSR1AQNx}' "$@"\n""")
        decode(chr(9212 - 9095) + "\164" + chr(8653 - 8551) + chr(0b101101) + "\x38"),
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
        await decode(chr(117) + chr(116) + chr(0b1100110) + "\x2d" + chr(0b1000 + 0o60)),
        )(a5c3UP8TmpNy)


async def M6flxKL4gRoX(lqCBDe1lOEOd):
    await decode(chr(117) + "\164" + "\x66" + chr(45) + chr(934 - 878)),
    )(Di3ZYNq4y1Jk)
    await mhwkmweqvIZS()
    decode(chr(6667 - 6550) + chr(116) + chr(0b1100110) + "\055" + "\x38"),
    )(fLL8E8IGPK8S(GiFJytvAvueM))
    if a5c3UP8TmpNy > int(chr(0b110000) + "\x6f" + chr(0b10010 + 0o36), 8):
        decode("\165" + chr(0b1 + 0o163) + chr(3169 - 3067) + chr(0b101101) + chr(56)),
        )(D6P0eecBAFVv())
    if QnsUyBGFs1xi > int("\060" + "\x6f" + chr(48), 8):
        decode(chr(117) + chr(5219 - 5103) + "\x66" + "\x2d" + chr(56)),
        )(I9T087Aiov_5())


async def KMS7j9IC8wK5(lqCBDe1lOEOd):
    await decode(chr(11154 - 11037) + "\x74" + "\146" + "\055" + chr(0b11101 + 0o33)),
    )()
    for NwVNoYZ0lVgA in decode(chr(117) + "\164" + chr(0b1100110) + chr(745 - 700) + chr(2611 - 2555)),
    )():
        decode("\165" + "\164" + "\x66" + "\055" + "\070"),
        )()
    try:
        await decode("\x75" + "\164" + chr(0b1100110) + chr(0b11110 + 0o17) + "\x38"),
        )(
            *decode(
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
        decode(
                "\165"
                + chr(116)
                + chr(0b110001 + 0o65)
                + chr(0b101101)
                + chr(0b11000 + 0o40)
            ),
        )(f"Ошибка при завершении работы: {hsEaj3FbHlV3}")


async def o_Zg3SYZ2U_F(JutrLWyLwTzT):
    decode(
            "\x75"
            + chr(0b1110100)
            + chr(102)
            + chr(0b100110 + 0o7)
            + chr(0b100001 + 0o27)
        ),
    )(
        decode(chr(0b11011 + 0o132) + chr(0b1110100) + chr(102) + "\055" + chr(0b111000))
    )
    await decode(chr(0b11001 + 0o134) + chr(116) + "\x66" + chr(45) + "\070"),
    )()
    decode("\165" + chr(0b1010101 + 0o37) + "\x66" + chr(785 - 740) + chr(56)),
    )(
        decode("\165" + chr(0b1001110 + 0o46) + chr(5124 - 5022) + "\055" + chr(0b111000))
    )


async def WeQFJHP3LH_W():
    _SvfhKl8rD1_ = await r1KJRGSk6S_M()
    if not _SvfhKl8rD1_:
        decode("\165" + chr(0b1100 + 0o150) + "\146" + chr(45) + chr(0b101000 + 0o20)),
        )(
            decode("\165" + chr(0b1110100) + chr(139 - 37) + "\x2d" + chr(1394 - 1338))
        )
        return
    JezwpIWfYHOX = decode("\x75" + chr(0b101110 + 0o106) + chr(102) + "\055" + chr(0b1 + 0o67))
    if FMmGOBZBev8A != JezwpIWfYHOX:
        decode("\165" + chr(10694 - 10578) + chr(0b1100110) + "\x2d" + "\x38"),
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
    decode(
            chr(13516 - 13399)
            + chr(0b1010001 + 0o43)
            + chr(0b1000110 + 0o40)
            + chr(851 - 806)
            + "\x38"
        ),
    )(vlARRACoCOHo)
    if VWiaMPSC0NzU:
        decode(
                chr(11169 - 11052)
                + chr(0b1110100)
                + chr(102)
                + "\x2d"
                + chr(0b110110 + 0o2)
            ),
        )(
            decode(chr(0b1110101) + chr(0b101001 + 0o113) + "\x66" + "\055" + chr(0b111000))
        )
        await decode("\165" + "\x74" + chr(0b1100110) + chr(0b100 + 0o51) + "\x38"),
        )()
        await mhwkmweqvIZS()
        fPSFiLwtmvLO = [diyel4O5bMLs.create_task(fLL8E8IGPK8S(GiFJytvAvueM))]
        if QnsUyBGFs1xi > int(
            chr(395 - 347) + chr(111) + chr(0b111 + 0o51), 8
        ):
            decode("\x75" + chr(0b1110100) + chr(0b1100110) + "\x2d" + "\x38"),
            )(
                decode(
                        "\165"
                        + chr(0b1110 + 0o146)
                        + chr(7489 - 7387)
                        + "\x2d"
                        + chr(56)
                    ),
                )(I9T087Aiov_5())
            )
        if a5c3UP8TmpNy > int(chr(0b110000) + "\157" + "\x30", 8):
            decode(
                    chr(0b1011100 + 0o31)
                    + chr(0b110000 + 0o104)
                    + chr(0b110010 + 0o64)
                    + chr(1450 - 1405)
                    + "\x38"
                ),
            )(
                decode("\165" + chr(0b1110100) + "\x66" + chr(45) + chr(56)),
                )(D6P0eecBAFVv())
            )
        await decode("\x75" + "\164" + chr(102) + "\055" + chr(0b111000)),
        )(GiFJytvAvueM)
        decode("\x75" + "\x74" + "\146" + chr(0b11 + 0o52) + chr(56)),
        )(
            decode(
                chr(117)
                + chr(0b1010000 + 0o44)
                + chr(0b1100110)
                + "\x2d"
                + chr(0b10011 + 0o45)
            )
        )
        for NwVNoYZ0lVgA in fPSFiLwtmvLO:
            decode(
                    chr(9385 - 9268)
                    + chr(116)
                    + chr(102)
                    + chr(1318 - 1273)
                    + chr(2695 - 2639)
                ),
            )()
        await decode("\165" + "\164" + chr(2272 - 2170) + chr(45) + chr(0b1110 + 0o52)),
        )(
            *fPSFiLwtmvLO,
            return_exceptions=int(
                "\x30" + "\157" + chr(0b110000 + 0o1), 8),
        )
    else:
        decode(chr(0b1100101 + 0o20) + "\x74" + "\x66" + chr(0b101101) + chr(0b111000)),
        )(
            decode(chr(0b1110101) + chr(0b1100110 + 0o16) + "\x66" + "\x2d" + "\070")
        )
        lqCBDe1lOEOd = fq44kslIKKlh.Application()
        decode("\x75" + chr(0b1000 + 0o154) + "\146" + chr(0b100011 + 0o12) + "\x38"),
        )(M6flxKL4gRoX)
        decode("\165" + chr(10887 - 10771) + "\146" + chr(45) + chr(0b110101 + 0o3)),
        )(KMS7j9IC8wK5)
        if sDa0ySHsUBbE:
            decode(
                    "\x75"
                    + chr(0b11011 + 0o131)
                    + chr(0b1100110)
                    + chr(1472 - 1427)
                    + chr(0b101010 + 0o16)
                ),
            )(
                decode("\165" + "\x74" + chr(6116 - 6014) + "\x2d" + chr(0b111000)),
                gLLuUhpdiNZQ,
            )
        if U3RbnQ1KQ4Bf:
            decode(
                    chr(0b1110101)
                    + chr(116)
                    + chr(8551 - 8449)
                    + chr(0b101101)
                    + chr(622 - 566)
                ),
            )(
                decode(
                    chr(6417 - 6300)
                    + chr(0b1110100)
                    + chr(0b1100011 + 0o3)
                    + chr(1664 - 1619)
                    + chr(56)
                ),
                FHt_8BTqROto,
            )
        if osp164bN12E4:
            decode(
                    chr(2384 - 2267)
                    + chr(116)
                    + chr(102)
                    + chr(0b101101)
                    + chr(0b11101 + 0o33)
                ),
            )(
                decode("\x75" + "\x74" + "\146" + chr(761 - 716) + chr(0b111000)),
                URH6xO9_OvAX,
            )
        if fqoAVnVIRd_I:
            decode(chr(0b10101 + 0o140) + "\164" + "\146" + chr(0b101101) + "\x38"),
            )(
                decode(
                    chr(253 - 136)
                    + chr(13396 - 13280)
                    + chr(0b10111 + 0o117)
                    + chr(0b101101)
                    + chr(0b111000)
                ),
                eVzbKhmdRT7G,
            )
        if DfumMdwt5gQ6:
            decode("\165" + chr(10604 - 10488) + chr(0b1100110) + "\x2d" + chr(56)),
            )(f"{K585qaYUbA_y}{{email}}", CjTWspeGMliC)
        decode(chr(117) + chr(0b1100101 + 0o17) + "\x66" + chr(0b101101) + chr(56)),
        )(f"{K585qaYUbA_y}{{email}}/{{tg_id}}", hQCziMO4TGCZ)
        getattr(
            m0HGG4fFzMqQ(dispatcher=_dIJgk7A3AIg, bot=GiFJytvAvueM),
            decode(
                chr(0b1100001 + 0o24)
                + chr(0b1 + 0o163)
                + "\x66"
                + chr(45)
                + chr(0b111000)
            ),
        )(lqCBDe1lOEOd, path=jpvzaVV9Pk2G)
        LUxf4g0U9GW3(lqCBDe1lOEOd, _dIJgk7A3AIg, bot=GiFJytvAvueM)
        VEYmCcpb5WZi = fq44kslIKKlh.AppRunner(lqCBDe1lOEOd)
        await decode(chr(117) + chr(6076 - 5960) + chr(0b1100110) + chr(982 - 937) + "\x38"),
        )()
        JutrLWyLwTzT = fq44kslIKKlh.TCPSite(
            VEYmCcpb5WZi, host=iWt7SquS5uxf, port=LDZldmpRRXTP
        )
        await decode(
                chr(12411 - 12294)
                + "\164"
                + chr(0b1100110)
                + chr(0b101101)
                + chr(718 - 662)
            ),
        )()
        decode("\165" + chr(116) + "\146" + "\x2d" + chr(56)),
        )(f"URL вебхука: {Di3ZYNq4y1Jk}")
        CRZYKFwfFJRI = diyel4O5bMLs.Event()
        SoAy9XMB2LZJ = diyel4O5bMLs.get_event_loop()
        for aIut2Xl7LjBC in (
            decode(
                    chr(0b1110001 + 0o4)
                    + chr(2272 - 2156)
                    + "\x66"
                    + chr(0b11111 + 0o16)
                    + chr(0b111000)
                ),
            ),
            decode(
                    chr(0b1010101 + 0o40)
                    + chr(8926 - 8810)
                    + chr(0b1010000 + 0o26)
                    + chr(1408 - 1363)
                    + chr(0b1001 + 0o57)
                ),
            ),
        ):
            decode(
                    chr(117)
                    + chr(9249 - 9133)
                    + chr(0b1100110)
                    + chr(0b101101)
                    + chr(56)
                ),
            )(
                aIut2Xl7LjBC,
                decode(
                        chr(8178 - 8061)
                        + "\x74"
                        + chr(0b1100110)
                        + chr(1530 - 1485)
                        + "\070"
                    ),
                ),
            )
        try:
            await decode(chr(117) + chr(0b1110100) + chr(0b1100110) + "\055" + "\x38"),
            )()
        finally:
            g5gb1yodGaJT = [
                NwVNoYZ0lVgA
                for NwVNoYZ0lVgA in diyel4O5bMLs.all_tasks()
                if NwVNoYZ0lVgA is not diyel4O5bMLs.current_task()
            ]
            for NwVNoYZ0lVgA in g5gb1yodGaJT:
                try:
                    decode(
                            chr(0b1110101)
                            + chr(12287 - 12171)
                            + chr(7711 - 7609)
                            + chr(45)
                            + chr(0b111000)
                        ),
                    )()
                except Exception as hsEaj3FbHlV3:
                    decode(
                            chr(0b110 + 0o157)
                            + "\164"
                            + "\146"
                            + chr(0b101101)
                            + "\070"
                        ),
                    )(hsEaj3FbHlV3)
            await decode(
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


if __name__ == decode(chr(117) + chr(0b1000111 + 0o55) + chr(7574 - 7472) + chr(45) + chr(2458 - 2402)):
    QK5bLxBOypkF()
    try:
        decode(
                chr(0b1000100 + 0o61)
                + chr(0b1110100)
                + "\146"
                + chr(0b101101)
                + chr(0b101110 + 0o12)
            ),
        )(WeQFJHP3LH_W())
    except Exception as hsEaj3FbHlV3:
        decode(
                chr(0b1110101)
                + chr(6982 - 6866)
                + chr(9174 - 9072)
                + "\055"
                + chr(2704 - 2648)
            ),
        )(f"Ошибка при запуске приложения:\n{hsEaj3FbHlV3}")
