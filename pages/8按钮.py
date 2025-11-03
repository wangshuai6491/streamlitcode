import streamlit as st
from typing import List, Union, Dict, Any

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

# 使用示例
def main():
    st.title("Streamlit 按钮组示例")
    
    # 示例1: 默认的是/否按钮组
    st.subheader("1. 默认按钮组")
    selected1 = button_group("请选择:")
    st.write(f"当前选择: {selected1}")
    
    # 示例2: 自定义选项
    st.subheader("2. 自定义选项")
    custom_options = [
        {"label": "选项A", "value": "A"},
        {"label": "选项B", "value": "B"},
        {"label": "选项C", "value": "C"}
    ]
    selected2 = button_group("请选择一个选项:", custom_options, "B")
    st.write(f"当前选择: {selected2}")
    
    # 示例3: 布尔值选项
    st.subheader("3. 布尔值选项")
    bool_options = [
        {"label": "启用", "value": True},
        {"label": "禁用", "value": False}
    ]
    selected3 = button_group("功能状态:", bool_options, True)
    st.write(f"当前状态: {'启用' if selected3 else '禁用'}")
    
    # 示例4: 多个按钮组
    st.subheader("4. 多个按钮组")
    col1, col2 = st.columns(2)
    
    with col1:
        choice1 = button_group("选择1:", [{"label": "上", "value": "up"}, {"label": "下", "value": "down"}], key="group1")
    
    with col2:
        choice2 = button_group("选择2:", [{"label": "左", "value": "left"}, {"label": "右", "value": "right"}], key="group2")
    
    st.write(f"选择结果: {choice1} + {choice2}")
    

if __name__ == "__main__":
    main()