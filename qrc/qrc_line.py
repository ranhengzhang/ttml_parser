import re

import numpy

from qrc.qrc_syl import QRCSyl
from ttml.ttml_line import TTMLLine
from ttml.ttml_syl import TTMLSyl
from utils import check_trailing_space, check_leading_space


class QRCLine:
    def __init__(self, content: str) -> None:
        self.syl: list[QRCSyl] = list[QRCSyl]()
        self.start: int = int()
        self.duration: int = int()
        self.trans: str | None = None

        line_start, line_duration = re.match(r'(\d+),(\d+)', content[1:content.index(']')]).groups()
        self.start = int(line_start)
        self.duration = int(line_duration)
        text = content[content.index(']')+1:]
        index_list: list[int] = [ite.end() for ite in re.finditer(r"\(\d+,\d+\)", text)]
        syl_list: list[str] = list(
            filter(None, map(lambda part: "".join(part), numpy.split([char for char in text], index_list))))
        for syl_text in syl_list:
            word, start, duration = re.match(r"(.*)\((\d+),(\d+)\)", syl_text, re.IGNORECASE).groups()
            if len(word):
                syl: QRCSyl = QRCSyl()
                syl.text = word
                syl.start = int(start)
                syl.duration = int(duration)
                self.syl.append(syl)

    def __str__(self) -> str:
        return f'[{self.start},{self.duration}]' + "".join([str(syl) for syl in self.syl])

    def to_ttml_line(self) -> TTMLLine:
        line: TTMLLine = TTMLLine()

        line.is_bg = ((self.syl[0].text.startswith('(') or self.syl[0].text.startswith('（')) and
                      (self.syl[-1].text.endswith(')') or self.syl[-1].text.endswith('）')))

        syls: list[TTMLSyl] = [ass_syl.to_ttml_syl() for ass_syl in self.syl]
        for syl in syls:
            has_leading_space: re.Match[str] | None = check_leading_space.search(syl.text)
            if has_leading_space:
                new_syl: TTMLSyl = TTMLSyl()

                new_syl.begin = syl.begin
                new_syl.end = syl.end
                new_syl.is_text = True
                new_syl.text = has_leading_space.group()
                line.syl.append(new_syl)

            syl.text = syl.text[len(has_leading_space.group()) if has_leading_space else 0:]
            line.syl.append(syl)

            has_trailing_space: re.Match[str] | None = check_trailing_space.search(syl.text)
            if has_trailing_space:
                new_syl: TTMLSyl = TTMLSyl()

                new_syl.begin = syl.end
                new_syl.end = syl.end
                new_syl.is_text = True
                new_syl.text = has_trailing_space.group()
                line.syl.append(new_syl)

        line.begin = self.syl[0].start
        line.end = self.syl[-1].start + self.syl[-1].duration
        if self.trans:
            line.ts_line['zh-CN'] = self.trans

        if line.is_bg:
            line.syl[0].text = replace_leading_bracket(line.syl[0].text)
            line.syl[-1].text = replace_trailing_bracket(line.syl[-1].text)

        return line