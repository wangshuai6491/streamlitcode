import os

# 注册自定义函数lineinput的固定代码，不要修改
import streamlit.components.v1 as components
_RELEASE = True
if not _RELEASE:
    _component_func = components.declare_component(
        "lineinput",
        url="http://localhost:5173",
    )
else:
    # 直接使用当前目录的frontend/dist
    build_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend/dist")
    _component_func = components.declare_component(
        "lineinput",
        path=build_dir
    )

def lineinput(name, default_values=None, key=None):
    """
    内联式文本输入框组件，将模板中的{{变量}}替换为输入框。
    
    参数:
        name: 包含{{变量名}}的模板字符串
        default_values: 可选，包含变量默认值的字典
    
    返回值:
        包含变量值字典和拼接后文本的字典
    """
    # 如果没有提供默认值，设置为空字典
    if default_values is None:
        default_values = {}
    
    # 调用底层组件函数，传入name和default_values参数
    component_value = _component_func(name=name, default_values=default_values, key=key, default={"variables": {}, "content": "等待用户输入..."})
    
    # 返回组件的返回值
    return component_value