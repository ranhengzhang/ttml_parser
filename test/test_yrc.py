import unittest

from loguru import logger

from trans.trans import Trans
from utils import serialize_object
from yrc.yrc import YRC


# noinspection PyMethodMayBeStatic
class MyTestCase(unittest.TestCase):
    def test_yrc_init(self) -> None:
        with open("../in/lyric.yrc") as in_file:
            content = in_file.read()
            logger.info(str(YRC(content)))

    def test_yrc_line_to_ttml_line(self) -> None:
        with open("../in/lyric.yrc") as in_file:
            content = in_file.read()
            yrc = YRC(content)
            logger.info("\n" + serialize_object(yrc.lines[0].to_ttml_line()))

    def test_yrc_to_ttml(self) -> None:
        with open("../in/lyric.yrc") as in_file:
            content = in_file.read()
            yrc = YRC(content)
            logger.info("\n" + str(yrc.to_ttml()))

    def test_yrc_match_trans(self) -> None:
        with open("../in/lyric.yrc") as in_file:
            content = in_file.read()
            yrc = YRC(content)
            with open("../in/trans.lrc") as trans_file:
                trans = trans_file.read()
                yrc.match_trans(Trans(trans))
            logger.info("\n" + str(yrc.to_ttml()))


if __name__ == '__main__':
    unittest.main()
