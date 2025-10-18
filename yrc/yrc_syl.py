from ttml.ttml_syl import TTMLSyl


class YRCSyl:
    def __init__(self) -> None:
        self.start: int = int()
        self.duration: int = int()
        self.text: str = str()

    def __str__(self) -> str:
        return f'({self.start},{self.duration},0){self.text}'

    def to_ttml_syl(self) -> TTMLSyl:
        syl: TTMLSyl = TTMLSyl()

        syl.begin = self.start
        syl.end = self.start + self.duration
        syl.text = self.text
        syl.is_text = not self.text.strip()

        return syl