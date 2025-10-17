import unittest

from loguru import logger

from audio_time import AudioTime


# noinspection PyMethodMayBeStatic
class MyTestCase(unittest.TestCase):
    def test_audio_time(self) -> None:
        logger.info(AudioTime.stringify(65537, False, True, True))
        logger.info(AudioTime.parse("01:05.537"))


if __name__ == '__main__':
    unittest.main()