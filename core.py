import copy

class TableStructureError(Exception):
    pass

class Table:
    def __init__(self, data=None, column_types=None):
        """
        data: 二维列表形式，包含表头行（可选）和数据行
        column_types: dict，key为列索引（int），value为type类型或None
        """
        if data is None:
            data = []
        self.data = data
        # 确保表的结构统一
        if len(self.data) > 1:
            length = len(self.data[0])
            for row in self.data:
                if len(row) != length:
                    raise TableStructureError("数据行长度不一致")
        self.column_types = column_types if column_types else {}

        # 尝试应用列类型（如果有）
        self._apply_column_types()

    def _apply_column_types(self):
        """根据已知的列类型转换数据列的类型"""
        if not self.column_types or len(self.data) <= 1:
            return
        header= self.data[0]
        for i, ct in self.column_types.items():
            for r in range(1, len(self.data)):
                try:
                    self.data[r][i] = ct(self.data[r][i])
                except ValueError:
                    # 类型转换异常处理
                    pass

    def get_rows_by_number(self, start, stop=None, copy_table=False):
        """根据行号获取单行或多行
        start, stop 为python切片风格的参数，如果stop为None，只取单行start
        """
        if stop is None:
            stop = start+1
        if start < 0 or stop > len(self.data):
            raise IndexError("行号超出范围")
        new_data = self.data[start:stop]
        if copy_table:
            new_data = copy.deepcopy(new_data)
        return Table(new_data, column_types=copy.deepcopy(self.column_types))

    def get_rows_by_index(self, *vals, copy_table=False):
        """根据第一列的值匹配获取新表格"""
        if len(self.data) <= 1:
            # 没有数据行或没有标题行
            return Table([], column_types=copy.deepcopy(self.column_types))
        header = self.data[0]
        matched = [header]
        for row in self.data[1:]:
            if row[0] in vals:
                matched.append(row)
        if copy_table:
            matched = copy.deepcopy(matched)
        return Table(matched, column_types=copy.deepcopy(self.column_types))

    def get_column_types(self, by_number=True):
        """返回列类型字典"""
        if by_number:
            return self.column_types
        else:
            # 如果需要根据列名返回，可扩展此逻辑
            header = self.data[0] if self.data else []
            return {header[i]: ct for i, ct in self.column_types.items() if i < len(header)}

    def set_column_types(self, types_dict, by_number=True):
        """设置列类型字典，并尝试转换数据"""
        if by_number:
            self.column_types.update(types_dict)
        else:
            # 假设传入键为列名
            if not self.data:
                return
            header = self.data[0]
            for k,v in types_dict.items():
                if k in header:
                    idx = header.index(k)
                    self.column_types[idx] = v
        # 重新应用类型
        self._apply_column_types()

    def get_values(self, column=0):
        """返回指定列的值列表（不包含表头）"""
        if not self.data:
            return []
        if column < 0 or column >= len(self.data[0]):
            raise IndexError("列号超出范围")
        return [row[column] for row in self.data[1:]]

    def get_value(self, column=0):
        """针对单行表格返回单值（不包含表头的单行数据）"""
        if len(self.data) != 2:
            raise ValueError("当前表格不只包含单行数据，无法使用 get_value")
        if column < 0 or column >= len(self.data[0]):
            raise IndexError("列号超出范围")
        return self.data[1][column]

    def set_values(self, values, column=0):
        """设置指定列的值列表"""
        if not self.data:
            raise ValueError("空表格无法设置值")
        if len(values) != len(self.data[1:]):
            raise ValueError("待设置的值数量与表格行数不匹配")
        if column < 0 or column >= len(self.data[0]):
            raise IndexError("列号超出范围")
        for i, val in enumerate(values):
            self.data[i+1][column] = val

    def set_value(self, value, column=0):
        """针对单行表格设置单值"""
        if len(self.data) != 2:
            raise ValueError("当前表格不只包含单行数据，无法使用 set_value")
        if column < 0 or column >= len(self.data[0]):
            raise IndexError("列号超出范围")
        self.data[1][column] = value

    def print_table(self):
        """打印表格"""
        if not self.data:
            print("空表格")
            return
        widths = []
        # 计算列宽
        for col_idx in range(len(self.data[0])):
            max_len = 0
            for row in self.data:
                cell_str = str(row[col_idx])
                if len(cell_str) > max_len:
                    max_len = len(cell_str)
            widths.append(max_len)

        # 打印
        for r_idx, row in enumerate(self.data):
            line = " | ".join(str(row[c]).ljust(widths[c]) for c in range(len(row)))
            print(line)

    @staticmethod
    def concat(table1, table2):
        """表格合并：要求表头一致"""
        if not table1.data or not table2.data:
            raise ValueError("表格数据不能为空")
        if len(table1.data[0]) != len(table2.data[0]):
            raise TableStructureError("两个表格列数不一致，无法合并")
        # 可以检查表头是否相同，如需严格检查请加
        if table1.data[0] != table2.data[0]:
            raise TableStructureError("两个表格表头不一致，无法合并")
        new_data = table1.data[:1] + table1.data[1:] + table2.data[1:]
        new_ct = copy.deepcopy(table1.column_types)
        return Table(new_data, column_types=new_ct)

    def split(self, row_number):
        """按行号拆分表格，row_number为分割点（不包含表头行计数）
           例如：表头1行 + 数据N行，row_number的范围应在1~N-1之间
        """
        if row_number < 1 or row_number >= len(self.data)-1:
            raise ValueError("无效的拆分行号")
        header = self.data[0]
        part1 = [header] + self.data[1:1+row_number]
        part2 = [header] + self.data[1+row_number:]
        return Table(part1, column_types=copy.deepcopy(self.column_types)), Table(part2, column_types=copy.deepcopy(self.column_types))