import re


def convert_ass_to_srt(ass_file_path, srt_file_path):
    try:
        with open(ass_file_path, 'r', encoding='utf-8') as ass_file:
            ass_data = ass_file.read()

        # Get the format for the dialogue block from the [Events] section
        format_pattern = re.search(
            r'\[Events\].*?Format:\s*(.+?)\r?\n', ass_data, re.DOTALL)
        if format_pattern:
            column_order = [col.strip().lower()
                            for col in format_pattern.group(1).split(',')]
            if 'start' not in column_order or 'end' not in column_order or 'text' not in column_order:
                raise ValueError(
                    "Invalid .ass format. Required columns 'Start', 'End', and 'Text' are missing.")

        # Regular expression pattern to match dialogue blocks within [Events] section
        dialogue_pattern = r'Dialogue:\s*(.*?)\r?\n'
        dialogue_blocks = re.findall(dialogue_pattern, ass_data, re.DOTALL)

        # Convert the dialogue blocks to .srt format
        srt_data = ''
        for index, block in enumerate(dialogue_blocks, start=1):
            dialogue_data = dict(zip(column_order, block.split(',')))
            start_time = dialogue_data['start']
            end_time = dialogue_data['end']
            text = dialogue_data['text'].replace('\\N', '\n')

            srt_data += f"{index}\r\n{convert_time_format(start_time)} --> {convert_time_format(end_time)}\n{text}\n\n"

        with open(srt_file_path, 'w', encoding='utf-8', newline='\r\n') as srt_file:
            srt_file.write(srt_data)

        print("Conversion successful.")
    except Exception as e:
        print("Error occurred during conversion:", e)


def convert_time_format(time_str):
    # Convert time format from HH:MM:SS.ss to HH:MM:SS,ss
    return time_str.replace('.', ',')

if __name__ == "__main__":
    ass_file_path = input("输入.ass路径: ")
    srt_file_path = ass_file_path.replace(".ass",".srt")
    convert_ass_to_srt(ass_file_path, srt_file_path)
