import random
import os


def generate_minefield(rows, cols, mine_percentage):
    minefield = [[" " for _ in range(cols)] for _ in range(rows)]

    # Place mines randomly
    total_cells = rows * cols
    num_mines = int(total_cells * mine_percentage / 100)
    mine_positions = random.sample(range(total_cells), num_mines)

    for position in mine_positions:
        row = position // cols
        col = position % cols
        minefield[row][col] = 'X'  # 'X' represents a mine

    return [['·' if cell == " " and (r, c) not in mine_positions else cell for c, cell in enumerate(row)] for r, row in enumerate(minefield)]


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
            [f"{i:{cL}d}|" if not (i+1) %
             seperate else f"{i:{cL}d}" for i in range(cols)]
        ) + (sep.A if cols % seperate else "")

    def spl(sep: sp):
        return sep.B*rL + sep.BA + sep.AC.join(
            sep.B.join(sep.C*cL for _ in range(seperate))
            for _ in range(cols//seperate)
        ) + sep.A + (sep.C + sep.BA*cL)*(cols % seperate) + \
            (sep.A if cols % seperate else "")

    def rcl(sep: sp):
        return f"{i:{rL}d}"+sep.CAC + (sep.ABC).join(
            [(sep.C * rL).join(field[i][j:j+seperate])
             for j in range(0, cols, seperate)]
        ) + sep.A

    print(ipl(sp_is))
    print(spl(sp_ts))

    # Print rows with row numbers
    for i in range(rows):
        if not i % seperate and i:
            print(spl(sp_rs))
        # row  001 | ...
        print(rcl(sp_cs))

    print(spl(sp_ts))


def initialize_user_interface(minefield, start_row, start_col) -> list[list[str]]:
    user_interface = [
        ["·" for _ in range(len(minefield[0]))] for _ in range(len(minefield))]
    mines = count_surrounding_mines(minefield, start_row, start_col)
    user_interface[start_row][start_col] = str(mines) if mines > 0 else " "
    if user_interface[start_row][start_col] == " ":
        flood_fill(minefield, user_interface, start_row, start_col)
    return user_interface


def count_surrounding_mines(minefield, row, col) -> int:
    mines = 0
    for i in range(max(0, row - 1), min(len(minefield), row + 2)):
        for j in range(max(0, col - 1), min(len(minefield[0]), col + 2)):
            if minefield[i][j] == 'X':
                mines += 1
    return mines


def is_finished(minefield, flag: bool) -> bool:
    if flag:
        return False
    else:
        for row in minefield:
            if "·" in row:
                return True
        return False


def flood_fill(minefield, user_interface, row, col):
    if 0 <= row < len(minefield) and 0 <= col < len(minefield[0]) and user_interface[row][col] == " ":
        mines = count_surrounding_mines(minefield, row, col)
        user_interface[row][col] = str(mines) if mines > 0 else " "
        if mines == 0:
            for i in range(max(0, row - 1), min(len(minefield), row + 2)):
                for j in range(max(0, col - 1), min(len(minefield[0]), col + 2)):
                    ffs(minefield, user_interface, i, j)
        else:
            return


def ffs(minefield, user_interface, row, col):
    if 0 <= row < len(minefield) and 0 <= col < len(minefield[0]) and user_interface[row][col] != " ":
        mines = count_surrounding_mines(minefield, row, col)
        user_interface[row][col] = str(mines) if mines > 0 else " "
        if mines == 0:
            for i in range(max(0, row - 1), min(len(minefield), row + 2)):
                for j in range(max(0, col - 1), min(len(minefield[0]), col + 2)):
                    ffs(minefield, user_interface, i, j)
        else:
            return


def get_options() -> tuple:
    rs = 20 if ((a := int(f'0{input("棋盘长度(默认20):")}')) == 0) else a
    cs = 20 if ((a := int(f'0{input("棋盘宽度(默认20):")}')) == 0) else a
    mp = 10 if ((a := int(f'0{input("埋雷比例(默认10):")}')) == 0) else a
    sp = 10 if ((a := int(f'0{input("分割辅助线宽度(默认10):")}')) == 0) else a
    ct = False if (
        (a := bool(input("地雷视图(默认False):").capitalize())) == False) else a
    return (rs, cs, mp, sp, ct)


if __name__ == "__main__":
    os.system("chcp 65001 > nul")
    rows = 20
    cols = 20
    mine_percentage = 10
    seperate = 10
    cheat = False
    fail_flag = False
    sp_is = sp("|", " ", " ")
    sp_ts = sp("|", "_", "_")
    sp_cs = sp("|", " ", " ")
    sp_rs = sp("|", "_", "_")

    print("输入参数，直接回车使用默认值")
    while 1:
        try:
            rows, cols, mine_percentage, seperate, cheat = get_options()
            if input(f"{rows} {cols} {mine_percentage} {seperate} {cheat}\n确认吗？(Y/N)").upper() != "Y":
                continue
            break
        except ValueError:
            print("输入有误，请重试")
            continue
        except KeyboardInterrupt:
            exit()

    minefield = generate_minefield(rows, cols, mine_percentage)

    if cheat:
        print("Actual Minefield:")
        print_minefield(minefield, sp_group(sp_is, sp_ts, sp_cs, sp_rs))

    start_row, start_col = random.choice([(i, j) for i in range(
        1, rows - 1) for j in range(1, cols - 1) if minefield[i][j] != 'X'])

    user_interface = initialize_user_interface(minefield, start_row, start_col)

    print("User Interface:")
    print_minefield(user_interface, sp_group(sp_is, sp_ts, sp_cs, sp_rs))
    try:
        print("s|sweep :查看")
        print("Ctrl+C  :退出")
        # print("R,0,0   :重开（相同参数）")
        while is_finished(user_interface, fail_flag):
            try:
                operation, coli, rowi = input(
                    "operation, col, row:\n").lower().split(",")
            except ValueError:
                continue
            col = int(rowi)
            row = int(coli)
            match operation:
                case "s" | "sweep":
                    if user_interface[row][col] == "·":
                        if minefield[row][col] == "X":
                            print("Hit the mine!")
                            fail_flag = True
                        else:
                            mines = count_surrounding_mines(
                                minefield, row, col)
                            user_interface[row][col] = str(
                                mines) if mines > 0 else " "
                        if user_interface[row][col] == " ":
                            flood_fill(minefield, user_interface, row, col)
                    elif user_interface[row][col] == " ":
                        flood_fill(minefield, user_interface, row, col)
            if cheat:
                print("Actual Minefield:")
                print_minefield(minefield, sp_group(
                    sp_is, sp_ts, sp_cs, sp_rs), seperate)
            print("User Interface:")
            print_minefield(user_interface, sp_group(
                sp_is, sp_ts, sp_cs, sp_rs), seperate)
    except KeyboardInterrupt:
        print("Ctrl+C Exit.")
