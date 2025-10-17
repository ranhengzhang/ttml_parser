from ttml.ttml_syl import TTMLSyl


class ASSSyl:
    def __init__(self) -> None:
        self._start_time: int = int()
        self._end_time: int = int()
        self.text: str = str()
        self.inline_fx: str | None = None
        self.is_furi: bool = False
        self.furi: list["ASSSyl"] = list["ASSSyl"]()

    @property
    def start_time(self) -> int:
        return self._start_time

    @start_time.setter
    def start_time(self, time: int) -> None:
        self._start_time = time
        if self._start_time >= self._end_time:
            self._end_time = self._start_time

    @property
    def end_time(self) -> int:
        return self._end_time

    @end_time.setter
    def end_time(self, time: int) -> None:
        self._end_time = time
        if self._start_time >= self._end_time:
            self._start_time = self._end_time

    @property
    def duration(self) -> int:
        return self._end_time - self._start_time

    @duration.setter
    def duration(self, time: int) -> None:
        self._end_time = self._start_time + time

    def append_furi(self, furi: "ASSSyl"):
        self.furi.append(furi)
        self.end_time = furi.end_time

    def to_ttml_syl(self) -> TTMLSyl:
        syl: TTMLSyl = TTMLSyl()

        syl.begin = self.start_time
        syl.end = self.start_time + 5 if self.inline_fx == "zero" or self.inline_fx == 'Z' else self.end_time
        syl.text = self.text
        syl.is_text = self.inline_fx == "text" or self.inline_fx == 'T' or not self.text.strip()

        return syl
