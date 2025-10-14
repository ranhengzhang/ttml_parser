import copy  # 导入copy模块，用于深拷贝操作
import re  # 导入re模块，用于正则表达式操作

from loguru import logger

from ass.ass_event import ASSEvent, ASSEventGenerator  # 从ass.ass_event模块导入ASSEvent和ASSEventGenerator类
from ass.ass_line import ASSLine  # 从ass.ass_line模块导入ASSLine类
from ass.ass_style import ASSStyle, ASSStyleGenerator  # 从ass.ass_style模块导入ASSStyle和ASSStyleGenerator类
from ttml.ttml import TTML  # 从ttml.ttml模块导入TTML类
from ttml.ttml_line import TTMLLine  # 从ttml.ttml_line模块导入TTMLLine类


class ASS:
    def __init__(self, content: str) -> None:

        """
        ASS类的初始化方法
        :param content: ASS格式的字幕内容字符串
        """
        self.script_info: tuple[list[str], dict[str, str]] = tuple[list[str], dict[str, str]](
            ([], {}))  # 存储脚本信息的元组，包含注释列表和键值对字典
        self.aegisub_project_garbage: dict[str, str] = dict[str, str]()  # 存储Aegisub项目垃圾信息的字典
        self.v4_styles: tuple[ASSStyleGenerator, list[ASSStyle]] = tuple[
            ASSStyleGenerator, list[ASSStyle]]()  # 存储V4+样式生成器和样式列表的元组
        self.events: tuple[ASSEventGenerator, list[ASSEvent]] = tuple[
            ASSEventGenerator, list[ASSEvent]]()  # 存储事件生成器和事件列表的元组

        # 将内容分割成不同的部分，每个部分以两个连续的换行符分隔
        parts: list[list[str]] = list(
            map(lambda text: re.split(r"\r?\n", text), re.split(r"(?:\r?\n){2}", content.strip())))
        for part in parts:
            match part[0]:
                case "[Script Info]":  # 处理脚本信息部分
                    for line in part[1:]:
                        if line.startswith(";"):  # 注释行以分号开头
                            self.script_info[0].append(line)
                        else:  # 键值对行
                            key, val = line.split(": ")
                            self.script_info[1][key] = val
                case "[Aegisub Project Garbage]":  # 处理Aegisub项目垃圾部分
                    for line in part[1:]:
                        key, val = line.split(": ")
                        self.aegisub_project_garbage[key] = val
                case "[V4+ Styles]":  # 处理V4+样式部分
                    generator: ASSStyleGenerator = ASSStyleGenerator(part[1])  # 创建样式生成器
                    self.v4_styles = (generator, list[ASSStyle]([]))  # 初始化样式生成器和样式列表
                    for line in part[2:]:
                        self.v4_styles[1].append(generator.generate(line))  # 生成样式并添加到列表
                case "[Events]":  # 处理事件部分
                    generator: ASSEventGenerator = ASSEventGenerator(part[1])  # 创建事件生成器
                    self.events = (generator, list[ASSEvent]([]))  # 初始化事件生成器和事件列表
                    for line in part[2:]:
                        self.events[1].append(generator.generate(line))  # 生成事件并添加到列表

    def __str__(self):
        """
        将ASS对象转换为字符串格式
        :return: ASS格式的字符串
        """
        # noinspection PyListCreation
        text: list[str] = []  # 用于存储字符串的列表

        # 添加脚本信息部分
        text.append("\r\n[Script Info]")
        text.append("\r\n".join(self.script_info[0]))  # 添加注释
        text.append("\r\n".join(map(lambda value: f"{value[0]}: {value[1]}", self.script_info[1].items())))  # 添加键值对

        # 添加Aegisub项目垃圾部分
        text.append("\r\n[Aegisub Project Garbage]")
        text.append("\r\n".join(map(lambda value: f"{value[0]}: {value[1]}", self.aegisub_project_garbage.items())))

        # 添加V4+样式部分
        text.append("\r\n[V4+ Style]")
        style_generator: ASSStyleGenerator = self.v4_styles[0]
        text.append(str(style_generator))  # 添加样式生成器信息
        text.extend(map(lambda value: style_generator.print(value), self.v4_styles[1]))  # 添加所有样式

        # 添加事件部分
        text.append("\r\n[Events]")
        event_generator: ASSEventGenerator = self.events[0]
        text.append(str(event_generator))  # 添加事件生成器信息
        text.extend(map(lambda value: event_generator.print(value), self.events[1]))  # 添加所有事件

        return "\r\n".join(text)  # 将所有部分合并为一个字符串

    def get_lines(self) -> list[ASSLine]:

        """
        从事件中获取所有ASS行
        :return: ASSLine对象列表
        """
        return list(filter(None, [event.to_ass_line() for event in self.events[1]]))  # 过滤掉空行并返回

    def to_ttml(self) -> TTML:

        """
        将ASS字幕转换为TTML格式
        :return: TTML对象
        """
        lyric_ass_lines: list[ASSLine] = self.get_lines()  # 获取所有ASS行
        lyric_ttml_lines: list[TTMLLine] = list[TTMLLine]()  # 初始化TTML行列表
        ttml_lyric: TTML = TTML()  # 初始化TTML对象

        offset: int = int()
        if "Update Details" in self.script_info[1]:
            update_details = self.script_info[1]["Update Details"]
            # have /[+-]?\d+/ ?
            if re.search(r"[+-]?\d+", update_details):
                offset = int(re.search(r"[+-]?\d+", update_details).group())
            else:
                offset = 0

        if "Title" in self.script_info[1]:
            ttml_lyric.metas["musicName"] |= {s.strip() for s in re.split(r'[&,/]', self.script_info[1]["Title"]) if s}

        # 处理每一行ASS字幕
        for ass_line in lyric_ass_lines:
            match ass_line.style:
                case "orig":  # 原始行
                    lyric_ttml_lines.append(ass_line.to_ttml_line())  # 转换为TTML行
                    if "x-chor" in ass_line.actor:  # 检查是否是合唱行
                        setattr(lyric_ttml_lines[-1], "chor", True)  # 设置合唱属性
                    if "x-part" in ass_line.actor:  # 检查是否标记分段
                        setattr(lyric_ttml_lines[-1], "part", re.search(r"(?<=x-part:)\S+", ass_line.actor).group()) # 设置分段属性 /(?<=x-part:)\S+/
                case "ts":  # 翻译行
                    lang = "zh-CN"  # 默认语言
                    # ass_line.actor 中匹配 /(?<=x-lang:)\S+?/
                    if ass_line.actor:
                        lang_match = re.search(r"(?<=x-lang:)\S+?", ass_line.actor)
                        if lang_match:
                            lang = lang_match.group(0)

                    lyric_ttml_lines[-1].ts_line[lang] = ass_line.syl[0].text
                case "roma":
                    lyric_ttml_lines[-1].roma_line = ass_line.syl[0].text

        for ttml_line in lyric_ttml_lines:
            if hasattr(ttml_line, "part"):
                if ttml_line.part:
                    ttml_lyric.parts.append((getattr(ttml_line, "part"), len(ttml_lyric.lines)))
            ttml_lyric.have_other |= ttml_line.is_other
            if hasattr(ttml_line, "chor"):
                if ttml_line.is_bg:
                    ttml_line.bg_line = copy.deepcopy(ttml_line)
                    ttml_line.is_bg = False
                    ttml_lyric.lines.append(ttml_line)
                else:
                    ttml_lyric.lines.append(copy.deepcopy(ttml_line))
                    ttml_line.is_other = not ttml_line.is_other
                    ttml_lyric.lines.append(ttml_line)
            else:
                if ttml_line.is_bg:
                    ttml_lyric.lines[-1].bg_line = ttml_line
                else:
                    ttml_lyric.lines.append(ttml_line)

        ttml_lyric.offset(offset)

        return ttml_lyric
