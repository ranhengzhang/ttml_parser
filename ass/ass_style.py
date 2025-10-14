import re

from loguru import logger


class ASSStyle:
    def __init__(self) -> None:
        self.Format: str = ""
        self.Name: str = ""
        self.Fontname: str = ""
        self.Fontsize: str = ""
        self.PrimaryColour: str = ""
        self.SecondaryColour: str = ""
        self.OutlineColour: str = ""
        self.BackColour: str = ""
        self.Bold: str = ""
        self.Italic: str = ""
        self.Underline: str = ""
        self.StrikeOut: str = ""
        self.ScaleX: str = ""
        self.ScaleY: str = ""
        self.Spacing: str = ""
        self.Angle: str = ""
        self.BorderStyle: str = ""
        self.Outline: str = ""
        self.Shadow: str = ""
        self.Alignment: str = ""
        self.MarginL: str = ""
        self.MarginR: str = ""
        self.MarginV: str = ""
        self.Encoding: str = ""


class ASSStyleGenerator:
    def __init__(self, content: str) -> None:
        self.format: list[str] = list[str]()

        format_value, others_value = re.split(r":\s?", content, maxsplit=1)
        self.format.append(format_value)
        self.format.extend(re.split(r",\s?", others_value))

    def __str__(self) -> str:
        return f"{self.format[0]}: {', '.join(self.format[1:])}"

    def generate(self, content: str) -> ASSStyle | None:
        style = ASSStyle()

        # noinspection DuplicatedCode
        format_value, others_value = re.split(r":\s?", content, maxsplit=1)
        if not hasattr(style, self.format[0]):
            logger.error(f"Invalid format: {self.format[0]}")
            return None
        setattr(style, self.format[0], format_value)
        for index, value in enumerate(re.split(r",\s?", others_value, maxsplit=len(self.format) - 2)):
            if not hasattr(style, self.format[index + 1]):
                logger.error(f"Invalid format: {self.format[index + 1]}")
                return None
            setattr(style, self.format[index + 1], value)

        return style

    def print(self, content: ASSStyle):
        return f"{getattr(content, self.format[0])}: {','.join(map(lambda value: getattr(content, value), self.format[1:]))}"
