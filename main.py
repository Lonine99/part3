from io_csv import load_table as load_csv, save_table as save_csv
from io_pickle import load_table as load_pickle, save_table as save_pickle
from io_text import save_table as save_text
from core import Table, TableStructureError

def display_options():
    print("请选择一个操作:")
    print("1. 从 CSV 文件加载表格")
    print("2. 从 Pickle 文件加载表格")
    print("3. 保存表格为 CSV 文件")
    print("4. 保存表格为 Pickle 文件")
    print("5. 保存表格为文本文件")
    print("6. 打印表格")
    print("7. 获取表格的部分行 (按行号)")
    print("8. 获取表格的部分行 (按索引值)")
    print("9. 获取列类型")
    print("10. 设置列类型")
    print("11. 合并两个表格")
    print("12. 拆分表格")
    print("0. 退出")

def main():
    table = None

    while True:
        display_options()
        choice = input("请输入选项: ").strip()

        if choice == "1":
            file_paths = input("请输入 CSV 文件路径 (多个文件用逗号分隔): ").split(",")
            try:
                table = load_csv(file_paths)
                print("CSV 文件加载成功！")
            except TableStructureError as e:
                print(f"表格结构错误: {e}")
            except Exception as e:
                print(f"加载失败: {e}")

        elif choice == "2":
            file_paths = input("请输入 Pickle 文件路径 (多个文件用逗号分隔): ").split(",")
            try:
                table = load_pickle(file_paths)
                print("Pickle 文件加载成功！")
            except TableStructureError as e:
                print(f"表格结构错误: {e}")
            except Exception as e:
                print(f"加载失败: {e}")

        elif choice == "3":
            if table:
                output_path = input("请输入保存的 CSV 文件路径: ").strip()
                max_rows = input("每个文件的最大行数 (留空则不分割): ").strip()
                max_rows = int(max_rows) if max_rows.isdigit() else None
                save_csv(table, output_path, max_rows)
                print(f"表格已保存到 {output_path}")
            else:
                print("当前没有加载任何表格！")

        elif choice == "4":
            if table:
                output_path = input("请输入保存的 Pickle 文件路径: ").strip()
                max_rows = input("每个文件的最大行数 (留空则不分割): ").strip()
                max_rows = int(max_rows) if max_rows.isdigit() else None
                save_pickle(table, output_path, max_rows)
                print(f"表格已保存到 {output_path}")
            else:
                print("当前没有加载任何表格！")

        elif choice == "5":
            if table:
                output_path = input("请输入保存的文本文件路径: ").strip()
                save_text(table, output_path)
                print(f"表格已保存到 {output_path}")
            else:
                print("当前没有加载任何表格！")

        elif choice == "6":
            if table:
                table.print_table()
            else:
                print("当前没有加载任何表格！")

        elif choice == "7":
            if table:
                start = int(input("请输入起始行号: ").strip())
                stop = input("请输入结束行号 (留空则只取一行): ").strip()
                stop = int(stop) if stop else None
                new_table = table.get_rows_by_number(start, stop, copy_table=True)
                new_table.print_table()
            else:
                print("当前没有加载任何表格！")

        elif choice == "8":
            if table:
                indices = input("请输入索引值 (多个值用逗号分隔): ").split(",")
                indices = [val.strip() for val in indices]
                new_table = table.get_rows_by_index(*indices, copy_table=True)
                new_table.print_table()
            else:
                print("当前没有加载任何表格！")

        elif choice == "9":
            if table:
                by_number = input("按列号获取类型? (y/n): ").strip().lower() == "y"
                column_types = table.get_column_types(by_number=by_number)
                print("列类型: ", column_types)
            else:
                print("当前没有加载任何表格！")

        elif choice == "10":
            if table:
                column = input("请输入列号或列名: ").strip()
                col_type = input("请输入列类型 (int, float, bool, str): ").strip()
                col_type = eval(col_type)  # 转换为 Python 类型
                table.set_column_types({int(column): col_type}, by_number=True)
                print("列类型已更新！")
            else:
                print("当前没有加载任何表格！")

        elif choice == "11":
            # 合并表格逻辑
            pass

        elif choice == "12":
            # 拆分表格逻辑
            pass

        elif choice == "0":
            print("退出程序！")
            break

        else:
            print("无效选项，请重新输入！")

if __name__ == "__main__":
    main()