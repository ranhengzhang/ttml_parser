from audio_time import AudioTime
from ttml.ttml_syl import TTMLSyl
from utils import escape_xml_manual


class TTMLLine:
    index: int = 0

    def __init__(self) -> None:
        self.begin: int = int()
        self.end: int = int()
        self.is_other: bool = False
        self.is_bg: bool = False
        self.ts_line: dict[str, str | "TTMLLine"] = dict[str, str | TTMLLine]()
        self.roma_line: (str | "TTMLLine" | None) = None
        self.syl: list[TTMLSyl] = list[TTMLSyl]()

        self._bg_line: (None | "TTMLLine") = None

    @property
    def bg_line(self) -> "TTMLLine | None":
        return self._bg_line

    @bg_line.setter
    def bg_line(self, line: "TTMLLine") -> None:
        self._bg_line = line
        self.begin = min(self.begin, line.begin)
        self.end = max(self.end, line.end)

    def offset(self, offset: int) -> None:
        self.begin += offset
        self.end += offset
        for syl in self.syl:
            syl.offset(offset)
        if self.bg_line:
            self.bg_line.offset(offset)

    def __str__(self) -> str:
        if not self.is_bg:
            TTMLLine.index += 1
        tag: str = "span" if self.is_bg else "p"
        return (
            f'<{tag} begin="{AudioTime.stringify(self.begin, False, True, True)}" end="{AudioTime.stringify(self.end, False, True, True)}" {'ttm:role="x-bg"' if self.is_bg else f'ttm:agent="{'v2' if self.is_other else 'v1'}" itunes:key="L{TTMLLine.index}"'}>'
            f'{"".join([str(syl) for syl in self.syl])}'
            f'{"".join([f'<span ttm:role="x-translation" xml:lang="{lang}">{escape_xml_manual(line) if type(line) == str else str(line)}</span>' for [lang, line] in self.ts_line.items()]) if len(self.ts_line) else ""}'
            f'{f'<span ttm:role="x-roman">{escape_xml_manual(self.roma_line)}</span>' if self.roma_line else ""}'
            f'{str(self.bg_line) if self.bg_line else ""}'
            f'</{tag}>')
