# encoding=utf-8
import random
import os


class sp():
    # `|` `-` ` `
    # _A: "|" Least
    # _B: "-" Often
    # _C: " " Most
    def __init__(self, A: str, B: str, C: str) -> None:
        self._A = A
        self._B = B
        self._C = C

    @property
    def A(self) -> str:
        return self._A

    @property
    def B(self) -> str:
        return self._B

    @property
    def C(self) -> str:
        return self._C

    @property
    def BA(self) -> str:
        return self._B+self._A

    @property
    def AC(self) -> str:
        return self._A+self._C

    @property
    def CA(self) -> str:
        return self._C+self._A

    @property
    def ABC(self) -> str:
        return self._A+self._B+self._C

    @property
    def CAC(self) -> str:
        return self._C+self._A+self._C


class sp_group():
    def __init__(self, index_seperate: sp, title_seperate: sp, content_seperate: sp, row_seperate: sp) -> None:
        self._index_seperate = index_seperate
        self._title_seperate = title_seperate
        self._content_seperate = content_seperate
        self._row_seperate = row_seperate

    @property
    def index_seperate(self) -> sp:
        return self._index_seperate

    @property
    def title_seperate(self) -> sp:
        return self._title_seperate

    @property
    def content_seperate(self) -> sp:
        return self._content_seperate

    @property
    def row_seperate(self) -> sp:
        return self._row_seperate


def generate_minefield(rows, cols, mine_percentage):
    global empty_default
    minefield = [[" " for _ in range(cols)] for _ in range(rows)]

    # Place mines randomly
    total_cells = rows * cols
    num_mines = int(total_cells * mine_percentage / 100)
    mine_positions = random.sample(range(total_cells), num_mines)

    for position in mine_positions:
        row = position // cols
        col = position % cols
        minefield[row][col] = mine_default  # mine_default represents a mine

    return [[empty_default if cell == " " and (r, c) not in mine_positions else cell for c, cell in enumerate(row)] for r, row in enumerate(minefield)]


