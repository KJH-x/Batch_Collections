import difflib
import pyperclip


def remove_duplicates(seq):
    seen = set()
    return [x for x in seq if not (x in seen or seen.add(x))]


raw_string = input("要处理的内容：(空置回车以读取剪切板)\n")
raw_string = pyperclip.paste() if not raw_string else raw_string
split_char = input("分隔符（单个字符/单个字符串）:")
split_char = "\n" if (not split_char or split_char == "\\n") else split_char

if split_char != "\n":
    raw_string.replace("\n", "")

items_list = raw_string.split(split_char)
items_set = remove_duplicates(items_list)
# items_list.sort()
# items_set.sort()

differ = difflib.Differ()
diff = list(differ.compare(items_list, items_set))
print(f"原行数{len(items_list)}，新行数{len(items_set)}")
print(f"差异{len([x for x in diff if (x.startswith('-')or x.startswith('+ '))])}行")
for i, line in enumerate(diff, start=1):
    if line.startswith("- ") or line.startswith("+ "):
        print(f"@Line {i}: {line}")

pyperclip.copy(split_char.join(items_set))
