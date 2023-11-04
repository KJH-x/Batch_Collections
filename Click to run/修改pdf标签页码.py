import re
import pyperclip
msg = pyperclip.paste()


def increment_numbers(text: str, shift: int) -> str:
    lines = text.splitlines()
    pattern = r'( \d{1,2})$'  # 匹配以[Tab][1-2位数字]结尾的模式

    for i in range(len(lines)):
        match = re.search(pattern, lines[i])
        if match:
            number = int(match.group(1)[1:])  # 提取数字并转换为整数
            new_number = number + shift
            new_line = lines[i][:match.start(
                1)+1] + '\t' + str(new_number) + lines[i][match.end(1):]
            lines[i] = new_line

    modified_text = '\n'.join(lines)
    return modified_text


msg = increment_numbers(msg, 2)
pyperclip.copy(msg)
