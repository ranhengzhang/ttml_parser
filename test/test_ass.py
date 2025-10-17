import unittest

from loguru import logger

from ass.ass import ASS
from utils import serialize_object


# noinspection PyMethodMayBeStatic
class ASSTestCase(unittest.TestCase):
    def test_ass_init(self) -> None:
        with open("in/lyric.ass") as in_file:
            content = in_file.read()
            logger.info(str(ASS(content)))

    def test_event_to_line(self) -> None:
        with open("in/lyric.ass") as in_file:
            content = in_file.read()
            ass = ASS(content)
            line = ass.events[1][202].to_ass_line()
            logger.info("\n" + serialize_object(line))

    def test_get_ass_lines(self) -> None:
        with open("in/lyric.ass") as in_file:
            content = in_file.read()
            ass = ASS(content)
            lines = ass.get_lines()
            logger.info("\n" + serialize_object(lines))

    def test_ass_line_to_ttml_line(self) -> None:
        with open("in/lyric.ass") as in_file:
            content = in_file.read()
            ass = ASS(content)
            lines = ass.get_lines()
            logger.info("\n" + serialize_object(lines[0].to_ttml_line()))

    def test_ass_to_ttml(self) -> None:
        with open("in/lyric.ass") as in_file:
            content = in_file.read()
            ass = ASS(content)
            logger.info("\n" + str(ass.to_ttml()))


if __name__ == '__main__':
    unittest.main()
