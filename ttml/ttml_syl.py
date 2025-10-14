from audio_time import AudioTime
from utils import escape_xml_manual


class TTMLSyl:
    def __init__(self) -> None:
        self.begin: int = int()
        self.end: int = int()
        self.text: str = str()
        self.is_text: bool = False

    def offset(self, offset: int) -> None:
        self.begin += offset
        self.end += offset

    def __str__(self) -> str:
        return escape_xml_manual(self.text) if self.is_text else f'<span begin="{AudioTime.stringify(self.begin, False, True, True)}" end="{AudioTime.stringify(self.end, False, True, True)}">{escape_xml_manual(self.text)}</span>'
