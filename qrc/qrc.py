import re

from qrc.qrc_line import QRCLine
from trans.trans import Trans
from ttml.ttml import TTML
from ttml.ttml_line import TTMLLine


class QRC:
    def __init__(self, content: str) -> None:
        self.metas: list[tuple[str, str]] = list[tuple[str, str]]()
        self.lines: list[QRCLine] = list[QRCLine]()

        lines: list[str] = list(filter(None, re.split(r"(?:\r?\n)", content.strip())))

        checker = lambda x: re.match(r'^\[.+?\:.+?\]$', x.strip()) is not None
        if any(checker(line) for line in lines):
            while not checker(lines[0]):
                lines.pop(0)

            while checker(lines[0]):
                matches: re.Match[str] = re.match(r'\[(.+?)\:\s?(.+?)\]', lines.pop(0))
                self.metas.append((matches.group(1).strip(),matches.group(2).strip()))

        self.lines.extend([QRCLine(line) for line in lines])

    def __str__(self) -> str:
        return '\n'.join([f'[{meta[0]}: {meta[1]}]' for meta in self.metas]) + "\n\n" + '\n'.join([str(line) for line in self.lines])

    def match_trans(self, trans: Trans) -> None:
        self.metas.extend(trans.metas)
        for trans_line in trans.lines:
            for line in self.lines:
                if not line.trans and line.start == trans_line.begin:
                    line.trans = trans_line.text
                    break

    def to_ttml(self) -> TTML:
        lyric_ttml_lines: list[TTMLLine] = [line.to_ttml_line() for line in self.lines]
        ttml_lyric: TTML = TTML()  # 初始化TTML对象

        offset:int = int()
        if any(meta[0] == "offset" for meta in self.metas):
            offset = int(next(meta[1] for meta in self.metas if meta[0] == "offset"))

        for meta in self.metas:
            if meta[0] != "offset":
                ttml_lyric.metas[meta[0]].add(meta[1])

        for line in lyric_ttml_lines:
            if line.is_bg:
                ttml_lyric.lines[-1].bg_line = line
            else:
                ttml_lyric.lines.append(line)

        ttml_lyric.offset(offset)

        return ttml_lyric