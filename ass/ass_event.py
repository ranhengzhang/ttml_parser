import re

import numpy
from loguru import logger

from ass.ass_line import ASSLine
from ass.ass_syl import ASSSyl
from audio_time import AudioTime


class ASSEvent:
    def __init__(self) -> None:
        self.Format: str = ""
        self.Layer: str = ""
        self.Start: str = ""
        self.End: str = ""
        self.Style: str = ""
        self.Name: str = ""
        self.MarginL: str = ""
        self.MarginR: str = ""
        self.MarginV: str = ""
        self.Effect: str = ""
        self.Text: str = ""

    def to_ass_line(self) -> ASSLine | None:
        logger.trace(self.Effect)
        if (self.Effect and self.Effect != "karaoke") or not self.Style in ["orig", "ts", "roma"]:
            return None

        line: ASSLine = ASSLine()

        line.comment = self.Format == "Comment"
        line.layer = int(self.Layer)
        line.style = self.Style
        line.actor = self.Name
        line.start_time = AudioTime.parse(self.Start)
        line.end_time = AudioTime.parse(self.End)
        line.duration = line.end_time - line.start_time

        if re.search(r"\{[^\}]+\}", self.Text):
            # noinspection RegExpRedundantEscape
            index_list: list[int] = [ite.start() for ite in re.finditer(r"\{[^\}]+\}", self.Text)]
            syl_list: list[str] = list(
                filter(None, map(lambda part: "".join(part), numpy.split([char for char in self.Text], index_list))))
            # 从后往前遍历 syl_list 将没有 \k 的部分向前合并(忽略大小写)
            for i in range(len(syl_list) - 1, 0, -1):
                if not re.search(r"\\k", syl_list[i], re.IGNORECASE):
                    syl_list[i - 1] += syl_list[i]
                    syl_list[i] = ""
            syl_list: list[str] = list(map(lambda syl: syl.replace("}{", ""), filter(None, syl_list)))
            # logger.debug("\n" + "\n".join(syl_list))
            start_time = line.start_time
            for syl_text in syl_list:
                syl: ASSSyl = ASSSyl()
                tags, text = re.match(r"(\{[^\}]+\})(.*)", syl_text, re.IGNORECASE).groups()
                tags: str
                text: str
                k: str = re.search(r"\\k[fo]?(\d+)", tags, re.IGNORECASE).group(1)
                duration = int(k) * 10

                syl.start_time = start_time
                syl.duration = duration
                syl.end_time = start_time + duration

                # inner effect
                if r"\-" in tags:
                    syl.inline_fx = re.search(r"\\-([^\\\}]+)", tags).group(1)

                # syl - furi
                if '|' in text:
                    syl_text, furi_text = re.split(r"\|<?", text)
                    if syl_text and syl_text != "#":
                        syl.text = syl_text
                        line.syl.append(syl)
                    if furi_text:
                        furi: ASSSyl = ASSSyl()
                        furi.start_time = start_time
                        furi.duration = duration
                        furi.end_time = start_time + duration
                        furi.is_furi = True
                        furi.text = furi_text
                        line.syl[-1].append_furi(furi)
                # pure syl
                elif text:
                    syl.text = text
                    line.syl.append(syl)
                start_time += duration
        else:
            syl: ASSSyl = ASSSyl()
            syl.start_time = line.start_time
            syl.duration = line.duration
            syl.end_time = line.end_time
            syl.text = self.Text
            line.syl.append(syl)

        return line


class ASSEventGenerator:
    def __init__(self, content: str) -> None:
        self.format: list[str] = list[str]()

        format_value, others_value = re.split(r":\s?", content, maxsplit=1)
        self.format.append(format_value)
        self.format.extend(re.split(r",\s?", others_value))

    def __str__(self):
        return f"{self.format[0]}: {', '.join(self.format[1:])}"

    def generate(self, content: str) -> ASSEvent | None:
        event = ASSEvent()

        # noinspection DuplicatedCode
        format_value, others_value = re.split(r":\s?", content, maxsplit=1)
        if not hasattr(event, self.format[0]):
            logger.error(f"Invalid format: {self.format[0]}")
            return None
        setattr(event, self.format[0], format_value)
        for index, value in enumerate(re.split(r",\s?", others_value, maxsplit=len(self.format) - 2)):
            if not hasattr(event, self.format[index + 1]):
                logger.error(f"Invalid format: {self.format[index + 1]}")
                return None
            setattr(event, self.format[index + 1], value)

        return event

    def print(self, content: ASSEvent):
        return f"{getattr(content, self.format[0])}: {','.join(map(lambda value: getattr(content, value), self.format[1:]))}"
