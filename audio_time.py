class AudioTime:
    @staticmethod
    def parse(content: str, offset: int = 0) -> int:
        *parts, last = content.split(":")
        parts: list[str]
        last: str

        parts.extend(last.split(".") if '.' in last else [last])
        value: int = 0
        for part in parts[:-1]:
            value *= 60
            value += int(part)
        value *= 1000
        value += int(parts[-1]) * (10 ** (3 - len(parts[-1])))

        return value + offset

    @staticmethod
    def stringify(value: int, prefix: bool, suffix: bool, use_dot: bool) -> str:
        # noinspection PyListCreation
        text: list[str] = []

        text.append(("{:0>3d}" if suffix else "{:0>2d}").format((value % 1000) // (10 ** (1 - int(suffix)))))
        text.append("." if use_dot else ":")
        value //= 1000
        text.append(("{:0>2d}" if prefix or value >= 60 else "{:d}").format(value % 60))
        value //= 60
        if prefix or value >= 60:
            text.append(":")
            text.append(("{:0>2d}" if value >= 60 else "{:d}").format(value % 60))
            value //= 60
        if value:
            text.append(":")
            text.append(str(value))

        return "".join(reversed(text))
