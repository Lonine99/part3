import csv
import os
from mytable.core import Table, TableStructureError

def load_table(file_list):
    if isinstance(file_list, str):
        file_list = [file_list]

    all_data = []
    header = None
    for i, f in enumerate(file_list):
        with open(f, 'r', encoding='utf-8', newline='') as fp:
            reader = csv.reader(fp)
            data = list(reader)
            if i == 0:
                header = data[0]
                all_data.extend(data)
            else:
                # 检查表头一致性
                if data[0] != header:
                    raise TableStructureError("多文件加载时表头不一致：{}".format(f))
                all_data.extend(data[1:])
    return Table(all_data)

def save_table(table, file_path, max_rows=None):
    if max_rows is None or max_rows >= (len(table.data)-1):
        # 不拆分
        with open(file_path, 'w', encoding='utf-8', newline='') as fp:
            writer = csv.writer(fp)
            writer.writerows(table.data)
    else:
        # 拆分
        base, ext = os.path.splitext(file_path)
        header = table.data[0]
        rows = table.data[1:]
        part_idx = 0
        for i in range(0, len(rows), max_rows):
            part_data = [header] + rows[i:i+max_rows]
            out_file = f"{base}_part_{part_idx}{ext}"
            with open(out_file, 'w', encoding='utf-8', newline='') as fp:
                writer = csv.writer(fp)
                writer.writerows(part_data)
            part_idx += 1