from ttml.ttml_syl import TTMLSyl


class ASSSyl:
    def __init__(self) -> None:
        self.start_time: int = int()
        self.end_time: int = int()
        self.duration: int = int()
        self.text: str = str()
        self.inline_fx: str | None = None
        self.is_furi: bool = False
        self.furi: list["ASSSyl"] = list["ASSSyl"]()

    def append_furi(self, furi: "ASSSyl"):
        self.furi.append(furi)
        self.end_time = furi.end_time
        self.duration = self.end_time - self.start_time

    def to_ttml_syl(self) -> TTMLSyl:
        syl: TTMLSyl = TTMLSyl()

        syl.begin = self.start_time
        syl.end = self.start_time + 5 if self.inline_fx == "zero" or self.inline_fx == 'Z' else self.end_time
        syl.text = self.text
        syl.is_text = self.inline_fx == "text" or self.inline_fx == 'T' or not self.text.strip()

        return syl
