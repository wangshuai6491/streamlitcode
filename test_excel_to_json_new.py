import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from static.cs import excel_to_json

# 测试参数
excel_file = "e:\\trae\\gitte\\streamlitcode\\static\\家庭承包制数据(有表格变量一个sheet一个word).xlsx"
text_data_start = "A1"
tables_data_mapping = {"家庭成员": "A10", "测试表": "A20"}
sheetname = None  # None表示处理所有sheet

# 调用函数并打印结果
try:
    result = excel_to_json(excel_file, text_data_start, tables_data_mapping, sheetname=sheetname)
    print("测试结果:")
    print(result)
    print(f"\n结果长度: {len(result)}")
    print("\n每个元素的结构:")
    for i, item in enumerate(result):
        print(f"\n元素 {i+1}:")
        print(f"  text_data: {item['text_data']}")
        print(f"  tables_data 键: {list(item['tables_data'].keys())}")
        for table_name, table_data in item['tables_data'].items():
            print(f"    {table_name}: {len(table_data)} 行数据")
            if len(table_data) > 0:
                print(f"      表头: {list(table_data[0].keys())}")
                print(f"      第一行数据: {table_data[0]}")
except Exception as e:
    print(f"测试失败，错误信息: {e}")
    import traceback
    traceback.print_exc()
