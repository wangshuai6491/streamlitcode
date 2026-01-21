import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from static.cs import excel_to_json

# 测试参数
excel_file = "e:\\trae\\gitte\\streamlitcode\\static\\家庭承包制数据（只有基础变量）.xlsx"
text_data_start = "A1"
tables_data_mapping = {}
sheetname = "基础变量"

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
        print(f"  tables_data: {item['tables_data']}")
except Exception as e:
    print(f"测试失败，错误信息: {e}")
    import traceback
    traceback.print_exc()
