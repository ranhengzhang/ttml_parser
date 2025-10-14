import copy
from collections import defaultdict

from audio_time import AudioTime
from ttml.ttml_line import TTMLLine
from utils import escape_xml_manual


class TTML:
    def __init__(self) -> None:
        self.metas: defaultdict[str, set[str]] = defaultdict(set)
        self.have_other: bool = False
        self.parts: list[tuple[str, int]] = list[tuple[str, int]]()
        self.lines: list[TTMLLine] = list[TTMLLine]()

    def offset(self, offset: int) -> None:
        for line in self.lines:
            line.offset(offset)

    @property
    def head(self) -> str:
        return (f'<head>'
                f'<metadata>'
                f'<ttm:agent type="person" xml:id="v1" />'
                f'{'''<ttm:agent type="other" xml:id="v2"/>''' if self.have_other else ""}'
                f'{"".join(["".join([f'<amll:meta key="{escape_xml_manual(key)}" value="{escape_xml_manual(value)}" />' for value in values]) for [key, values] in self.metas.items()])}'
                f'</metadata>'
                f'</head>')

    @property
    def body(self) -> str:
        TTMLLine.index = 0

        if self.parts:
            part_list = copy.deepcopy(self.parts)
            part_text: list[list[str | TTMLLine]] = list[list[str | TTMLLine]]()

            part_text.append(list[str | TTMLLine]())
            for index, line in reversed(list(enumerate(self.lines))):
                part_text[-1].append(line)
                if len(part_list) and index == part_list[-1][1]:
                    part_text[-1].append(part_list[-1][0])
                    part_list.pop()
                    part_text.append(list[str | TTMLLine]())
            if len(part_text[-1]) == 0:
                part_text.pop()
            elif type(part_text[-1][-1]) != "str":
                part_text[-1].append("Verse")

            return (f'<body dur="{AudioTime.stringify(self.lines[-1].end, False, True, True)}">'
                    f'{"".join([f'<div begin="{AudioTime.stringify(part[-2].begin, False, True, True)}" end="{AudioTime.stringify(part[0].end, False, True, True)}" itunes:song-part="{part[-1]}">{"".join([str(line) for line in reversed(part[:-1])])}</div>' for part in reversed(part_text)])}'
                    f'</body>')
        else:
            return (f'<body dur="{AudioTime.stringify(self.lines[-1].end, False, True, True)}">'
                    f'<div begin="{AudioTime.stringify(self.lines[0].begin, False, True, True)}" end="{AudioTime.stringify(self.lines[-1].end, False, True, True)}">{[str(line) for line in self.lines]}</div>'
                    f'</body>')

    def __str__(self) -> str:
        return (
            f'<tt xmlns="http://www.w3.org/ns/ttml" xmlns:ttm="http://www.w3.org/ns/ttml#metadata" xmlns:amll="http://www.example.com/ns/amll" xmlns:itunes="http://music.apple.com/lyric-ttml-internal">'
            f'{self.head}'
            f'{self.body}'
            f'</tt>')
