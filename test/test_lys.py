import unittest

from loguru import logger

from lys.lys import LYS
from trans.trans import Trans
from utils import serialize_object


# noinspection PyMethodMayBeStatic
class MyTestCase(unittest.TestCase):
    def test_lys_init(self) -> None:
        with open("../in/lyric.lys") as in_file:
            content = in_file.read()
            logger.info(str(LYS(content)))

    def test_lys_line_to_ttml_line(self) -> None:
        with open("../in/lyric.lys") as in_file:
            content = in_file.read()
            lys = LYS(content)
            logger.info("\n" + serialize_object(lys.lines[0].to_ttml_line()))

    def test_lys_to_ttml(self) -> None:
        with open("../in/lyric.lys") as in_file:
            content = in_file.read()
            lys = LYS(content)
            logger.info("\n" + str(lys.to_ttml()))

    def test_lys_match_trans(self) -> None:
        with open("../in/lyric.lys") as in_file:
            content = in_file.read()
            lys = LYS(content)
            with open("../in/trans.lrc") as trans_file:
                trans = trans_file.read()
                lys.match_trans(Trans(trans))
            logger.info("\n" + str(lys.to_ttml()))


if __name__ == '__main__':
    unittest.main()
