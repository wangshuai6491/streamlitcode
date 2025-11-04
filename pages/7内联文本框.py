import streamlit as st
import re
import os
import sys
from typing import List, Union, Dict, Any

# 添加父目录到Python路径，确保可以导入__init__.py中的函数
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 直接导入__init__.py中的lineinput函数
from __init__ import lineinput

# 导入模块化的页面函数
# 先确保可以访问主目录
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 再添加模块化目录
modular_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static', '模块化')
sys.path.append(modular_dir)

# 初始化会话状态
def init_session_state():
    # 初始化默认值缓存为空字典，只保留lineinput组件返回的variables
    if 'default_values' not in st.session_state:
        st.session_state.default_values = {}
    # 初始化用地类型会话状态
    if 'land_type' not in st.session_state:
        st.session_state.land_type = '单独选址'

# 更新会话状态中的变量缓存
def update_variable_cache(component_result):
    # 当组件返回结果且包含更新的变量值时，更新会话状态中的缓存
    if component_result and isinstance(component_result, dict):
        # 检查是否有 'variables' 字段，这应该包含用户在组件中修改的变量值
        if 'variables' in component_result and isinstance(component_result['variables'], dict):
            # 更新会话状态中的默认值缓存
            for var_name, var_value in component_result['variables'].items():
                st.session_state.default_values[var_name] = var_value
            # st.success("已更新会话状态中的变量值缓存")
            return True
    return False

# 自定义按钮组样式
def button_group(
    label: str = "",
    options: List[Dict[str, Union[str, bool]]] = None,
    default_value: Union[str, bool] = None,
    key: str = None
    ) -> Union[str, bool]:
    """
    创建一个选择按钮组
    Args:
        label: 组件标签
        options: 选项列表，每个选项包含 label 和 value
        default_value: 默认选中的值
        key: 组件的唯一键
    
    Returns:
        当前选中的值
    """
    if options is None:
        options = [
            {"label": "是", "value": "是"},
            {"label": "否", "value": "否"}
        ]
    
    if default_value is None:
        default_value = options[0]["value"]
    
    # 初始化 session state
    if key is None:
        key = f"button_group_{label}"
    
    if key not in st.session_state:
        st.session_state[key] = default_value
    
    # 显示标签
    if label:
        st.write(label)
    
    # 创建按钮组布局
    cols = st.columns(len(options))
    
    current_value = st.session_state[key]
    
    for i, option in enumerate(options):
        with cols[i]:
            is_selected = current_value == option["value"]
            
            # 按钮样式
            button_style = """
            <style>
            .btn-group-button {
                width: 100%;
                padding: 0.5rem 1rem;
                border: 1px solid #d1d5db;
                background-color: white;
                color: #374151;
                font-size: 0.875rem;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            .btn-group-button:hover {
                background-color: #f3f4f6;
            }
            .btn-group-button.selected {
                background-color: #3b82f6;
                color: white;
                border-color: #3b82f6;
            }
            .btn-group-button:first-child {
                border-top-left-radius: 0.5rem;
                border-bottom-left-radius: 0.5rem;
            }
            .btn-group-button:last-child {
                border-top-right-radius: 0.5rem;
                border-bottom-right-radius: 0.5rem;
            }
            .btn-group-button:not(:first-child):not(:last-child) {
                border-radius: 0;
            }
            </style>
            """
            
            # 按钮类名
            button_class = "btn-group-button"
            if is_selected:
                button_class += " selected"
            
            # 创建按钮
            if st.button(
                option["label"],
                key=f"{key}_{i}",
                use_container_width=True,
                type="primary" if is_selected else "secondary"
            ):
                st.session_state[key] = option["value"]
                st.rerun()
    
    return st.session_state[key]

# 主应用逻辑
if __name__ == "__main__":
    # 初始化会话状态
    init_session_state()
    
    # 在侧边栏添加用地类型选择（所有页面共享）
    st.sidebar.title("全局设置")
    st.sidebar.subheader("用地类型选择")
    st.session_state.land_type = st.sidebar.radio(
        "选择用地类型:",
        ('单独选址', '批次用地'),
        index=1,
        horizontal=False
    )
    
    # 增加侧边栏导航
    st.sidebar.title("模块单元")
    
    # 在这里动态导入，避免文件顶部导入的缓存问题
    modules = {}
    
    # 动态导入所有page_1到page_13模块
    for page_num in range(1, 14):
        module_name = f"page_{page_num}"
        if module_name not in globals():
            try:
                # 使用importlib动态导入模块
                import importlib.util
                module_path = os.path.join(modular_dir, f"{module_name}.py")
                
                if os.path.exists(module_path):
                    spec = importlib.util.spec_from_file_location(module_name, module_path)
                    module = importlib.util.module_from_spec(spec)
                    globals()[module_name] = module
                    spec.loader.exec_module(module)
                    
                    # 将模块的主函数添加到字典中
                    if hasattr(module, module_name):
                        # 设置默认的模块显示名称
                        display_names = {
                            1: "基本情况",
                            2: "审核许可",
                            3: "计划指标",
                            4: "土地预审",
                            5: "权属地类",
                            6: "国土空间规划",
                            7: "耕地占补平衡及永久基本农田占用补划",
                            8: "土地征收",
                            9: "土地利用",
                            10: "违法用地",
                            11: "压矿情况",
                            12: "地灾情况",
                            13: "信访情况"
                        }
                        display_name = display_names.get(page_num, f"模块{page_num}")
                        modules[f"{page_num}: {display_name}"] = getattr(module, module_name)
            except Exception as e:
                st.sidebar.warning(f"导入模块 {module_name} 失败: {str(e)}")
    
    # 创建侧边栏选择器
    selected_module = st.sidebar.selectbox(
        "选择要查看的模块:",
        list(modules.keys())
    )
    
    # 调用选中的模块函数
    selected_function = modules[selected_module]
    component_result = selected_function()
    
    # 更新会话状态中的变量缓存
    update_variable_cache(component_result)
    
    # 把缓存显示放到最后就能确保刷新
    with st.sidebar.expander("当前缓存", expanded=False):
        st.write(st.session_state.default_values)