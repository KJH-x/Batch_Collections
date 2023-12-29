import time
import os


def calculate_bpm(timestamps) -> tuple[float, float, int]:
    if len(timestamps) < 2:
        return 0, 0, 0

    time_diffs = [timestamps[i] - timestamps[i-1]
                  for i in range(1, len(timestamps))]
    # print(f"cb: time_diffs: {time_diffs}")
    avg_time_diff = sum(time_diffs) / len(time_diffs)
    filtered_time_diffs = [diff for diff in time_diffs if abs(
        diff - avg_time_diff) <= 0.2 * avg_time_diff]
    # print(f"cb: 0.1 * avg_time_diff: {0.1 * avg_time_diff}")
    exclude_list = [f"{x:.3f}" for x in list(
        set(time_diffs)-set(filtered_time_diffs))]
    # print(f"cb: avg: {avg_time_diff}")
    # print(f"cb: exclude: {', '.join(exclude_list)}")

    if (not len(filtered_time_diffs)) or (not sum(filtered_time_diffs)):
        return 0, 0, 0

    bpm = 60 / (sum(filtered_time_diffs) / len(filtered_time_diffs))
    return bpm, (sum(filtered_time_diffs) / len(filtered_time_diffs)), len(exclude_list)


def main():
    timestamps = []
    bpm_list = []
    last_timestamp = None
    current_bpm = 0
    print("在合适的节拍位置连续按下 Enter 开始计算 BPM，按下 Ctrl+C 结束程序...")

    input("按下 Enter:")
    ctd = 0.0
    try:
        while True:
            current_timestamp = time.time()
            if last_timestamp is not None:
                time_difference = current_timestamp - last_timestamp
                # print(f"main: td: {time_difference}")
                # print(f"main: timestamps: {timestamps}")
                # print(f"main: judge: {(timestamps[-1] - timestamps[0])}")
                if len(timestamps) > 2 and ctd:
                    if time_difference > 2 * ctd:
                        timestamps = []
                        bpm_list.append(current_bpm)
            timestamps.append(current_timestamp)
            last_timestamp = current_timestamp
            last_bpm = current_bpm
            current_bpm, ctd, exclude_count = calculate_bpm(timestamps)

            os.system("cls")
            if current_bpm != 0:
                if current_bpm > last_bpm:
                    print(
                        f"\n[{len(timestamps):03d}]当前BPM: {current_bpm:.2f}(+), 继续按下Enter:")
                elif current_bpm == last_bpm:
                    print(
                        f"\n[{len(timestamps):03d}]当前BPM: {current_bpm:.2f}(=), 继续按下Enter:")
                elif current_bpm < last_bpm:
                    print(
                        f"\n[{len(timestamps):03d}]当前BPM: {current_bpm:.2f}(-), 继续按下Enter:")
                input(f"  - 排除了{exclude_count}个数据")
            else:
                input(f"\n[{len(timestamps):03d}]继续按下Enter:")

    except KeyboardInterrupt:
        print("\n程序结束")
        input("\n".join([str(x) for x in bpm_list]))


if __name__ == "__main__":
    main()
