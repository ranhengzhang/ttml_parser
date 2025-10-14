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