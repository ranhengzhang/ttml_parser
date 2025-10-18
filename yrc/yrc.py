import re

from trans.trans import Trans
from ttml.ttml import TTML
from ttml.ttml_line import TTMLLine
from yrc.yrc_line import YRCLine


class YRC:
    def __init__(self, content: str) -> None:
        self.lines: list[YRCLine] = list[YRCLine]()

        lines: list[str] = list(filter(None, re.split(r"(?:\r?\n)", content.strip())))

        checker = lambda x: re.match(r'^\[\d+,\d+\](\(\d+,\d+,0\).*?)+$', x.strip()) is not None
        while not checker(lines[0]):
            lines.pop(0)

        self.lines.extend([YRCLine(line) for line in lines])

    def __str__(self) -> str:
        return '\n'.join([str(line) for line in self.lines])

    def match_trans(self, trans: Trans) -> None:
        for trans_line in trans.lines:
            for line in self.lines:
                if not line.trans and line.start == trans_line.begin:
                    line.trans = trans_line.text
                    break

    def to_ttml(self) -> TTML:
        lyric_ttml_lines: list[TTMLLine] = [line.to_ttml_line() for line in self.lines]
        ttml_lyric: TTML = TTML()  # 初始化TTML对象

        for line in lyric_ttml_lines:
            if line.is_bg:
                ttml_lyric.lines[-1].bg_line = line
            else:
                ttml_lyric.lines.append(line)

        return ttml_lyric