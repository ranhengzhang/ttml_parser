import unittest

from loguru import logger

from ass.ass import ASS


# noinspection PyMethodMayBeStatic
class MyTestCase(unittest.TestCase):
    def test_ttml_head(self) -> None:
        with open("in/lyric.ass") as in_file:
            content = in_file.read()
            ttml = ASS(content).to_ttml()
            logger.info("\n" + ttml.head)

    def test_ttml_body(self) -> None:
        with open("in/lyric.ass") as in_file:
            content = in_file.read()
            ttml = ASS(content).to_ttml()
            logger.info("\n" + ttml.body)

    def test_ttml_str(self) -> None:
        with open("in/lyric.ass") as in_file:
            content = in_file.read()
            ttml = ASS(content).to_ttml()
            logger.info("\n" + str(ttml))


if __name__ == '__main__':
    unittest.main()