def print_minefield(field, styles: sp_group, seperate=10):
    rows = len(field)
    cols = len(field[0])
    rL = max(len(str(rows)), 2)
    cL = max(len(str(cols)), 2)

    """
          is  ->    ->    |
          ts  ->    ->    |
    | cs-|    ->    -|    |
    | cs-|    ->    -|    |
    | rs->    ->    ->    |
    | cs-|    ->    -|    |
    | cs-|    ->    -|    |
    """
    sp_is = styles.index_seperate
    sp_ts = styles.title_seperate
    sp_cs = styles.content_seperate
    sp_rs = styles.row_seperate
    # 001 002 003| 004 ... seperate index with generation

    """
    seperate repeats
    structure
    seperateR :
    [A]*rL [B] [... [... D ...] C [... D ...] ...] [C (opt)]

    seperateR = "-"*rL+"-|" +\
        "| ".join(" ".join(["-"*cL for _ in range(seperate)])
                  for _ in range(cols//seperate)) +\
        "|" + (" " + "-"*cL)*(cols % seperate) + \
        ("|"if cols % seperate else "")

    seperateM = " "*rL+"-|" +\
        "|-".join("-".join([" "*cL for _ in range(seperate)])
                  for _ in range(cols//seperate)) +\
        "|" + ("-" + " "*cL)*(cols % seperate) + \
        ("|"if cols % seperate else "")

    print(" "*rL+" |" + " ".join(
        [f"{i:{cL}d}|" if not (i+1) %
         seperate else f"{i:{cL}d}" for i in range(cols)]
    ) + ("|"if cols % seperate else "")
    )
    """
    def ipl(sep: sp):
        return sep.B*rL+sep.BA + sep.B.join(
            [f"{i:{cL}d}{sep.A}" if not (i+1) %
             seperate else f"{i:{cL}d}" for i in range(cols)]
        ) + (sep.A if cols % seperate else "")

    def spl(sep: sp):
        return sep.B*rL + sep.BA + sep.AC.join(
            sep.B.join(sep.C*cL for _ in range(seperate))
            for _ in range(cols//seperate)
        ) + sep.A + (sep.C + sep.BA*cL)*(cols % seperate) + \
            (sep.A if cols % seperate else "") + sep.B*(rL+1)

    def rcl(sep: sp):
        return f"{i:{rL}d}" + sep.CAC + (sep.ABC).join(
            [(sep.C * rL).join(field[i][j:j+seperate])
             for j in range(0, cols, seperate)]
        ) + sep.A + f"{i:{rL}d}"

    print(ipl(sp_is))
    print(spl(sp_ts))

    # Print rows with row numbers
    for i in range(rows):
        if not i % seperate and i:
            print(spl(sp_rs))
        # row  001 | ...
        print(rcl(sp_cs))

    print(spl(sp_ts))
    print(ipl(sp_is))


def initialize_user_interface(minefield, start_row, start_col) -> list[list[str]]:
    global rows, cols, user_default
    user_interface = [
        [user_default for _ in range(rows)] for _ in range(cols)]
    for i in range(start_row-1, start_row+2):
        for j in range(start_col-1, start_col+2):
            mines = surrounding_mines_int(minefield, i, j)
            if mines != -1:
                user_interface[i][j] = str(mines) if mines > 0 else " "
                if user_interface[i][j] == " ":
                    flood_fill(minefield, user_interface, i, j)

    return user_interface


def surrounding_mines_int(minefield, row, col) -> int:
    global rows, cols, mine_default
    mines = 0
    if minefield[row][col] == mine_default:
        return -1
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if minefield[i][j] == mine_default:
                mines += 1
    return mines


def surrounding_mines_str(minefield, row, col) -> str:
    mines = surrounding_mines_int(minefield, row, col)
    return str(mines) if mines > 0 else " "


def is_finished(minefield: list[list[str]], user_interface: list[list[str]], flag: bool) -> bool:
    global mine_percentage, flag_check, rows, cols, mine_default
    if flag:
        return False
    else:
        flag_count = 0
        flag_check = True
        for row in range(rows):
            if "." in user_interface[row]:
                return True
            else:
                for col in range(cols):
                    if user_interface[row][col] == flag:
                        flag_count += 1
                        flag_check &= (minefield[row][col] == mine_default)
        if flag_count == rows*cols*mine_percentage//100:
            if flag_check:
                return False
            else:
                return True
        else:
            return True


def flood_fill(minefield, user_interface, row, col):
    global rows, cols
    if 0 <= row < rows and 0 <= col < cols and user_interface[row][col] == " ":
        user_interface[row][col] = surrounding_mines_str(minefield, row, col)
        if surrounding_mines_int(minefield, row, col) == 0:
            for i in range(max(0, row - 1), min(rows, row + 2)):
                for j in range(max(0, col - 1), min(cols, col + 2)):
                    ffs(minefield, user_interface, i, j)
        else:
            return


def ffs(minefield, user_interface, row, col):
    if 0 <= row < rows and 0 <= col < cols and user_interface[row][col] != " ":
        user_interface[row][col] = surrounding_mines_str(minefield, row, col)
        if surrounding_mines_int(minefield, row, col) == 0:
            for i in range(max(0, row - 1), min(rows, row + 2)):
                for j in range(max(0, col - 1), min(cols, col + 2)):
                    ffs(minefield, user_interface, i, j)
        else:
            return


def get_options() -> tuple[int, int, int, int, bool, bool]:
    rs = 20 if ((a := int(f'0{input("棋盘长度(默认20):")}')) == 0) else a
    cs = 20 if ((a := int(f'0{input("棋盘宽度(默认20):")}')) == 0) else a
    mp = 10 if ((a := int(f'0{input("埋雷比例(默认10):")}')) == 0) else a
    sp = 10 if ((a := int(f'0{input("分割辅助线宽度(默认10):")}')) == 0) else a
    ct = False if (
        (a := bool(input("地雷视图(默认False):").capitalize())) == False) else a
    fb = False if (
        (a := bool(input("字符兼容模式(默认False):").capitalize())) == False) else a
    return (rs, cs, mp, sp, ct, fb)


CHECK = """
UTF-8 字符显示确认
细阴影："░"，深阴影："▓"，二四象限："▚"，圆角方形："▢"
制表符等宽测试，以下内容是否严格对齐
 │░│▓│?│ 
─┼─┼─┼─┼─
 │▢│▚│1│
─┼─┼─┼─┼─
 │ │-│ │ 
若以上内容有显示错误，请更换字体如：
Source Code Pro
JetBarins Mono
或启用兼容模式
"""

DIMAP = """
Y
└─X

S, x, y          : 查看
F, x, y          : 标记
uF, x, y         : 取消标记
SPL, size        : 调整分割线
Cheat            : 看地雷（一次）
Check            : 立刻结算
R                : 重开（相同参数）
Ctrl+C           : 退出
"""

if __name__ == "__main__":
    os.system("chcp 65001 > nul")
    rows = 20
    cols = 20
    mine_percentage = 10
    seperate = 10
    cheat = False
    fail_flag = False
    reopen_flag = True
    flag_check = True
    force_check = False
    fallback_flag = False

    print(CHECK)
    print("参数设置，直接回车使用默认值")
    while 1:
        try:
            rows, cols, mine_percentage, seperate, cheat, fallback_flag = get_options()
            if input(f"{rows} {cols} {mine_percentage} {seperate} {cheat} {fallback_flag}\n确认使用以上参数吗？(Y/N)").upper() != "Y":
                continue
            break
        except ValueError:
            print("输入有误，请重试")
            continue
        except KeyboardInterrupt:
            exit()

    if fallback_flag:
        sp_is = sp("|", " ", " ")
        sp_ts = sp("|", "─", "─")
        sp_cs = sp("|", " ", " ")
        sp_rs = sp("|", "─", "─")
        sps = sp_group(sp_is, sp_ts, sp_cs, sp_rs)

        user_default, user_mine_flag, mine_default, empty_default = (
            "O", "F", "X", ".")
        right_mine_flag, wrong_mine_flag, question_flag = ("√", "B", "?")
    else:
        sp_is = sp("│", " ", " ")
        sp_ts = sp("┼", "─", "─")
        sp_cs = sp("│", " ", " ")
        sp_rs = sp("┼", "─", "─")
        sps = sp_group(sp_is, sp_ts, sp_cs, sp_rs)

        user_default, user_mine_flag, mine_default, empty_default = (
            "▢", "░", "╳", "·")
        right_mine_flag, wrong_mine_flag, question_flag = ("▓", "▚", "?")

    while reopen_flag:
        minefield = generate_minefield(rows, cols, mine_percentage)

        if cheat:
            print("Actual Minefield:")
            print_minefield(minefield, sps)

        start_row, start_col = random.choice(
            [(i, j) for i in range(1, rows - 1) for j in range(1, cols - 1)
             if minefield[i][j] != mine_default]
        )
        user_interface = initialize_user_interface(
            minefield, start_row, start_col)

        print_minefield(user_interface, sps)
        try:
            reopen_flag = False
            while is_finished(minefield, user_interface, fail_flag):
                print(DIMAP)
                operation = " "
                arg1 = arg2 = -1
                try:
                    input_string = input("Operators, arg1 [,arg2]:\n").lower()
                    temp = [[_.strip() for _ in input_string.split(sp)]
                            for sp in (",", "|", ".", "。", "，", " ")]
                    command = max(temp, key=len)
                    match len(command):
                        case 3:
                            operation, arg1, arg2 = command
                        case 2:
                            operation, arg1 = command
                        case 1:
                            operation = command[0]
                        case _:
                            raise ValueError
                except ValueError:
                    continue

                match operation:
                    case "s" | "f" | "uf" | "spl":
                        col = int(arg1)
                        row = int(arg2)
                        if col*row < 0 or row > rows or col > cols:
                            print("错误指令")
                            continue
                        if operation == "s":
                            if user_interface[row][col] == user_default:
                                if minefield[row][col] == mine_default:
                                    user_interface[row][col] = mine_default
                                    fail_flag = True
                                else:
                                    mines = surrounding_mines_int(
                                        minefield, row, col)
                                    user_interface[row][col] = str(
                                        mines) if mines > 0 else " "
                            elif user_interface[row][col] == user_mine_flag:
                                user_interface[row][col] = question_flag
                            elif user_interface[row][col] == question_flag:
                                user_interface[row][col] = user_default

                            if user_interface[row][col] == " ":
                                flood_fill(minefield, user_interface, row, col)

                        elif operation == "f":
                            if user_interface[row][col] == user_default:
                                user_interface[row][col] = user_mine_flag

                        elif operation == "uf":
                            if user_interface[row][col] == user_mine_flag:
                                user_interface[row][col] = user_default

                        elif operation == "spl":
                            seperate = int(arg1)

                        if cheat:
                            print("Actual Minefield:")
                            print_minefield(minefield, sps, seperate)
                        print_minefield(user_interface, sps, seperate)

                    case "cheat":
                        print_minefield(minefield, sps, seperate)

                    case "check":
                        force_check = True
                        break

                    case "r":
                        reopen_flag = True
                        break

                    case _:
                        continue

            def review() -> tuple[int, int, int, float]:
                _wrong = _miss = _checked = _explored = 0
                for row in range(rows):
                    for col in range(cols):
                        if user_interface[row][col] != user_default:
                            _explored += 1
                        if minefield[row][col] == mine_default:
                            if user_interface[row][col] == user_mine_flag:
                                user_interface[row][col] = right_mine_flag
                                _checked += 1
                            else:
                                user_interface[row][col] = mine_default
                                _miss += 1
                        elif minefield[row][col] == empty_default:
                            if user_interface[row][col] == user_mine_flag:
                                user_interface[row][col] = wrong_mine_flag
                                _wrong += 1
                            else:
                                user_interface[row][col] = surrounding_mines_str(
                                    minefield, row, col)

                return (_wrong, _miss, _checked, _explored*100/(rows*cols))

            if flag_check == True:
                print("全部完成")
            if fail_flag == True:
                print("踩到地雷，呃呃，菜菜")
            if force_check == True:
                print("手动结束")
            _wrong, _miss, _checked, _explored = review()
            print(f"选错{_wrong}个，选漏{_miss}个，找对{_checked}个,探索进度:{_explored:2f}%")
            print_minefield(user_interface, sps, seperate)

        except KeyboardInterrupt:
            print("Ctrl+C Exit.")
            exit()
