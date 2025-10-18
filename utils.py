import json
import re
from typing import AnyStr

check_leading_space: re.Pattern[AnyStr] = re.compile(r'^\s+')
check_trailing_space: re.Pattern[AnyStr] = re.compile(r'\s+$')

replace_leading_bracket = lambda text: re.sub(r'^[(（]*', r'(', text)
replace_trailing_bracket = lambda text: re.sub(r'[)）]*$', r')', text)

def escape_xml_manual(text: str) -> str:
    """
    不借助库，将字符串转换为 XML 安全的形式。

    该函数手动替换5个XML特殊字符。
    """
    # 替换的顺序至关重要。
    # 必须先替换 '&'，以避免对其他转义序列（如 '&lt;'）中的 '&' 进行二次转义。
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = text.replace("\"", "&quot;")
    text = text.replace("'", "&apos;")
    return text


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