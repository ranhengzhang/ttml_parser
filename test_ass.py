import json
import unittest

from loguru import logger

from ass.ass import ASS
from audio_time import AudioTime


def serialize_object(obj, indent=2) -> str:
    """
    对象序列化的入口函数，返回格式化的 JSON 字符串

    Args:
        obj: 任意 Python 对象
        indent: JSON 字符串的缩进量

    Returns:
        格式化的 JSON 字符串
    """

    def _serialize(obj):
        """
        递归序列化对象的内部实现函数
        Args:
            obj: 任意 Python 对象

        Returns:
            序列化后的对象
        """
        # 处理 None
        if obj is None:
            return None

        # 处理基本数据类型
        if isinstance(obj, (str, int, float, bool)):
            return obj

        # 处理列表和元组
        if isinstance(obj, (list, tuple)):
            return [_serialize(item) for item in obj]

        # 处理字典
        if isinstance(obj, dict):
            return {key: _serialize(value) for key, value in obj.items()}

        # 处理set
        if isinstance(obj, set):
            return [_serialize(item) for item in obj]

        # 处理对象
        if hasattr(obj, '__dict__'):
            return _serialize(obj.__dict__)

        # 处理其他类型
        try:
            return str(obj)
        except:
            return None

    # 先进行递归序列化，然后格式化返回
    serialized_data = _serialize(obj)
    return json.dumps(serialized_data, indent=indent, ensure_ascii=False)


# noinspection PyMethodMayBeStatic
class ASSTestCase(unittest.TestCase):
    def test_ass_init(self) -> None:
        with open("in.txt") as in_file:
            content = in_file.read()
            logger.info(str(ASS(content)))

    def test_audio_time(self) -> None:
        logger.info(AudioTime.stringify(65537, False, True, True))
        logger.info(AudioTime.parse("01:05.537"))

    def test_event_to_line(self) -> None:
        with open("in.txt") as in_file:
            content = in_file.read()
            ass = ASS(content)
            line = ass.events[1][202].to_ass_line()
            logger.info("\n" + serialize_object(line))

    def test_get_ass_lines(self) -> None:
        with open("in.txt") as in_file:
            content = in_file.read()
            ass = ASS(content)
            lines = ass.get_lines()
            logger.info("\n" + serialize_object(lines))

    def test_ass_line_to_ttml_line(self) -> None:
        with open("in.txt") as in_file:
            content = in_file.read()
            ass = ASS(content)
            lines = ass.get_lines()
            logger.info("\n" + serialize_object(lines[0].to_ttml_line()))

    def test_ass_to_ttml(self) -> None:
        with open("in.txt") as in_file:
            content = in_file.read()
            ass = ASS(content)
            logger.info("\n" + serialize_object(ass.to_ttml()))

    def test_ttml_head(self) -> None:
        with open("in.txt") as in_file:
            content = in_file.read()
            ttml = ASS(content).to_ttml()
            logger.info("\n" + ttml.head)

    def test_ttml_body(self) -> None:
        with open("in.txt") as in_file:
            content = in_file.read()
            ttml = ASS(content).to_ttml()
            logger.info("\n" + ttml.body)

    def test_ttml_str(self) -> None:
        with open("in.txt") as in_file:
            content = in_file.read()
            ttml = ASS(content).to_ttml()
            logger.info("\n" + str(ttml))


if __name__ == '__main__':
    unittest.main()
