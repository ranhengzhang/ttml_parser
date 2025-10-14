import re

from ass.ass_syl import ASSSyl
from ttml.ttml_line import TTMLLine
from ttml.ttml_syl import TTMLSyl


class ASSLine:
    def __init__(self) -> None:
        self.comment: bool = bool()
        self.layer: int = int()
        self.start_time: int = int()
        self.end_time: int = int()
        self.duration: int = int()
        self.style: str = str()
        self.actor: str = str()
        self.syl: list[ASSSyl] = list[ASSSyl]()

    def to_ttml_line(self) -> TTMLLine:
        line: TTMLLine = TTMLLine()

        line.begin = self.start_time
        line.end = self.end_time
        line.is_other = "x-duet" in self.actor or "x-anti" in self.actor
        line.is_bg = "x-bg" in self.actor

        syls: list[TTMLSyl] = [ass_syl.to_ttml_syl() for ass_syl in self.syl]
        for syl in syls:
            if (not syl.is_text) and syl.text.strip():
                has_leading_space = re.search(r'^\s+', syl.text)
                has_trailing_space = re.search(r'\s+$', syl.text)

                if has_leading_space:
                    new_syl: TTMLSyl = TTMLSyl()

                    new_syl.begin = syl.begin
                    new_syl.end = syl.begin
                    new_syl.is_text = syl.is_text
                    new_syl.text = has_leading_space.group()
                    line.syl.append(new_syl)

                syl.text = syl.text.strip()
                line.syl.append(syl)

                if has_trailing_space:
                    new_syl: TTMLSyl = TTMLSyl()

                    new_syl.begin = syl.end
                    new_syl.end = syl.end
                    new_syl.is_text = syl.is_text
                    new_syl.text = has_trailing_space.group()
                    line.syl.append(new_syl)
            else:
                line.syl.append(syl)

        if line.is_bg:
            line.syl[0].text = '(' + line.syl[0].text
            line.syl[-1].text = line.syl[-1].text + ')'

        return line
