import unittest

from loguru import logger

from qrc.qrc import QRC
from trans.trans import Trans
from utils import serialize_object


# noinspection PyMethodMayBeStatic
class MyTestCase(unittest.TestCase):
    def test_qrc_init(self) -> None:
        with open("../in/lyric.qrc") as in_file:
            content = in_file.read()
            logger.info(serialize_object(QRC(content)))

    def test_qrc_line_to_ttml_line(self) -> None:
        with open("../in/lyric.qrc") as in_file:
            content = in_file.read()
            qrc = QRC(content)
            logger.info("\n" + serialize_object(qrc.lines[0].to_ttml_line()))

    def test_qrc_to_ttml(self) -> None:
        with open("../in/lyric.qrc") as in_file:
            content = in_file.read()
            qrc = QRC(content)
            logger.info("\n" + str(qrc.to_ttml()))

    def test_qrc_match_trans(self) -> None:
        with open("../in/lyric.qrc") as in_file:
            content = in_file.read()
            qrc = QRC(content)
            with open("../in/trans.lrc") as trans_file:
                trans = trans_file.read()
                qrc.match_trans(Trans(trans))
            logger.info("\n" + str(qrc.to_ttml()))


if __name__ == '__main__':
    unittest.main()
