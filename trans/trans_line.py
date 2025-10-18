from audio_time import AudioTime


class TransLine:
    def __init__(self, content: str) -> None:
        self.begin: int = int()
        self.text: str = str()

        self.begin = AudioTime.parse(content[1:content.index(']')])
        self.text = content[content.index(']') + 1:].strip()