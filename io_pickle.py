import pickle
import os
from mytable.core import Table, TableStructureError

def load_table(file_list):
    """
    加载单文件或多文件的pickle表格，如果传入列表，则是多文件加载并检查结构一致性。
    """
    if isinstance(file_list, str):
        file_list = [file_list]

    all_data = []
    column_types = {}
    header = None
    for i, f in enumerate(file_list):
        with open(f, 'rb') as fp:
            data_dict = pickle.load(fp)
        if i == 0:
            header = data_dict['data'][0]
            column_types = data_dict.get('column_types', {})
            all_data.extend(data_dict['data'])
        else:
            if data_dict['data'][0] != header:
                raise TableStructureError("多文件加载时表头不一致：{}".format(f))
            all_data.extend(data_dict['data'][1:])
    return Table(all_data, column_types=column_types)

def save_table(table, file_path, max_rows=None):
    """
    保存表格为pickle格式，如果max_rows指定且小于表格总行数，则分拆保存。
    """
    if max_rows is None or max_rows >= (len(table.data)-1):
        # 不拆分
        data_dict = {
            'data': table.data,
            'column_types': table.column_types
        }
        with open(file_path, 'wb') as fp:
            pickle.dump(data_dict, fp)
    else:
        base, ext = os.path.splitext(file_path)
        header = table.data[0]
        rows = table.data[1:]
        part_idx = 0
        for i in range(0, len(rows), max_rows):
            part_data = [header] + rows[i:i+max_rows]
            data_dict = {
                'data': part_data,
                'column_types': table.column_types
            }
            out_file = f"{base}_part_{part_idx}{ext}"
            with open(out_file, 'wb') as fp:
                pickle.dump(data_dict, fp)
            part_idx += 1
