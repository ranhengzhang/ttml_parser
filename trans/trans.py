import re

from trans.trans_line import TransLine


class Trans:
    def __init__(self, content: str) -> None:
        self.metas: list[tuple[str,str]] = list[tuple[str,str]]()
        self.lines: list[TransLine] = list[TransLine]()

        lines: list[str] = list(filter(None, re.split(r"(?:\r?\n)", content.strip())))

        checker = lambda x: re.match(r'^\[.+?\:.+?\]$', x.strip()) is not None
        if any(checker(line) for line in lines):
            while not checker(lines[0]):
                lines.pop(0)

            while checker(lines[0]):
                matches: re.Match[str] = re.match(r'\[(.+?)\:\s?(.+?)\]', lines.pop(0))
                self.metas.append((matches.group(1).strip(),matches.group(2).strip()))

        self.lines.extend([TransLine(line) for line in lines])