from ttml.ttml_syl import TTMLSyl


class LYSSyl:
    def __init__(self):
        self.start: int = int()
        self.duration: int = int()
        self.text: str = str()

    def __str__(self) -> str:
        return f'{self.text}({self.start},{self.duration})'

    def to_ttml_syl(self) -> TTMLSyl:
        syl: TTMLSyl = TTMLSyl()

        syl.begin = self.start
        syl.end = self.start + self.duration
        syl.text = self.text
        syl.is_text = not self.text.strip()

        return syl