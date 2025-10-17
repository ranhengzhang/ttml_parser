import copy
import re
import weakref
from _weakref import ReferenceType
from typing import TYPE_CHECKING

import numpy

from ttml.ttml_line import TTMLLine
from ttml.ttml_syl import TTMLSyl
from utils import check_leading_space, check_trailing_space, replace_leading_bracket, replace_trailing_bracket

if TYPE_CHECKING:
    from lys.lys import LYS
from lys.lys_syl import LYSSyl


class LYSLine:
    def __init__(self, content: str, parent: 'LYS') -> None:
        self.syl: list[LYSSyl] = list[LYSSyl]()
        self.is_bg: bool = False
        self.is_other: bool = False
        self._parent: ReferenceType[LYS] | None = None

        self.parent = parent
        self.role = int(content[:content.index(']')][1:])
        text = content[content.index(']')+1:]
        index_list: list[int] = [ite.end() for ite in re.finditer(r"\(\d+,\d+\)", text)]
        syl_list: list[str] = list(
            filter(None, map(lambda part: "".join(part), numpy.split([char for char in text], index_list))))
        for syl_text in syl_list:
            word, start, duration = re.match(r"(.*)\((\d+),(\d+)\)", syl_text, re.IGNORECASE).groups()
            if len(word):
                syl: LYSSyl = LYSSyl()
                syl.text = word
                syl.start = int(start)
                syl.duration = int(duration)
                self.syl.append(syl)

    def __str__(self) -> str:
        return f'[{self.role}]{"".join([str(syl) for syl in self.syl])}'

    @property
    def role(self) -> int:
        return (int(self.parent.have_bg) + int(self.is_bg)) * 3 + int(self.parent.have_other) + int(self.is_other)

    @role.setter
    def role(self, val: int) -> None:
        self.is_other = val % 3 == 2
        self.is_bg = val >= 5
        self.parent.have_other |= self.is_other
        self.parent.have_bg |= self.is_bg

    @property
    def parent(self) -> 'LYS':
        return self._parent() if self._parent is not None else None

    @parent.setter
    def parent(self, parent: 'LYS') -> None:
        self._parent: ReferenceType[LYS] = weakref.ref(parent)

    def to_ttml_line(self) -> TTMLLine:
        line: TTMLLine = TTMLLine()

        line.is_bg = self.is_bg
        line.is_other = self.is_other

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

        if line.is_bg:
            line.syl[0].text = replace_leading_bracket(line.syl[0].text)
            line.syl[-1].text = replace_trailing_bracket(line.syl[-1].text)

        return line
