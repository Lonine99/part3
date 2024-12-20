def save_table(table, file_path):

    if not table.data:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("空表格\n")
        return

    # 计算列宽
    widths = []
    for col_idx in range(len(table.data[0])):
        max_len = 0
        for row in table.data:
            cell_str = str(row[col_idx])
            if len(cell_str) > max_len:
                max_len = len(cell_str)
        widths.append(max_len)

    with open(file_path, 'w', encoding='utf-8') as f:
        for r_idx, row in enumerate(table.data):
            line = " | ".join(str(row[c]).ljust(widths[c]) for c in range(len(row)))
            f.write(line + "\n")